import sys
import glob
import serial

serialComunication = serial.Serial(port = "COM7", baudrate=250000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO)

print(type(serialComunication))