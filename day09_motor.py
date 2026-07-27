class Motor:
    def __init__(self, name):
        self.name = name
        self.speed = 0

    def set_speed(self, speed):
        speed = max(0, min(255, speed))
        self.speed = speed
        pct = int(speed / 255 * 100)
        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
        print(f"{self.name}: [{bar}] {pct}%")

motor = Motor("左轮")
motor.set_speed(0)
motor.set_speed(60)
motor.set_speed(150)
motor.set_speed(255)
motor.set_speed(300)   # 应被限制在 255