import serial
import time

arduino = serial.Serial('COM5', 9600, timeout=.1)
command = input("Enter command: ")
arduino.write(command.encode())
time.sleep(1)
print(arduino.read_all())