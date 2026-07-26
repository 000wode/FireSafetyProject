import serial
import time

ser = serial.Serial('COM3', 9600)
time.sleep(2)

print("读取传感器数据...")
for i in range(10):
    line = ser.readline().decode().strip()
    print(f"[{i+1}] {line}")

ser.close()