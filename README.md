
# 智安哨兵 — 智能消防预警系统
![系统架构图](images/architecture_final.png)

## 机器学习：火灾分类器决策边界
![决策边界](images/decision_boundary.png)
> 随机森林分类器 vs 硬阈值对比：模型边界能捕捉特征间的组合关系

## 传感器数据分析
![传感器数据可视化](images/sensor_data_visual.png)
> 360 组模拟数据：烟雾、火焰、温度三路信号在 10 分钟火灾事件窗口内同步跳变

## 真实数据采集与机器学习
基于 Arduino 采集的真实传感器数据（烟雾/火焰），使用随机森林训练火灾分类器。
- [数据集](data/)：正常 30 条 + 火灾事件 29 条（标签经清洗）
- [采集脚本](code/day15_collect.py)
- [分类器](code/day16_real_classifier.py)
> 历史终端输出记录：污染标签版 accuracy 为 0.83；清洗标签版固定留出测试为 18/18 命中。标签由阈值规则生成，样本为 59 条单次采集记录，结果只属于小型原型，不能写成泛化准确率。

随机森林仅用于 Python 离线训练、分类分析与验证，不参与实时报警。实时报警由 Arduino 四级状态机独立完成。

## Python 实时监控端
![仪表盘](images/dashboard_normal.png)
> tkinter 桌面应用：通过串口实时显示烟雾/火焰/温度/湿度，与 Arduino 联动报警
演示视频：[https://www.bilibili.com/video/BV1sstM6KEAL/?spm_id_from=333.1387.upload.video_card.click&vd_source=ffb1d966e4811d2e76971d9f13d774d3]

## 运行记录复核
| 测试项 | 结果 |
|---|---|
| 运行时长 | 单次连续运行约 2 小时 42 分钟（原始 CSV 可复核） |
| 误报与断线 | 项目记录未见误报、无断线；判定标准待补充，尚不代表长期部署结论 |
| 响应延迟 | 推送链路已打通；延迟统计待补 |
| 数据量 | 599 条数据行 |
| 串口日志 | 未保留 |
> ThingSpeak API 曾暴露完整 Write API Key，相关凭据已完成用户确认的轮换/作废；仓库当前不使用明文凭据。
> 设计者：李凌航 | 2026.08

## 小车入口

键盘遥控小车已拆分到独立仓库：[`000wode/keyboard-car-control`](https://github.com/000wode/keyboard-car-control)。请在新仓库查看固件、Python 上位机、接线表、依赖、运行命令和按键说明；接线信息按代码推导，硬件未复测。
