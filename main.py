# -*- coding:utf-8 -*-
# win 下运行的程序
# 程序名称: 交通信号灯数据集生成
# 程序说明：用于扩展交通信号检测数据集
# 程序文件结构说明：必须包含的三个文件
# work_dir\\before\\base(存放背景图片)
# work_dir\\before\\logo（存放logo图片，png格式，logo图片必须在logo文件夹的下级文件夹里面（自己写的遍历函数决定的））
# work_dir\\information.txt （logo编号，汉字名称，数字类别）
# 程序功能：
# 1.背景图片添加logo（合并图层）
# 2.生成所有图片的XML打标文件
# 3.生成训练和测试所需的ImageSets\\Main\\train.txt和test.txt文件（内容是图片编号，不含.jpg，如00001）
# 4.生成训练和测试所需的2018_train.txt和2018_test.txt文件（内容是存放图片的绝对路径）
# 程序时间：
# 2018年8月25日 星期六 22：30 至 01:30 实现logo沿直线生成，大小线性变化
# 2018年8月26日 星期日 09：30 至 11:20 实现三种logo的移动方式，添加logo高度和大小的随机变化，主函数的编写
# 2018年8月26日 星期日 15：00 至 16:30 实现遍历文件夹中文文件并添加logo，add_logo函数
# 2018年8月26日 星期日 20：00 至 1:30 实现edit_logo函数
# 2018年8月27日 星期一 18:00 实现xml文档的编辑并保存在xml中， txt2dict函数
# 2018年8月28日 星期二 20:00 整理好程序 主函数三行代码

import os
import make_data

# work_dir = os.getcwd()
work_dir = 'C:\\Users\\young\\Desktop\\YZN20180828'
if not os.path.exists(os.path.join(work_dir, "Annotations")):
    os.makedirs(os.path.join(work_dir, "Annotations"))
if not os.path.exists(os.path.join(work_dir, "ImageSets\\Main")):
    os.makedirs(os.path.join(work_dir, "ImageSets\\Main"))
if not os.path.exists(os.path.join(work_dir, "JPEGImages")):
    os.makedirs(os.path.join(work_dir, "JPEGImages"))

make_data.go(work_dir, loop=200)
print("程序执行完成")
