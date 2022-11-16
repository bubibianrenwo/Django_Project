import os

from django.shortcuts import render

import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render


# Create your views here.

def start(request):
    return render(request, 'index.html')


def getcom(request):
    codeareadat = open(".\stapp\static\complicate_code\Data_characterization_analyse\code", encoding="utf-8")
    codeareadata = codeareadat.read()
    return render(request, 'com.html',{"code":codeareadata})


def runcode(request):
    if request.method == "POST":
        codeareadata = request.POST['codearea']

        codeareadat = open(".\stapp\static\complicate_code\Data_characterization_analyse\code", encoding="utf-8")
        codeareadata = codeareadat.read()
        img = io.BytesIO()
        # -*- coding: utf-8 -*-
        import pandas as pd

        catering_sale = './stapp/catering_sale.xls'  # 餐饮数据
        data = pd.read_excel(catering_sale, index_col=u'日期')  # 读取数据，指定“日期”列为索引列
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        plt.figure()  # 建立图像
        p = data.boxplot(return_type='dict')  # 画箱线图，直接使用DataFrame的方法
        x = p['fliers'][0].get_xdata()  # 'flies'即为异常值的标签
        y = p['fliers'][0].get_ydata()
        y.sort()  # 从小到大排序，该方法直接改变原对象

        # 用annotate添加注释
        # 其中有些相近的点，注解会出现重叠，难以看清，需要一些技巧来控制。
        # 以下参数都是经过调试的，需要具体问题具体调试。
        for i in range(len(x)):
            if i > 0:
                plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.05 - 0.8 / (y[i] - y[i - 1]), y[i]))
            else:
                plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i] + 0.08, y[i]))
        plt.savefig(img, format='png')
        img.seek(0)
        plot_img = base64.b64encode(img.getvalue()).decode()

        # finally return and render index page and send codedata and output to show on page

    return render(request, 'com.html', {"code": codeareadata, "plot_img": plot_img})
