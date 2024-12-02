# Piotrowski-Kik 接触模型
Python implementation of [A simplified model of wheel--rail contact mechanics for non-Hertzian problems](http://dx.doi.org/10.1080/00423110701586444).

## 摘要
The presented model assumes semi-elliptical normal pressure distribution in the direction of rolling. The contact area is found by virtual penetration of wheel and rail. The normal pressure is calculated by satisfying contact conditions at the geometrical point of contact. The calculation is non-iterative, fast and completely reliable. It may be carried out on-line in MultiBody Systems (MBS) computer codes. The tests using the programme CONTACT by Kalker and experience from application in MBS codes show that the model is suitable for technical applications. The creep forces have been calculated with the FASTSIM algorithm, adapted for a non-elliptical contact area. Some applications in rail vehicle dynamics and wear simulation have been outlined.

本模型假设在滚动方向上的正压力分布为半椭圆形。通过车轮和轨道的虚拟穿透来确定接触区域。正压力通过满足接触点的几何接触条件来计算。该计算非迭代，快速且完全可靠。它可以在线执行在多体动力学计算机代码中。通过使用 Kalker 的 CONTACT 程序进行的测试和在 MBS 代码中的应用表明，该模型适用于技术应用。蠕滑力已经使用为非椭圆形接触区域适配的 FASTSIM 算法进行了计算。还概述了在轨道车辆动力学和磨耗模拟中的一些应用。

## 关键词
Rail; Wheel; Contact problems; Dynamics;Wear; Simulation

## 模型简介
Semi-Hertzian (semi-elliptical normal pressure distribution along the (rolling) x-axis) non-iterative contact solution that is particularly usefull when curvatures are not constant along the (lateral) y-axis. Results shown in the original article are in agreement with results from Kalker's variational method. However, alike Kalker's method the model is limited to elastic material response and geometries that permit the assumption of an infinite half-space. Additionally, both bodies have to possess identical material properties.

## 核心特征
(1) 半赫兹接触模型
(2) 沿滚动方向(x轴)的半椭圆形法向压力分布
(3) 非迭代求解方法
(4) 特别适用于沿横向(y轴)曲率非恒定的情况

## 模型限制
(1) 仅适用于弹性材料响应
(2) 几何形状必须满足半无限空间假设
(3) 两个接触体必须具有相同的材料特性

## 如何使用
0. 安装：NumPy、SciPy、Matplotlib (for visualisation only)
1. Place files defining geometry of the profiles in *profiles* directory.
2. In `pkmodel.py`, specify path to the profiles or call functions from `./lib/geometry.py` to work with analytical geometries.
3. Set simulation parameters in `settings.py`.
4. Run `pkmodel.py`.

## 特别地
对于 Piotrowski-Kik contact model 补充了可视化的部分。包括：绘制轮轨轮廓、可视化嵌入量、可视化压力分布
