# 智安哨兵 - 桌面监控仪表盘（静态版）
import tkinter as tk
from tkinter import font

# ── 创建主窗口 ──
root = tk.Tk()
root.title("智安哨兵 - 智能消防监控系统")
root.geometry("500x400")
root.configure(bg="#1e1e2e")

# ── 字体 ──
big_font = font.Font(family="Arial", size=24, weight="bold")
label_font = font.Font(family="Arial", size=14)
status_font = font.Font(family="Arial", size=18, weight="bold")

# ── 标题 ──
title = tk.Label(root, text="🔥 智安哨兵", bg="#1e1e2e", fg="#ffffff",
                 font=font.Font(family="Arial", size=28, weight="bold"))
title.pack(pady=20)

# ── 数据帧（四个数值卡片）──
data_frame = tk.Frame(root, bg="#1e1e2e")
data_frame.pack(pady=10)

def make_card(parent, label, row, col):
    card = tk.Frame(parent, bg="#313244", padx=20, pady=15, relief="ridge", bd=2)
    card.grid(row=row, column=col, padx=10, pady=10)
    tk.Label(card, text=label, bg="#313244", fg="#a6adc8",
             font=label_font).pack()
    value_label = tk.Label(card, text="---", bg="#313244", fg="#89b4fa",
                           font=big_font)
    value_label.pack()
    return value_label

smoke_value = make_card(data_frame, "烟雾浓度", 0, 0)
flame_value = make_card(data_frame, "火焰强度", 0, 1)
temp_value  = make_card(data_frame, "温度 (°C)", 1, 0)
hum_value   = make_card(data_frame, "湿度 (%)", 1, 1)

# ── 状态显示 ──
status_label = tk.Label(root, text="🟢 正常", bg="#1e1e2e", fg="#a6e3a1",
                        font=status_font)
status_label.pack(pady=10)

# ── 模拟数据更新 ──
import random

def update_mock():
    """用模拟数据刷新界面（Day 18 换成真实串口数据）"""
    s = random.randint(25, 50)
    f = random.randint(980, 1023)
    t = random.uniform(23, 26)
    h = random.randint(55, 65)

    smoke_value.config(text=f"{s}")
    flame_value.config(text=f"{f}")
    temp_value.config(text=f"{t:.1f}")
    hum_value.config(text=f"{h}")

    # 状态逻辑（和 Arduino 一致）
    if s > 500 or f < 400:
        status_label.config(text="🔴 报警！", fg="#f38ba8")
    elif s > 200 or f < 700:
        status_label.config(text="🟠 预警", fg="#fab387")
    else:
        status_label.config(text="🟢 正常", fg="#a6e3a1")

    root.after(1000, update_mock)   # 每秒刷新

update_mock()

# ── 运行 ──
root.mainloop()