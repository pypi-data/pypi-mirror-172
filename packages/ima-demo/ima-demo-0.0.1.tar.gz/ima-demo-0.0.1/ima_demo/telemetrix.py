"""
 Copyright (c) 2021 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import socket
import sys
import threading
import time
from collections import deque

import serial
# noinspection PyPackageRequirementscd
from serial.serialutil import SerialException
# noinspection PyPackageRequirements
from serial.tools import list_ports

# noinspection PyUnresolvedReferences
from ima.private_constants import PrivateConstants


# noinspection PyPep8,PyMethodMayBeStatic,GrazieInspection,PyBroadException,PyCallingNonCallable
class Telemetrix(threading.Thread):
    """
    This class exposes and implements the telemetrix API.
    It uses threading to accommodate concurrency.
    It includes the public API methods as well as
    a set of private methods.

    """

    # noinspection PyPep8,PyPep8,PyPep8
    def __init__(self, com_port=None, arduino_instance_id=1,
                 arduino_wait=4, sleep_tune=0.000001,
                 shutdown_on_exception=True,
                 ip_address=None, ip_port=31335):

        """

        :param com_port: e.g. COM3 or /dev/ttyACM0.
                         Only use if you wish to bypass auto com port
                         detection.

        :param arduino_instance_id: Match with the value installed on the
                                    arduino-telemetrix sketch.

        :param arduino_wait: Amount of time to wait for an Arduino to
                             fully reset itself.

        :param sleep_tune: A tuning parameter (typically not changed by user)

        :param shutdown_on_exception: call shutdown before raising
                                      a RunTimeError exception, or
                                      receiving a KeyboardInterrupt exception

        :param ip_address: ip address of tcp/ip connected device.

        :param ip_port: ip port of tcp/ip connected device
        """

        # initialize threading parent
        threading.Thread.__init__(self)

        # create the threads and set them as daemons so
        # that they stop when the program is closed

        # create a thread to interpret received serial data
        self.the_reporter_thread = threading.Thread(target=self._reporter)
        self.the_reporter_thread.daemon = True

        self.ip_address = ip_address
        self.ip_port = ip_port

        if not self.ip_address:
            self.the_data_receive_thread = threading.Thread(target=self._serial_receiver)
        else:
            self.the_data_receive_thread = threading.Thread(target=self._tcp_receiver)

        self.the_data_receive_thread.daemon = True

        # flag to allow the reporter and receive threads to run.
        self.run_event = threading.Event()

        # check to make sure that Python interpreter is version 3.7 or greater
        python_version = sys.version_info
        if python_version[0] >= 3:
            if python_version[1] >= 7:
                pass
            else:
                raise RuntimeError("ERROR: Python 3.7 or greater is "
                                   "required for use of this program.")

        # save input parameters as instance variables
        self.com_port = com_port
        self.arduino_instance_id = arduino_instance_id
        self.arduino_wait = arduino_wait
        self.sleep_tune = sleep_tune
        self.shutdown_on_exception = shutdown_on_exception

        # create a deque to receive and process data from the arduino
        self.the_deque = deque()

        # The report_dispatch dictionary is used to process
        # incoming report messages by looking up the report message
        # and executing its associated processing method.

        self.report_dispatch = {}

        # To add a command to the command dispatch table, append here.
        self.report_dispatch.update(
            {PrivateConstants.LOOP_COMMAND: self._report_loop_data})
        self.report_dispatch.update(
            {PrivateConstants.DEBUG_PRINT: self._report_debug_data})
        self.report_dispatch.update(
            {PrivateConstants.DIGITAL_REPORT: self._digital_message})
        self.report_dispatch.update(
            {PrivateConstants.ANALOG_REPORT: self._analog_message})
        self.report_dispatch.update(
            {PrivateConstants.FIRMWARE_REPORT: self._firmware_message})
        self.report_dispatch.update({PrivateConstants.I_AM_HERE_REPORT: self._i_am_here})
        self.report_dispatch.update(
            {PrivateConstants.SONAR_DISTANCE: self._sonar_distance_report})
        self.report_dispatch.update(
            {PrivateConstants.FEATURES:
                 self._features_report})

        # dictionaries to store the callbacks for each pin
        self.analog_callbacks = {}

        self.digital_callbacks = {}
        self.old_digital_data = {
            2:0, 3:0, 4:0, 5:0,
            6:0, 7:0, 8:0, 9:0,
            10:0, 11:0, 12:0, 13:0
        }

        self.i2c_callback = None
        self.i2c_callback2 = None

        self.i2c_1_active = False
        self.i2c_2_active = False

        self.spi_callback = None

        self.onewire_callback = None

        self.cs_pins_enabled = []

        # the trigger pin will be the key to retrieve
        # the callback for a specific HC-SR04
        self.sonar_callbacks = {}

        self.sonar_count = 0

        self.dht_callbacks = {}

        self.dht_count = 0

        # serial port in use
        self.serial_port = None

        # socket for tcp/ip communications
        self.sock = None

        # flag to indicate we are in shutdown mode
        self.shutdown_flag = False

        # debug loopback callback method
        self.loop_back_callback = None

        # flag to indicate the start of a new report
        # self.new_report_start = True

        # firmware version to be stored here
        self.firmware_version = []

        # reported arduino instance id
        self.reported_arduino_id = []

        # reported features
        self.reported_features = 1

        # flag to indicate if i2c was previously enabled
        self.i2c_enabled = False

        # flag to indicate if spi is initialized
        self.spi_enabled = False

        # flag to indicate if onewire is initialized
        self.onewire_enabled = False

        # stepper motor variables

        # updated when a new motor is added
        self.next_stepper_assigned = 0

        # valid list of stepper motor interface types
        self.valid_stepper_interfaces = [1, 2, 3, 4, 6, 8]

        # maximum number of steppers supported
        self.max_number_of_steppers = 4

        # number of steppers created - not to exceed the maximum
        self.number_of_steppers = 0

        # dictionary to hold stepper motor information
        self.stepper_info = {'instance': False, 'is_running': None,
                             'maximum_speed': 1, 'speed': 0, 'acceleration': 0,
                             'distance_to_go_callback': None,
                             'target_position_callback': None,
                             'current_position_callback': None,
                             'is_running_callback': None,
                             'motion_complete_callback': None,
                             'acceleration_callback': None}

        # build a list of stepper motor info items
        self.stepper_info_list = []
        # a list of dictionaries to hold stepper information
        for motor in range(self.max_number_of_steppers):
            self.stepper_info_list.append(self.stepper_info)

        self.the_reporter_thread.start()
        self.the_data_receive_thread.start()

        # print(f"Telemetrix:  Version {PrivateConstants.TELEMETRIX_VERSION}\n\n"
        #       f"Copyright (c) 2021 Alan Yorinks All Rights Reserved.\n")
        print('等待智能硬件启动')
        # using the serial link
        if not self.ip_address:
            if not self.com_port:
                # user did not specify a com_port
                try:
                    self._find_arduino()
                except KeyboardInterrupt:
                    if self.shutdown_on_exception:
                        self.shutdown()
            else:
                # com_port specified - set com_port and baud rate
                try:
                    self._manual_open()
                except KeyboardInterrupt:
                    if self.shutdown_on_exception:
                        self.shutdown()

            if self.serial_port:
                # print(
                #     f"Arduino compatible device found and connected to {self.serial_port.port}")

                self.serial_port.reset_input_buffer()
                self.serial_port.reset_output_buffer()

            # no com_port found - raise a runtime exception
            else:
                if self.shutdown_on_exception:
                    self.shutdown()
                raise RuntimeError('No Arduino Found or User Aborted Program')
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip_address, self.ip_port))
            print(f'Successfully connected to: {self.ip_address}:{self.ip_port}')

        # allow the threads to run
        self._run_threads()
        # print(f'Waiting for Arduino to reset')
        # print(f'Reset Complete')

        # get telemetrix firmware version and print it
        # print('\nRetrieving Telemetrix4Arduino firmware ID...')
        self._get_firmware_version()
        if not self.firmware_version:
            if self.shutdown_on_exception:
                self.shutdown()
            raise RuntimeError(f'Telemetrix4Arduino firmware version')

        else:
            pass
            # print(f'Telemetrix4Arduino firmware version: {self.firmware_version[0]}.'
            #       f'{self.firmware_version[1]}.{self.firmware_version[2]}')
        command = [PrivateConstants.ENABLE_ALL_REPORTS]
        self._send_command(command)

        # get the features list
        command = [PrivateConstants.GET_FEATURES]
        self._send_command(command)
        time.sleep(.2)

        # Have the server reset its data structures
        command = [PrivateConstants.RESET]
        self._send_command(command)

    def _find_arduino(self):
        """
                This method will search all potential serial ports for an Arduino
                containing a sketch that has a matching arduino_instance_id as
                specified in the input parameters of this class.

                This is used explicitly with the Telemetrix4Arduino sketch.
                """

        # a list of serial ports to be checked
        serial_ports = []

        # print('Opening all potential serial ports...')
        the_ports_list = list_ports.comports()
        for port in the_ports_list:
            if port.pid is None:
                continue
            try:
                self.serial_port = serial.Serial(port.device, 115200,
                                                 timeout=1, writeTimeout=0)
            except SerialException:
                continue
            # create a list of serial ports that we opened
            serial_ports.append(self.serial_port)

            # display to the user
            # print('\t' + port.device)

            # clear out any possible data in the input buffer
        # wait for arduino to reset
        # print(f'\nWaiting {self.arduino_wait} seconds(arduino_wait) for Arduino devices to '
        #       'reset...')
        # temporary for testing
        time.sleep(self.arduino_wait)

        # check for correct arduino device
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()
        print(f'启动成功')
    def _manual_open(self):
        """
        Com port was specified by the user - try to open up that port

        """
        # if port is not found, a serial exception will be thrown
        try:
            print(f'Opening {self.com_port}...')
            self.serial_port = serial.Serial(self.com_port, 115200,
                                             timeout=1, writeTimeout=0)

            print(
                f'\nWaiting {self.arduino_wait} seconds(arduino_wait) for Arduino devices to '
                'reset...')
            self._run_threads()
            time.sleep(self.arduino_wait)

            self._get_arduino_id()

            if self.reported_arduino_id != self.arduino_instance_id:
                if self.shutdown_on_exception:
                    self.shutdown()
                raise RuntimeError(f'Incorrect Arduino ID: {self.reported_arduino_id}')
            # print('Valid Arduino ID Found.')
            # get arduino firmware version and print it
            # print('\nRetrieving Telemetrix4Arduino firmware ID...')
            self._get_firmware_version()

            if not self.firmware_version:
                if self.shutdown_on_exception:
                    self.shutdown()
                raise RuntimeError(
                    f'Telemetrix4Arduino Sketch Firmware Version Not Found')

            else:
                print(f'Telemetrix4Arduino firmware version: {self.firmware_version[0]}.'
                      f'{self.firmware_version[1]}')
        except KeyboardInterrupt:
            if self.shutdown_on_exception:
                self.shutdown()
            raise RuntimeError('User Hit Control-C')

    def analog_write(self, pin, value):
        """
        Set the specified pin to the specified value.

        :param pin: arduino pin number

        :param value: pin value (maximum 16 bits)

        """
        value_msb = value >> 8
        value_lsb = value & 0xff
        command = [PrivateConstants.ANALOG_WRITE, pin, value_msb, value_lsb]
        self._send_command(command)

    def digital_write(self, pin, value):
        """
        Set the specified pin to the specified value.

        :param pin: arduino pin number

        :param value: pin value (1 or 0)

        """

        command = [PrivateConstants.DIGITAL_WRITE, pin, value]
        self._send_command(command)


    def servo_write(self, pin_number, angle):
        """

        Set a servo attached to a pin to a given angle.

        :param pin_number: pin

        :param angle: angle (0-180)

        """
        command = [PrivateConstants.SERVO_WRITE, pin_number, angle]
        self._send_command(command)


    def _get_arduino_id(self):
        """
        Retrieve arduino-telemetrix arduino id

        """
        command = [PrivateConstants.ARE_U_THERE]
        self._send_command(command)
        # provide time for the reply
        time.sleep(.5)

    def _get_firmware_version(self):
        """
        This method retrieves the
        arduino-telemetrix firmware version

        """
        command = [PrivateConstants.GET_FIRMWARE_VERSION]
        self._send_command(command)
        # provide time for the reply
        time.sleep(.5)


    def set_pin_mode_analog_output(self, pin_number):
        """
        Set a pin as a pwm (analog output) pin.

        :param pin_number:arduino pin number

        """
        self._set_pin_mode(pin_number, PrivateConstants.AT_OUTPUT)

    def set_pin_mode_analog_input(self, pin_number, old_value, differential=0):
        """
        Set a pin as an analog input.

        :param pin_number: arduino pin number

        :param differential: difference in previous to current value before
                             report will be generated

        :param callback: callback function


        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for analog input pins = 2

        """
        self._set_pin_mode(pin_number, PrivateConstants.AT_ANALOG, old_value, differential)
        # pass
    def set_pin_mode_digital_input(self, pin_number,old_value):
        """
        Set a pin as a digital input.

        :param pin_number: arduino pin number

        :param callback: callback function


        callback returns a data list:

        [pin_type, pin_number, pin_value, raw_time_stamp]

        The pin_type for digital input pins = 0

        """
        self._set_pin_mode(pin_number, PrivateConstants.AT_INPUT,old_value)


    def set_pin_mode_digital_output(self, pin_number):
        """
        Set a pin as a digital output pin.

        :param pin_number: arduino pin number
        """

        self._set_pin_mode(pin_number, PrivateConstants.AT_OUTPUT)


    # noinspection PyRedundantParentheses
    def set_pin_mode_servo(self, pin_number, min_pulse=544, max_pulse=2400):
        """

        Attach a pin to a servo motor

        :param pin_number: pin

        :param min_pulse: minimum pulse width

        :param max_pulse: maximum pulse width

        """

        minv = (min_pulse).to_bytes(2, byteorder="big")
        maxv = (max_pulse).to_bytes(2, byteorder="big")

        command = [PrivateConstants.SERVO_ATTACH, pin_number,
                   minv[0], minv[1], maxv[0], maxv[1]]
        self._send_command(command)

    def set_pin_mode_sonar(self, trigger_pin, echo_pin,
                           old_value):
        """

        :param trigger_pin:

        :param echo_pin:

        :param callback: callback

        callback data: [PrivateConstants.SONAR_DISTANCE, trigger_pin, distance_value, time_stamp]

        """
        if self.sonar_count < PrivateConstants.MAX_SONARS - 1:
            self.sonar_callbacks[trigger_pin] = old_value
            self.sonar_count += 1

            command = [PrivateConstants.SONAR_NEW, trigger_pin, echo_pin]
            self._send_command(command)
        else:
            if self.shutdown_on_exception:
                self.shutdown()
            raise RuntimeError(
                f'Maximum Number Of Sonars Exceeded - set_pin_mode_sonar fails for pin {trigger_pin}')



    def _set_pin_mode(self, pin_number, pin_state, old_value = 0, differential=0):
        """
        A private method to set the various pin modes.

        :param pin_number: arduino pin number

        :param pin_state: INPUT/OUTPUT/ANALOG/PWM/PULLUP
                         For SERVO use: set_pin_mode_servo
                         For DHT   use: set_pin_mode_dht

        :param differential: for analog inputs - threshold
                             value to be achieved for report to
                             be generated

        :param callback: A reference to a call back function to be
                         called when pin data value changes

        """

        if pin_state == PrivateConstants.AT_INPUT:
            # old_value.append(self.old_digital_data[pin_number])
            self.digital_callbacks[pin_number] = old_value
        elif pin_state == PrivateConstants.AT_INPUT_PULLUP:
            self.digital_callbacks[pin_number] = old_value
        elif pin_state == PrivateConstants.AT_ANALOG:
            self.analog_callbacks[pin_number] = old_value
        else:
            pass

        if pin_state == PrivateConstants.AT_INPUT:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_INPUT, 1]

        elif pin_state == PrivateConstants.AT_INPUT_PULLUP:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_INPUT_PULLUP, 1]

        elif pin_state == PrivateConstants.AT_OUTPUT:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_OUTPUT]

        elif pin_state == PrivateConstants.AT_ANALOG:
            command = [PrivateConstants.SET_PIN_MODE, pin_number,
                       PrivateConstants.AT_ANALOG,
                       differential >> 8, differential & 0xff, 1]
        else:
            if self.shutdown_on_exception:
                self.shutdown()
            raise RuntimeError('Unknown pin state')

        if command:
            self._send_command(command)

    def shutdown(self):
        """
        This method attempts an orderly shutdown
        If any exceptions are thrown, they are ignored.
        """
        self.shutdown_flag = True

        self._stop_threads()

        try:
            command = [PrivateConstants.STOP_ALL_REPORTS]
            self._send_command(command)
            time.sleep(.5)

            if self.ip_address:
                try:
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                except Exception:
                    pass
            else:
                try:
                    self.serial_port.reset_input_buffer()
                    self.serial_port.reset_output_buffer()

                    self.serial_port.close()

                except (RuntimeError, SerialException, OSError):
                    # ignore error on shutdown
                    pass
        except Exception:
            raise RuntimeError('Shutdown failed - could not send stop streaming message')






    '''
    report message handlers
    '''

    def _analog_message(self, data):
        """
        This is a private message handler method.
        It is a message handler for analog messages.

        :param data: message data

        """
        pin = data[0]
        value = (data[1] << 8) + data[2]
        # set the current value in the pin structure
        if self.analog_callbacks[pin][0] != value:
            self.analog_callbacks[pin][0] = value


    def _digital_message(self, data):
        """
        This is a private message handler method.
        It is a message handler for Digital Messages.

        :param data: digital message

        """
        pin = data[0]
        value = data[1]
        if self.digital_callbacks[pin][0] != value:
            self.digital_callbacks[pin][0] = value
    def _firmware_message(self, data):
        """
        Telemetrix4Arduino firmware version message

        :param data: data[0] = major number, data[1] = minor number.

                               data[2] = patch number
        """

        self.firmware_version = [data[0], data[1], data[2]]

    def _i_am_here(self, data):
        """
        Reply to are_u_there message
        :param data: arduino id
        """
        self.reported_arduino_id = data[0]


    def _report_debug_data(self, data):
        """
        Print debug data sent from Arduino
        :param data: data[0] is a byte followed by 2
                     bytes that comprise an integer
        :return:
        """
        value = (data[1] << 8) + data[2]
        print(f'DEBUG ID: {data[0]} Value: {value}')

    def _report_loop_data(self, data):
        """
        Print data that was looped back
        :param data: byte of loop back data
        :return:
        """
        if self.loop_back_callback:
            self.loop_back_callback(data)

    def _send_command(self, command):
        """
        This is a private utility method.


        :param command:  command data in the form of a list

        """
        # the length of the list is added at the head
        command.insert(0, len(command))
        send_message = bytes(command)

        if self.serial_port:
            try:
                self.serial_port.write(send_message)
            except SerialException:
                if self.shutdown_on_exception:
                    self.shutdown()
                raise RuntimeError('write fail in _send_command')
        elif self.ip_address:
            self.sock.sendall(send_message)
        else:
            raise RuntimeError('No serial port or ip address set.')


    def _sonar_distance_report(self, report):
        """

        :param report: data[0] = trigger pin, data[1] and data[2] = distance

        callback report format: [PrivateConstants.SONAR_DISTANCE, trigger_pin, distance_value, time_stamp]
        """

        # get callback from pin number
        cb = self.sonar_callbacks[report[0]]
        # print((report[1] << 8) + report[2])
        if len(cb) < 1:
            cb.append(((report[1] << 8) + report[2]))
        else:
            cb[0] = (report[1] << 8) + report[2]
        # build report data
        # cb_list = [PrivateConstants.SONAR_DISTANCE, report[0],
        #            ((report[1] << 8) + report[2]), time.time()]
        #
        # cb(cb_list)


    def _features_report(self, report):
        self.reported_features = report[0]

    def _run_threads(self):
        self.run_event.set()

    def _is_running(self):
        return self.run_event.is_set()

    def _stop_threads(self):
        self.run_event.clear()

    def _reporter(self):
        """
        This is the reporter thread. It continuously pulls data from
        the deque. When a full message is detected, that message is
        processed.
        """
        self.run_event.wait()

        while self._is_running() and not self.shutdown_flag:
            if len(self.the_deque):
                # response_data will be populated with the received data for the report
                response_data = []
                packet_length = self.the_deque.popleft()
                # print('packet_length:',packet_length)
                if packet_length:
                    # get all the data for the report and place it into response_data
                    for i in range(packet_length):
                        while not len(self.the_deque):
                            time.sleep(self.sleep_tune)
                        data = self.the_deque.popleft()
                        response_data.append(data)
                    # print('response_data',response_data)
                    # get the report type and look up its dispatch method
                    # here we pop the report type off of response_data
                    report_type = response_data.pop(0)
                    # print(report_type)

                    # retrieve the report handler from the dispatch table
                    dispatch_entry = self.report_dispatch.get(report_type)
                    # if there is additional data for the report,
                    # it will be contained in response_data
                    # noinspection PyArgumentList
                    dispatch_entry(response_data)
                    continue
                else:
                    if self.shutdown_on_exception:
                        self.shutdown()
                    raise RuntimeError(
                        'A report with a packet length of zero was received.')
            else:
                time.sleep(self.sleep_tune)

    def _serial_receiver(self):
        """
        Thread to continuously check for incoming data.
        When a byte comes in, place it onto the deque.
        """
        self.run_event.wait()

        # Don't start this thread if using a tcp/ip transport
        if self.ip_address:
            return

        while self._is_running() and not self.shutdown_flag:
            # we can get an OSError: [Errno9] Bad file descriptor when shutting down
            # just ignore it
            try:
                if self.serial_port.inWaiting():
                    c = self.serial_port.read()
                    self.the_deque.append(ord(c))
                    # print('c:',ord(c))
                else:
                    time.sleep(self.sleep_tune)
                    # continue
            except OSError:
                pass

    def _tcp_receiver(self):
        """
        Thread to continuously check for incoming data.
        When a byte comes in, place it onto the deque.
        """
        self.run_event.wait()

        # Start this thread only if ip_address is set

        if self.ip_address:

            while self._is_running() and not self.shutdown_flag:
                try:
                    payload = self.sock.recv(1)
                    self.the_deque.append(ord(payload))
                except Exception:
                    pass
        else:
            return
