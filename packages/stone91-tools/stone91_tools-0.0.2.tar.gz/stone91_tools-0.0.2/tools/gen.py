import numpy as np
import matplotlib.pyplot as plt
import math
import random
from typing import *
from IPython import display


# 按照概率分布函数生成制定数目的数据
def gen_data_by_pdf(func:Callable, num:int, dim:int, is_np = 0):
    """
    desc:按照概率分布函数生成特定数目的数据。
         采用蒙特卡洛法，运行速度缓慢。
    func: pdf函数，用于生成样本点
    num: 生成样本的个数
    dim: 样本数字的维度,int
    is_np: 是否返回np数组，默认为list
    """
    li = []
    for i in range(num):
        r = [(random.random()-0.5)*2**30 for i in range(dim)]
        while random.random()>func(r):
            r = [(random.random()-0.5)*2**30 for i in range(dim)]
        li.append(tuple(r))
    if is_np:
        return np.array(li)
    return li

# 按照概率分布画图
def draw_distribution_2d(list_pdf:List[Callable], labels:List[str] = None, title:str = '', sample_num:int = 100):
    """
    按照蒙特卡洛方法从pdf生成样本点
    然后按照样本点绘图.
    仅限2d
    list_pdf: [pdf1,pdf2,pdf3]
               pdf 负责接收k维度输入，返回一个值；
    """
    if not labels:
        labels = ['' for i in range(len(list_pdf))]
    for i in range(len(list_pdf)):
        pdf = list_pdf[i]
        ## 按照估计出的分布生成随机数据
        samples = gen_data_by_pdf(pdf, sample_num, dim=2, is_np = 1)
        ## 把随机数据变成对应网格；然后按照对应高斯分布生成100x100的z矩阵
        X, Y = np.meshgrid(samples[:,0], samples[:,1])
        d = np.dstack([X,Y])
        Z = np.array(apply_func(pdf(d),dim=1)).reshape(samples.shape[0],samples.shape[0])
        ## 绘制两个分布的热力图，mixed数据的整体散点图
        plt.contour(X, Y, Z,  alpha =0.3, zorder=10, label=labels[i]);
    plt.legend()
    plt.title(title)
