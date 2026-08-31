// ═══════════════════════════════════════════════════
//  智安哨兵 v1.0 — 智能消防预警系统
//  多传感器融合 + 自适应阈值 + 四级状态机 + 喷淋联动
//  继电器为低电平触发（IO2 碰 GND 吸合）
//  设计者：李凌航 | 2026
// ═══════════════════════════════════════════════════
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ── 引脚分配 ──
int mq2Pin = A2;
int flamePin = A3;
int buzzer = 9;
int ledPin = 11;
int relayPin = 8;

// ── 融合权重 ──
float wSmoke = 0.4;
float wFlame = 0.4;
float wTemp  = 0.2;
float tempThreshold = 34.0;

// ── 动态阈值 ──
int smokeThreshold = 150;
int flameThreshold = 600;

// ── 状态机 ──
enum State { NORMAL, CAUTION, ALERT, FIRE };
State currentState = NORMAL;

unsigned long lastBlink = 0;
int blinkInterval = 0;
bool ledOn = false;

void setup() {
  pinMode(buzzer, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);     // 低电平触发：默认 HIGH = 继电器断开

  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
  dht.begin();

  lcd.setCursor(0, 0);
  lcd.print("Warming Up...");
  Serial.println("MQ-2 预热 60 秒...");
  delay(60000);

  calibrate();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Calibrated!");
  Serial.println("校准完成，进入监测");
  delay(1500);
  lcd.clear();
}

void calibrate() {
  const int samples = 20;
  long sumS = 0, sumF = 0;
  long sumSqS = 0, sumSqF = 0;

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Calibrating...");
  Serial.println("开始采集基线样本...");

  for (int i = 0; i < samples; i++) {
    int s = analogRead(mq2Pin);
    int f = analogRead(flamePin);

    sumS += s;              sumF += f;
    sumSqS += (long)s * s;  sumSqF += (long)f * f;

    Serial.print("样本");
    Serial.print(i + 1);
    Serial.print(": S=");
    Serial.print(s);
    Serial.print(" F=");
    Serial.println(f);

    delay(500);
  }

  float muS = sumS / (float)samples;
  float muF = sumF / (float)samples;

  float varS = (sumSqS / (float)samples) - muS * muS;
  float varF = (sumSqF / (float)samples) - muF * muF;
  if (varS < 0) varS = 0;
  if (varF < 0) varF = 0;
  float sigmaS = sqrt(varS);
  float sigmaF = sqrt(varF);

  smokeThreshold = (int)(muS + 3 * sigmaS);
  flameThreshold = (int)(muF * 0.5);

  if (smokeThreshold < 100) smokeThreshold = 100;
  if (flameThreshold > 800) flameThreshold = 800;
  if (flameThreshold < 100) flameThreshold = 100;

  Serial.println("──────────────");
  Serial.print("烟雾基线 μ=");
  Serial.print(muS, 1);
  Serial.print(" σ=");
  Serial.print(sigmaS, 1);
  Serial.print(" → 阈值=");
  Serial.println(smokeThreshold);
  Serial.print("火焰基线 μ=");
  Serial.print(muF, 1);
  Serial.print(" → 阈值=");
  Serial.println(flameThreshold);
  Serial.println("──────────────");
}

void loop() {
  int smoke = analogRead(mq2Pin);
  int flame = analogRead(flamePin);
  float temp = dht.readTemperature();

  float sScore = constrain((smoke - smokeThreshold) / 500.0, 0, 1) * wSmoke;
  float fScore = constrain((flameThreshold - flame) / 400.0, 0, 1) * wFlame;
  float tScore = constrain((temp - tempThreshold) / 10.0, 0, 1) * wTemp;
  float totalScore = sScore + fScore + tScore;

  // ── 状态转移 + 水泵控制（低电平触发）──
  if (totalScore >= 0.6) {
    currentState = FIRE;
    blinkInterval = 125;
    digitalWrite(relayPin, LOW);      // 💦 低电平 = 继电器吸合 = 喷水
    lcd.setCursor(0, 1);
    lcd.print("FIRE!       ");
    Serial.print("🔴 报警! score=");
  } else if (totalScore >= 0.4) {
    currentState = ALERT;
    blinkInterval = 333;
    digitalWrite(relayPin, HIGH);     // 断开
    lcd.setCursor(0, 1);
    lcd.print("Alert!      ");
    Serial.print("🟠 预警 score=");
  } else if (totalScore >= 0.2) {
    currentState = CAUTION;
    blinkInterval = 1000;
    digitalWrite(relayPin, HIGH);
    lcd.setCursor(0, 1);
    lcd.print("Caution     ");
    Serial.print("🟡 关注 score=");
  } else {
    currentState = NORMAL;
    digitalWrite(relayPin, HIGH);     // 断开
    digitalWrite(ledPin, LOW);
    noTone(buzzer);
    lcd.setCursor(0, 1);
    lcd.print("Normal      ");
    Serial.print("🟢 正常 score=");
  }
  Serial.println(totalScore, 2);

  // ── 非阻塞 LED 闪烁 + 蜂鸣器 ──
  if (currentState != NORMAL) {
    unsigned long now = millis();
    if (now - lastBlink >= blinkInterval) {
      lastBlink = now;
      ledOn = !ledOn;
      digitalWrite(ledPin, ledOn);

      if (currentState == FIRE) {
        tone(buzzer, 1200, 100);
        delay(50);
        tone(buzzer, 600, 100);
      } else if (currentState == ALERT) {
        tone(buzzer, 800, 50);
      } else if (currentState == CAUTION) {
        tone(buzzer, 400, 30);
      }
    }
  }

  // ── LCD 第一行 ──
  lcd.setCursor(0, 0);
  lcd.print("S:");
  lcd.print(smoke);
  lcd.print(" F:");
  lcd.print(flame);
  lcd.print(" T:");
  lcd.print((int)temp);
  lcd.print("   ");

  delay(50);
}