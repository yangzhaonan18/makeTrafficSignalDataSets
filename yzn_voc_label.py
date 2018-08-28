# -*- coding:utf-8 -*-

# ubuntu 下是用的程序
# 程序名称：数据集格式转换
# 程序功能：XML文件的点坐标格式，转换成TXT文件的比例坐标格式
# 程序说明：
# 1.需要数据：
# Annotations 文件夹下的XML文件（存放的所有图片的XML打标数据 如：<object> </object>）
# ImageSets\\Main 文件夹下存放的train.txt和test.txt文件（分别存放用于测试和训练的图片编号，即不含后缀名的图片名称）
# 2.产生数据：
# label文件下的TXT文件，存放所有图片的打标数据 如：6 0.097 0.8288177339901478 0.14200000000000002 0.12561576354679804
# 生成2018_train.txt和2018_test.txt文件，存放训练和测试图片的绝对路径，如H:\YOLOV3\darknet-master\build\darknet\x64\data\voc/VOCdevkit/VOC2007/JPEGImages/000001.jpg
# 程序时间：2018年08月28日14:30开始 19:10开始
import xml.etree.ElementTree as ET
import os

classes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
           "20"]  # 类的名称是我们感兴趣的目标对象的名称 如：这里用数字表示，通常填写 bird,car, person之类的词
sets = ["train", "test"]  # 数据


def convert(size, box):  # 内容转换（XML的点坐标格式，转换成YOLO的比例坐标格式）
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(work_dir, image_id):
    in_file = open(os.path.join(work_dir, "Annotations\\%s.xml" % image_id), 'rb')
    out_file = open(os.path.join(work_dir, "labels\\%s.txt" % image_id), "w")  # 所有的YOLO打标数据都放在这里
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')  # 读取背景图片的尺寸
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):  # 遍历每一个对象（打了标记的目标）
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue  # 跳过“难”的和 不在classes列表中的对象（已经打了标记但不需要的对象）
        cls_id = classes.index(cls)  # 获取当前图片中的标记对象在classes列表中的序号
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))  # 目标对象信息存放在一个元组中，（元组的特点是不可改变）
        bb = convert((w, h), b)  # 返回的也是一个元组格式
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')  # 将转换后的内容按行存放到指定文件中


for image_set in sets:
    # work_dir = os.getcwd()  # 运行前这里要修改成自己的目录
    work_dir = 'C:\\Users\\young\\Desktop\\YZN20180828'
    if not os.path.exists(os.path.join(work_dir, "labels")):
        os.makedirs(os.path.join(work_dir, "labels"))  # 新建一个label文件夹。用于存放标记文件txt
    image_ids = open(os.path.join(work_dir, "ImageSets\\Main\\%s.txt" % image_set)).read().strip().split()  # 读取编号
    list_file = open(os.path.join(work_dir, "%s.txt" % image_set), 'w')  # train.txt,存放完整路径
    for image_id in image_ids:
        list_file.write("%s" % os.path.join(work_dir, "JPEGImages\\%s.jpg\n" % image_id))  # 存放训练图片的 完整路径
        convert_annotation(work_dir, image_id)
    list_file.close()
