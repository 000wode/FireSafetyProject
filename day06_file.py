data=[
    "时间 温度 湿度 状态"
     "14:00,25.3,60,正常",
    "14:01,25.8,61,正常",
    "14:02,28.5,62,⚠️高温",
    "14:03,29.1,63,⚠️高温",
    "14:04,26.2,61,正常",
]
with open("sensor_log.csv", "w", encoding="utf-8") as f:
          for line in data:
              f.write(line + "\n")
print("sensor_log.csv已生成")
with open("sensor_log.csv", "r", encoding="utf-8") as f:
          print(f.read())