# 列表
sensors = ["MQ-2烟雾", "火焰", "DHT11温度", "DHT11湿度"]
sensors.append("蜂鸣器")
print(f"传感器清单：{sensors}")
print(f"一共 {len(sensors)} 个组件")

# 字典
project = {
    "名称": "智安哨兵",
    "作者": "弥天",
    "天数": 45
}
print(f"项目：{project['名称']}")
print(f"作者：{project['作者']}")