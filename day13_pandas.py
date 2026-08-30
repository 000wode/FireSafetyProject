# 传感器数据分析入门
import pandas as pd
import numpy as np

# ══ 1. 生成模拟的传感器日志（模拟 Arduino 采集 1 小时）══
np.random.seed(7)

time = pd.date_range('2026-08-01 09:00', periods=360, freq='10s')

# 正常时段 20 分钟 + 异常时段 10 分钟 + 恢复 30 分钟
smoke = np.concatenate([
    np.random.normal(30, 8, 120),     # 正常：30±8
    np.random.normal(400, 80, 60),    # 烟雾事件：400±80
    np.random.normal(32, 9, 180)      # 恢复
])
flame = np.concatenate([
    np.random.normal(1000, 20, 120),  # 正常：无火
    np.random.normal(150, 60, 60),    # 有火：150±60
    np.random.normal(990, 25, 180)    # 恢复
])
temp = np.concatenate([
    np.random.normal(24, 1, 120),
    np.random.normal(38, 4, 60),
    np.random.normal(25, 1.5, 180)
])

df = pd.DataFrame({
    '时间': time,
    '烟雾': smoke.round(1),
    '火焰': flame.round(0),
    '温度': temp.round(1)
})

print("═" * 50)
print("数据概览（前 5 行）:")
print(df.head())
print("\n数据信息:")
print(df.info())

print("═" * 50)
print("\n描述性统计:")
print(df.describe().round(1))

print("═" * 50)
print("\n各列均值:")
print(df[['烟雾', '火焰', '温度']].mean().round(1))

print("═" * 50)
print("\n找出烟雾 > 150 的记录（潜在事件）:")
events = df[df['烟雾'] > 150]
print(f"共 {len(events)} 条异常记录")
print(events.head())

print("═" * 50)
print("\n火焰 < 500 的记录（明火检测）:")
fires = df[df['火焰'] < 500]
print(f"共 {len(fires)} 条火焰记录")
print(fires.head())

print("═" * 50)
print("\n事件窗口统计:")
if len(events) > 0:
    print(f"烟雾事件持续: 从 {events['时间'].iloc[0]} 到 {events['时间'].iloc[-1]}")
    print(f"烟雾峰值: {events['烟雾'].max()}")