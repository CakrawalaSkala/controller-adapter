import serial
import re
import time
import vgamepad as vg


# Config
SERIAL_PORT = 'COM20'
BAUD_RATE = 115200
UPDATE_RATE = 1000 # makin kecil makin responsif, tapi jitter

# Sensitivity (1-500) semakin kecil, semakin sensitif
ROLL_SENSITIVITY = 500
PITCH_SENSITIVITY = 500
YAW_SENSITIVITY = 500
THROTTLE_SENSITIVITY = 500

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

last_update = 0
roll = 0
pitch = 0
yaw = 0
throttle = 0

data_count = 0
failed_count = 0

ROLL_MIN = 1500 - ROLL_SENSITIVITY
ROLL_MAX = 1500 + ROLL_SENSITIVITY
PITCH_MIN = 1500 - PITCH_SENSITIVITY
PITCH_MAX = 1500 + PITCH_SENSITIVITY
YAW_MIN = 1500 - YAW_SENSITIVITY
YAW_MAX = 1500 + YAW_SENSITIVITY
THROTTLE_MIN = 1500 - THROTTLE_SENSITIVITY
THROTTLE_MAX = 1500 + THROTTLE_SENSITIVITY

def process_data(raw):
    current_time = time.time_ns() // 1000  # Convert to microseconds

    data = re.split(r'[a-z]', raw)

    if len(data) != 5 or data[1] == '':
        failed_count += 1
        print("Failed to parse data")
    else:
        data_count += 1

        roll += parse_value(float(data[1]), ROLL_MIN, ROLL_MAX, -1, 1)
        pitch += parse_value(float(data[2]), PITCH_MIN, PITCH_MAX, 1, -1)
        yaw += parse_value (float(data[3]), YAW_MIN, YAW_MAX, -1, 1)
        throttle += parse_value(float(data[4]), THROTTLE_MIN, THROTTLE_MAX, -1, 1)

    if current_time - last_update >= UPDATE_RATE:
        if failed_count == data_count:
            gamepad.right_joystick_float(0, 0)
            gamepad.left_joystick_float(0, 0.8)
        else:
            gamepad.right_joystick_float(roll / data_count, pitch / data_count)
            gamepad.left_joystick_float(yaw / data_count, throttle / data_count)

        data_count = 0
        failed_count = 0
        last_update = current_time

        roll = 0
        pitch = 0
        yaw = 0
        throttle = 0

        gamepad.update()

if __name__ == "__main__":
    read_remote_data()