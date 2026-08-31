# 真实传感器数据采集器
import serial
import time
import csv

PORT = 'COM3'
BAUD = 9600
DURATION = 90
FILENAME = 'real_sensor_data_fire.csv'

ser = serial.Serial(PORT, BAUD)
time.sleep(2)

print(f"开始采集 {DURATION} 秒真实传感器数据...")
print("=" * 50)

with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['time', 'smoke', 'flame', 'temp', 'hum'])

    start = time.time()
    count = 0

    while time.time() - start < DURATION:
        try:
            line = ser.readline().decode().strip()
            print(f"[原始] {line}")        # ← 先打印原始行
            if line and not line.startswith('time'):
                values = line.split(',')
                if len(values) >= 5:        # ← 加长度检查
                    writer.writerow(values)
                    count += 1
                    print(f"[{count:3d}] S={values[1]:>4s} F={values[2]:>4s} "
                          f"T={values[3]:>5s} H={values[4]:>5s}")
        except Exception as e:
            print("读取错误:", e)
            break

ser.close()
print("=" * 50)
print(f"采集完成！共 {count} 条数据 → {FILENAME}")