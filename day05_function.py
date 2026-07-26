# 函数练习
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

def classify_temp(temp):
    if temp > 30:
        return "高温预警"
    elif temp > 25:
        return "偏高"
    elif temp > 15:
        return "正常"
    else:
        return "偏低"

temperatures = [10, 22, 28, 35]
for t in temperatures:
    f = celsius_to_fahrenheit(t)
    level = classify_temp(t)
    print(f"{t}°C = {f:.1f}°F → {level}")