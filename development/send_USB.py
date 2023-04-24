import serial
import time
import keyboard

serialPort = serial.Serial(port = "COM7", baudrate=9600,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
   
# Read line   
while True:
    serialPort.write("Hello World!!!".encode('Ascii'))
    receive = serialPort.read()
    print(receive.decode('Ascii'))
    #time.sleep(1)

    if keyboard.is_pressed('q'):
        print("O usuario quis sair")
        break
    
serialPort.close()