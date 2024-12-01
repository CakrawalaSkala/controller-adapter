# Remote to Virtual Gamepad

This project converts remote inputs received through a serial connection into virtual Xbox 360 gamepad controls.

## Prerequisites

- Python 3.x
- A serial connection to the remote
- Windows OS (vgamepad requirement)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/CakrawalaSkala/liftoff-controller.git
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Configuration

The default settings in `main.py` are:
- Serial Port: COM3
- Baud Rate: 115200

To change these, modify the constants at the top of `main.py`:
```python
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200
```

## Usage

Run the script:
```bash
python main.py
```

The script will continuously read data from the serial port and convert it into Xbox 360 gamepad controls. The script will exit when the user closes the terminal window.

## Input Mapping

- Roll → Right joystick X-axis
- Pitch → Right joystick Y-axis
- Yaw → Left joystick X-axis
- Throttle → Left joystick Y-axis