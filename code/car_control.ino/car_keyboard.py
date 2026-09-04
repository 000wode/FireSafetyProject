# 键盘遥控小车
import serial
import time
from pynput import keyboard

ser = serial.Serial('COM3', 9600)
time.sleep(2)

print("🎮 键盘遥控小车")
print("W=前进 S=后退 A=左转 D=右转 X=停止")
print("按 Esc 退出")
print("(松开按键 = 停止)")

current = 'x'

def on_press(key):
    global current
    try:
        if key == keyboard.Key.esc:
            return False
        if hasattr(key, 'char') and key.char:
            c = key.char.lower()
            if c in 'wasdx' and c != current:
                current = c
                ser.write(c.encode())
                print(f"▶ 发送: {c.upper()}")
    except Exception as e:
        print(e)

def on_release(key):
    global current
    try:
        if hasattr(key, 'char') and key.char:
            c = key.char.lower()
            if c == current and c in 'wasd':
                ser.write(b'x')
                current = 'x'
    except Exception:
        pass

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()

ser.close()
print("退出")