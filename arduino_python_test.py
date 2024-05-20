from datetime import datetime
import serial
import sys
import glob
import numpy as np
import csv

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    # Windows
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    # Linux
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    # Mac
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# Find and open Arduino port
port = serial_ports()[0]  # Assuming Arduino port is the first one
arduino = serial.Serial(port=port, baudrate=115200)

# Parameters
stop_num = 20
delay = 5

pulse = 0
pulse_times = []
while True:
    var = input()
    print("You entered: " + var)

    if var == "":
        arduino.write('8'.encode('utf-8'))
        pulse_times.append(datetime.now())
        pulse += 1

        if pulse == stop_num:
            break

# Save Python timestamps
filename = 'delay_' + str(delay) + 'ms.csv'
with open(filename, 'w') as f:
    write = csv.writer(f)
    write.writerow(pulse_times)
