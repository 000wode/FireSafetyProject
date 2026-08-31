import pandas as pd

normal = pd.read_csv('real_sensor_data.csv')
fire = pd.read_csv('real_sensor_data_fire.csv')

print("═" * 40)
print("正常数据统计:")
print(normal[['smoke', 'flame', 'temp']].describe().round(1))

print("\n异常数据统计:")
print(fire[['smoke', 'flame', 'temp']].describe().round(1))

print("\n对比:")
print(f"正常烟雾均值: {normal['smoke'].mean():.1f} vs 异常: {fire['smoke'].mean():.1f}")
print(f"正常火焰均值: {normal['flame'].mean():.1f} vs 异常: {fire['flame'].mean():.1f}")