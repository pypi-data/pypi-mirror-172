import numpy as np
import matplotlib.pyplot as plt
import math
import random
from typing import *
from IPython import display


## 函数装饰器
# numpy单个函数应用装饰器
def np_single(func):
    """
    这个装饰器允许把逻辑执行在np矩阵的每个元素中
    """
    return np.vectorize(func)


# numpy执行函数，以横向或者纵向轴的数据为维度来执行函数
def apply_func(func, data, dim = 1, **kwargs):
    """
    numpy执行函数，以横向或者纵向轴的数据为维度来执行函数
    func：参数为横向向量1xd维度的函数
    data: dim=1则data的shape为 （num, dim）, dim=0则（dim,num）
    return: list；执行结果
    """
    r = []
    if dim == 1:
        n,d = data.shape
        for i in range(n):
            x = data[i,:]
            y = func(x, kwargs)
            r.append(y)
    else:
        d,n = data.shape
        for i in range(n):
            x = data[:,i]
            y = func(x, kwargs)
            r.append(y)
    return r
