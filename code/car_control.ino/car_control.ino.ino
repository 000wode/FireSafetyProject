int IN1 = 4, IN2 = 5, IN3 = 6, IN4 = 8;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  // 左转 2 秒（右轮转、左轮停）
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);   // 左轮停
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);  // 右轮正转
  delay(2000);

  // 停
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  delay(1000);

  // 右转 2 秒（左轮转、右轮停）
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);  // 左轮正转
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);   // 右轮停
  delay(2000);

  // 停
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  delay(1000);
}