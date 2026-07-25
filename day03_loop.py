# 九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()

# while 循环练习：倒数
count = 10
while count > 0:
    print(f"倒计时：{count}")
    count -= 1
print("发射！")