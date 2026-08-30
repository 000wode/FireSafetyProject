# 火灾分类器决策边界可视化
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 重新生成数据（和 Day 11 一样）
np.random.seed(42)

normal_s = np.random.normal(30, 10, 200)
normal_f = np.random.normal(1000, 30, 200)
normal_t = np.random.normal(24, 2, 200)

fire_s = np.random.normal(500, 100, 200)
fire_f = np.random.normal(50, 20, 200)
fire_t = np.random.normal(45, 5, 200)

X = np.vstack([
    np.column_stack([normal_s, normal_f, normal_t]),
    np.column_stack([fire_s, fire_f, fire_t])
])
y = np.array([0] * 200 + [1] * 200)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ══ 画决策边界：横轴=烟雾，纵轴=火焰（固定温度在典型值）══
x_min, x_max = 0, 700       # 烟雾范围
y_min, y_max = 0, 1100      # 火焰范围
step = 10

xx, yy = np.meshgrid(
    np.arange(x_min, x_max, step),
    np.arange(y_min, y_max, step)
)

# 温度固定为 30°C（中性值），在网格每个点上预测
grid = np.column_stack([xx.ravel(), yy.ravel(), np.full(xx.size, 30.0)])
probs = model.predict_proba(grid)[:, 1]     # 火灾概率
probs = probs.reshape(xx.shape)

# ══ 绘图 ══
plt.figure(figsize=(12, 8))

# 背景：概率热力图
contour = plt.contourf(xx, yy, probs, levels=20, cmap='RdYlGn_r', alpha=0.85)
plt.colorbar(contour, label='火灾概率')

# 样本点
plt.scatter(X[y == 0, 0], X[y == 0, 1], c='green', label='正常', s=20, alpha=0.6)
plt.scatter(X[y == 1, 0], X[y == 1, 1], c='red', label='火灾', s=20, alpha=0.6)

# 你系统的硬阈值线（对比用）
plt.axvline(150, color='blue', linestyle='--', linewidth=2, label='烟雾阈值 S=150')
plt.axhline(510, color='purple', linestyle='--', linewidth=2, label='火焰阈值 F=510')

plt.xlabel('烟雾浓度 S（MQ-2 读数）')
plt.ylabel('火焰强度 F（火焰传感器读数）')
plt.title('智安哨兵：火灾分类器决策边界（温度固定 30°C）\n绿=正常区 红=火灾区 蓝虚线=你的硬阈值')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('decision_boundary.png', dpi=150)
print("已保存 decision_boundary.png")
plt.show()