int IN1 = 4, IN2 = 5, IN3 = 6, IN4 = 8;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  Serial.begin(9600);
  Serial.println("小车遥控就绪!");
  Serial.println("W=前进 S=后退 A=左转 D=右转 X=停止");
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();   // 读一个字符

    switch (cmd) {
      case 'W': case 'w':
        forward();
        Serial.println("前进");
        break;
      case 'S': case 's':
        backward();
        Serial.println("后退");
        break;
      case 'A': case 'a':
        turnLeft();
        Serial.println("左转");
        break;
      case 'D': case 'd':
        turnRight();
        Serial.println("右转");
        break;
      case 'X': case 'x':
        stopCar();
        Serial.println("停止");
        break;
    }
  }
}

void forward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void backward() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}

void turnLeft() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void turnRight() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}

void stopCar() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}