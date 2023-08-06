import numpy as np
import matplotlib.pyplot as plt
import math
import random
from IPython import display


# 让图变成动图
def anime_show(time = 0.1):
    """
    让图变成动图
    time: 动图停留时间
    """
    plt.show()
    plt.pause(time)#每次显示图片的暂停时间
    display.clear_output(wait=True)#每次显示完图以后删除，达到显示动图的效果
    

## 机器学习
# 对数据画折线图
def plot_loss(data_list, label = [], title='', color='rgbcmyk', log = 0):
    """
    对数据画折线图
    data_list = [data1, data2]
    label = ['class1_name', 'class2_name']
    log: 是否取对数纵轴
    data.shape = [num, dim],dim=2
    """
    batch_n = len(data_list)
    if log:
        plt.yscale('log')
    for i in range(batch_n):
        plt.plot([i for i in range(len(data_list[i]))], [each for each in data_list[i]], c=color[i], label=label[i])
    plt.legend()
    plt.title(title)
    return plt


# 对2d数据画散点图
def scatter(data_list, label = [], title='', color='rgbcmyk'):
    """
    data_list = [data1, data2]
    label = ['class1_name', 'class2_name']
    data.shape = [num, dim],dim=2
    """
    batch_n = len(data_list)
    for i in range(batch_n):
        plt.scatter([each[0] for each in data_list[i]], [each[1] for each in data_list[i]], c=color[i], label=label[i])
    plt.legend()
    plt.title(title)
    return plt


# 画2d直线
def line(x_interval:tuple, func_list:List[Callable], label = [], title='', color='rgbcmyk'):
    """
    画2d直线
    x_interval:(0,10)开始和结束区间
    func_list：[lambda x： x^2,lambda x： x^3]
    label = ['1','2']
    """
    batch_n = len(func_list)
    x = np.linspace(x_interval[0], x_interval[1])
    for i in range(batch_n):
        plt.plot(x, func_list[i](x), c=color[i], label=label[i])
    plt.legend()
    plt.title(title)
    return plt


## 数字图像处理
# 对多个图像画统计直方图
def plot_pixel_sum(data_list, bins = 255, label = [], title='', color='rgbcmyk', sep = False):
    """
    data_list = [np.img, np.img]
    label = ['img_name', 'img_name']
    sep: 分开画图还是合并
    """
    batch_n = len(data_list)
    if not sep:
        for i in range(batch_n):
            plt.hist(data_list[i].ravel(), 
                     bins = bins, alpha = 0.5, range=(0, 255), 
                     weights = np.ones_like(data_list[i].ravel())/len(data_list[i].ravel()),
                     color=color[i], label=label[i])
        plt.xlabel('Gray value') 
        plt.ylabel('pixel percentage') 
        plt.legend()
        plt.title(title)
    else:
        for i in range(batch_n):
            plt.hist(data_list[i].ravel(), 
                     bins = bins, alpha = 0.5, range=(0, 255), 
                     weights = np.ones_like(data_list[i].ravel())/len(data_list[i].ravel()),
                     color=color[i], label=label[i])
            plt.xlabel('Gray value') 
            plt.legend()
            plt.title('{}:{}'.format(title,label[i]))
            plt.ylabel('pixel percentage') 
            plt.show()
    #plot_pixel_sum([house, lena,rose], label=['house','lena','rose'],title='2pics', sep=1)                                     
    return plt
    