"""Implementation of Piotrowski-Kik contact model.

Details and references about the model can be found in README.

In the following code the adopted naming convention is the one of
`PEP 8 <https://www.python.org/dev/peps/pep-0008/#naming-conventions>`_
with the exception that the function and method names are mixedCase. 

.. module:: pkmodel

.. moduleauthor:: Rostyslav Skrypnyk
"""

# Standard library imports:
import os
import sys
sys.path.insert(0, os.path.abspath('./lib')) # Add lib to path.
# 3rd party imports:
import numpy as np
# local library specific imports:
import settings as s
import pkmodellib as pkl
import geometry as geom
import matplotlib.pyplot as plt
import scipy.integrate as spint

def visualizePressureDistribution(wheel, interpen, radius, E, nu, delta, delta0):
    # 获取 Y 坐标
    y_array = wheel[:, 0]
    
    # 识别正嵌入量的区域
    region_array = pkl.nonzeroRuns(interpen)
    
    # 初始化压力数组
    pressures = np.zeros_like(y_array)
    
    # 计算每个接触区域的压力分布
    for region in region_array:
        ind_l, ind_u = region[0], region[1]
        # 获取该区域的嵌入量
        g_region = interpen[ind_l:ind_u]
        y_region = y_array[ind_l:ind_u]
        
        # 计算最大压力
        pmax = pkl.maxPressure(wheel[ind_l:ind_u], g_region, radius, E, nu, delta, delta0)
        pmax = pmax[0]  # 由于每个区域只有一个 pmax 值
        
        # 假设压力分布为半椭圆分布
        # 计算归一化位置
        y_center = np.mean(y_region)
        a = (y_region[-1] - y_region[0]) / 2  # 接触半宽度
        xi = (y_region - y_center) / a  # 归一化到 [-1, 1]
        
        # 计算压力分布
        pressures[ind_l:ind_u] = pmax * np.sqrt(1 - (xi)**2)
    # 绘制压力分布
    plt.figure()
    plt.plot(y_array, pressures, label='Pressure Distribution')
    plt.xlabel('Y (mm)')
    plt.ylabel('Pressure [MPa]')
    plt.title('Pressure Distribution')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    rail, wheel = pkl.getProfiles(s.rail_path, s.wheel_path)
    new_wheel = pkl.equalPoints(wheel, rail)

    interpen = pkl.interpenetration(new_wheel, rail,
                                    s.virtual_penetration)
    max_pressures = pkl.maxPressure(new_wheel, interpen,
                                    s.wheel_radius, s.E, s.nu,
                                    s.penetration, s.virtual_penetration)
    print (max_pressures)
# End of function main.

# 后处理1：绘制轮轨轮廓
    pkl.plotProfiles(rail, wheel)

# 后处理2：可视化嵌入量
    # 绘制嵌入量
    plt.figure()
    plt.plot(new_wheel[:, 0], interpen, label='Penetration')
    plt.xlabel('Y (mm)')
    plt.ylabel('Penetration')
    plt.title('Inter Penetration')
    plt.legend()
    plt.grid(True)
    plt.show()

# 后处理3：可视化压力分布
    visualizePressureDistribution(new_wheel, interpen, s.wheel_radius, s.E, s.nu,
                                  s.penetration, s.virtual_penetration)


# Make sure main() does not run when the file is being imported:
if __name__ == '__main__':
    main()

