# 用模拟传感器数据训练火灾分类器
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# 生成模拟数据：烟雾, 火焰, 温度, 湿度 → 标签(0正常/1火灾)
np.random.seed(42)

# 正常数据：三个特征都在正常范围
normal_s = np.random.normal(30, 10, 200)     # 烟雾 30±10
normal_f = np.random.normal(1000, 30, 200)   # 火焰 1000±30
normal_t = np.random.normal(24, 2, 200)      # 温度 24±2

# 火灾数据：特征异常
fire_s = np.random.normal(500, 100, 200)     # 烟雾高
fire_f = np.random.normal(50, 20, 200)       # 火焰低
fire_t = np.random.normal(45, 5, 200)        # 温度高

X_normal = np.column_stack([normal_s, normal_f, normal_t])
X_fire = np.column_stack([fire_s, fire_f, fire_t])

X = np.vstack([X_normal, X_fire])
y = np.array([0] * 200 + [1] * 200)  # 0=正常, 1=火灾

# 划分训练/测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 训练随机森林分类器
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 评估
y_pred = model.predict(X_test)
print(f"测试集准确率: {accuracy_score(y_test, y_pred) * 100:.1f}%")

# 看看模型怎么判断一个新样本
new_samples = np.array([
    [35, 990, 24.5],    # 应该预测 0（正常）
    [520, 45, 42.0],    # 应该预测 1（火灾）
    [200, 700, 28.0],   # 中间状态
])

for sample in new_samples:
    s, f, t = sample
    pred = model.predict([sample])[0]
    prob = model.predict_proba([sample])[0]
    result = "🔥 火灾" if pred == 1 else "✅ 正常"
    print(f"S={s:.0f} F={f:.0f} T={t:.1f} → {result} (火灾概率 {prob[1]*100:.1f}%)")