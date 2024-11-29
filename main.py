import serial
import re
import time
import vgamepad as vg


SERIAL_PORT = 'COM3'
BAUD_RATE = 115200

gamepad = vg.VX360Gamepad()

def read_remote_data():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)
        while True:
            if ser.in_waiting > 0:
                raw = ser.readline().decode('utf-8', "ignore").strip()
                process_data(raw)

def parse_value(value, inputMin, inputMax, outputMin, outputMax):
    value = min(max(value, inputMin), inputMax)

    inputRange = inputMax - inputMin
    outputRange = outputMax - outputMin
    return (value - inputMin) * outputRange / inputRange + outputMin

def process_data(raw):
    data = re.split(r'[a-z]', raw)

    if(len(data) != 5 or data[1] == ''):
        return
    

    roll = parse_value(float(data[1]), 1000, 2000, -1, 1)
    pitch = parse_value(float(data[2]), 1000, 2000, 1, -1)
    yaw = parse_value (float(data[3]), 1000, 2000, -1, 1)
    throttle = parse_value(float(data[4]), 1000, 2000, -1, 1)

    print(f'Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}, Throttle: {throttle}')

    gamepad.right_joystick_float(roll, pitch)
    gamepad.left_joystick_float(yaw, throttle)

    gamepad.update()

if __name__ == "__main__":
    read_remote_data()