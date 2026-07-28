import numpy as np

# 模拟你的 MQ-2 传感器采集的 20 个读数（正常环境）
mq2_normal = [195, 198, 192, 200, 197, 194, 196, 201, 193, 199,
              197, 195, 198, 194, 200, 196, 193, 197, 199, 195]

# 模拟出现烟雾时的读数
mq2_smoke = [195, 196, 198, 197, 355, 480, 520, 389, 200, 198]

mu = np.mean(mq2_normal)     # 平均值
sigma = np.std(mq2_normal)   # 标准差
threshold = mu + 3 * sigma   # μ+3σ 异常阈值

print(f"基线均值 μ = {mu:.1f}")
print(f"标准差 σ = {sigma:.1f}")
print(f"异常阈值 μ+3σ = {threshold:.1f}")
print()

# 逐点检测
for i, value in enumerate(mq2_smoke):
    z_score = (value - mu) / sigma
    if value > threshold:
        print(f"  第{i+1}次 → {value} | Z={z_score:.1f} | ⚠️ 异常！")
    else:
        print(f"  第{i+1}次 → {value} | Z={z_score:.1f} | 正常")