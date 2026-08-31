# 智安哨兵 - 桌面监控仪表盘（实时版）
import tkinter as tk
from tkinter import font
import serial
import time

# ══ 串口连接 ══
PORT = 'COM3'
BAUD = 9600
ser = None

def connect_serial():
    global ser
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        print(f"已连接 {PORT}")
        return True
    except Exception as e:
        print(f"串口连接失败: {e}")
        return False

# ── 创建主窗口 ──
root = tk.Tk()
root.title("智安哨兵 - 智能消防监控系统")
root.geometry("500x450")
root.configure(bg="#1e1e2e")

big_font = font.Font(family="Arial", size=24, weight="bold")
label_font = font.Font(family="Arial", size=14)
status_font = font.Font(family="Arial", size=18, weight="bold")

title = tk.Label(root, text="🔥 智安哨兵", bg="#1e1e2e", fg="#ffffff",
                 font=font.Font(family="Arial", size=28, weight="bold"))
title.pack(pady=20)

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

status_label = tk.Label(root, text="🔄 连接中...", bg="#1e1e2e", fg="#89b4fa",
                        font=status_font)
status_label.pack(pady=10)

# 连接提示
conn_label = tk.Label(root, text="", bg="#1e1e2e", fg="#f38ba8",
                      font=font.Font(family="Arial", size=11))
conn_label.pack()

# ══ 实时读取 ══
def read_serial():
    """从串口读取 Arduino 数据并刷新界面"""
    global ser

    if ser is None:
        if connect_serial():
            status_label.config(text="🟢 已连接", fg="#a6e3a1")
        else:
            status_label.config(text="❌ 串口未连接", fg="#f38ba8")
            conn_label.config(text=f"请确认 Arduino 已连接 {PORT}，并关闭 Arduino IDE")
            root.after(3000, read_serial)
            return

    try:
        line = ser.readline().decode().strip()
        if line and not line.startswith(('time', '预热', '开始')):
            parts = line.split(',')
            if len(parts) >= 5:
                t, s, f, temp, hum = parts[0], parts[1], parts[2], parts[3], parts[4]

                s_int = int(s)
                f_int = int(f)

                smoke_value.config(text=f"{s}")
                flame_value.config(text=f"{f}")
                temp_value.config(text=f"{float(temp):.1f}")
                hum_value.config(text=f"{float(hum):.0f}")

                # 状态判断（与 Arduino 融合算法一致）
                if f_int < 400 or s_int > 500:
                    status_label.config(text="🔴 报警！", fg="#f38ba8")
                elif s_int > 200 or f_int < 700:
                    status_label.config(text="🟠 预警", fg="#fab387")
                else:
                    status_label.config(text="🟢 正常", fg="#a6e3a1")
    except Exception as e:
        pass   # 读不到数据先跳过，下秒再试

    root.after(1000, read_serial)

read_serial()

# 关闭时断开串口
def on_close():
    if ser:
        ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()