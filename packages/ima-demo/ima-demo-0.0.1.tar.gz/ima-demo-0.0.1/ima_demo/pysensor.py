import ima.telemetrix
import time

senor_distance = []
Pin_dict = {}


for i in range(2, 14):
    Pin_dict.update({i: [False]})
Pin_dict.update({'A0': [False]})
Pin_dict.update({'A1': [False]})
Pin_dict.update({'A2': [False]})
Pin_dict.update({'A3': [False]})
Pin_dict.update({'A4': [False]})
Pin_dict.update({'A5': [False]})
Ard = ima.telemetrix.Telemetrix()


def mode(pattern, pin, direction):
    if not Pin_dict[pin][0] and Pin_dict[pin][0] is not 0:
        if pattern == 'd' and pin in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            Ard.set_pin_mode_digital_output(pin)
            return True
        elif pattern == 'a' and pin in [3, 5, 6, 9, 10, 11]:
            if direction == 'o':
                Ard.set_pin_mode_analog_output(pin)
            return True
        elif pattern == 'a' and direction == 'i' and pin in ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']:
            return True
        else:
            return False
    else:
        return '管脚已被占用'


def write(pattern, pin, value):
    if mode(pattern, pin, 'o'):
        if value in [0, 1]:
            # print('数字写入')
            Ard.digital_write(pin, value)
        else:
            # print('模拟写入')
            Ard.analog_write(pin, value)
    else:
        return '管脚模式错误'

def read(pattern, pin):
    if mode(pattern, pin, 'i'):
        if pattern == 'd':
            for i in range(2):
                Ard.set_pin_mode_digital_input(pin, Pin_dict[pin])
                time.sleep(0.1)
        if pattern == 'a':
            for i in range(2):
                Ard.set_pin_mode_analog_input(int(pin[1]), Pin_dict[pin], differential=0)
                time.sleep(0.1)
        return Pin_dict[pin]
    else:
        return '管脚模式错误'


def hs(TRIGGER_PIN, ECHO_PIN):
    if not Pin_dict[TRIGGER_PIN][0] and not Pin_dict[ECHO_PIN][0]:
        Pin_dict[TRIGGER_PIN][0] = True
        Pin_dict[ECHO_PIN][0] = True
        for i in range(2):
            Ard.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN, senor_distance)
            time.sleep(0.1)
        return senor_distance
    else:
        return '管脚已被占用'


def servo(pin, angle):
    if mode('a',pin,'o') and not Pin_dict[pin][0]:
        Pin_dict[pin][0] = True
        Ard.set_pin_mode_servo(pin)
        time.sleep(0.2)
        #Ard.set_pin_mode_servo(pin)
        Ard.servo_write(pin, int(angle))
    else:
        Ard.servo_write(pin, int(angle))


def motor(INV, ING, speed):
    if speed >= 1:
        write('a', INV, speed+60)
        # time.sleep(0.2)
        write('a', ING, 0)


