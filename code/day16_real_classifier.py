# 用真实传感器数据训练火灾分类器（v2：清洗标签）
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

normal = pd.read_csv('real_sensor_data.csv')
fire = pd.read_csv('real_sensor_data_fire.csv')

# ══ 关键修复：重新定义标签 ══
# 火灾 = 烟雾明显超标(S>100) 或 火焰骤降(F<600)
# fire.csv 里前 6 秒的正常段（S=36）会正确标回 0
fire['label'] = ((fire['smoke'] > 100) | (fire['flame'] < 600)).astype(int)
normal['label'] = 0

print("清洗后标签分布:")
print(f"  正常: {len(normal)} 条 (全部标0)")
print(f"  事件文件: {fire['label'].value_counts().to_dict()}")

data = pd.concat([normal, fire], ignore_index=True)

features = ['smoke', 'flame']
X = data[features].values
y = data['label'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"\n测试集准确率: {accuracy_score(y_test, y_pred) * 100:.1f}%")
print("\n详细报告:")
print(classification_report(y_test, y_pred, target_names=['正常', '火灾'], zero_division=0))

print("特征重要性:")
for name, imp in zip(features, model.feature_importances_):
    print(f"  {name}: {imp:.3f}")

print("\n测试实时数据:")
samples = [
    [36, 1020],
    [752, 1020],
    [698, 119],
]
for s in samples:
    prob = model.predict_proba([s])[0]
    pred = "🔥 火灾" if model.predict([s])[0] == 1 else "✅ 正常"
    print(f"  S={s[0]} F={s[1]} → {pred} (火灾概率 {prob[1]*100:.1f}%)")