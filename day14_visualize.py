# 传感器数据可视化
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(7)

time = pd.date_range('2026-08-01 09:00', periods=360, freq='10s')
smoke = np.concatenate([
    np.random.normal(30, 8, 120),
    np.random.normal(400, 80, 60),
    np.random.normal(32, 9, 180)
])
flame = np.concatenate([
    np.random.normal(1000, 20, 120),
    np.random.normal(150, 60, 60),
    np.random.normal(990, 25, 180)
])
temp = np.concatenate([
    np.random.normal(24, 1, 120),
    np.random.normal(38, 4, 60),
    np.random.normal(25, 1.5, 180)
])

# ══ 三行三列子图：原始数据 + 事件标注 ══
fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# 1. 烟雾
axes[0].plot(time, smoke, color='orange', linewidth=1)
axes[0].axvspan(time[120], time[179], color='red', alpha=0.2, label='火灾事件窗口')
axes[0].axhline(150, color='blue', linestyle='--', label='阈值 S=150')
axes[0].set_ylabel('烟雾浓度')
axes[0].set_title('智安哨兵 · 传感器数据可视化')
axes[0].legend(loc='upper right')

# 2. 火焰
axes[1].plot(time, flame, color='red', linewidth=1)
axes[1].axvspan(time[120], time[179], color='red', alpha=0.2)
axes[1].axhline(510, color='blue', linestyle='--', label='阈值 F=510')
axes[1].set_ylabel('火焰强度')
axes[1].legend(loc='upper right')

# 3. 温度
axes[2].plot(time, temp, color='green', linewidth=1)
axes[2].axvspan(time[120], time[179], color='red', alpha=0.2)
axes[2].set_ylabel('温度 (°C)')
axes[2].set_xlabel('时间')
axes[2].legend(['温度', '火灾事件'])

plt.tight_layout()
plt.savefig('sensor_data_visual.png', dpi=150)
print("已保存 sensor_data_visual.png")
plt.show()