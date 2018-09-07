# -*- coding:utf-8 -*-
# ImageDraw, ImageFont, ImageEnhance


from PIL import Image, ImageFilter, ImageEnhance
from lxml import etree as ET
from xml.dom import minidom
import os
import time
import random
import numpy


# 读取logo分类class.txt文件的每一行内容并存储到列表中， 返回列表
# 输入的是完整的路径，输出的是字典，将logo编码作为键，同一行的其他信息作为键值
def txt2dict(logo_class_path):
    dict_class = {}  # 定义一个空字典
    file = open(logo_class_path, "r", encoding="gbk", errors="ignore")  # 注意编码格式 近影响结果 print可以测试文件内容的显示效果  utf-8  gbk
    while True:
        mystr = file.readline()  # 表示一次读取一行
        if not mystr:
            break  # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
        mystr.split()
        dict_class[mystr.split()[0]] = mystr.split()[1:]
    # print(inf_dict)  # [1280, 1024, 710, 316, 31, 34]
    return dict_class


# from xml.dom import minidom
# [base_im_w, base_im_h, logo_x, logo_y, logo_size_x, logo_size_y]
# 编写xml文件，输入的数据是6个int数值，xml里面只有str类型
def edit_xml(xml_fullname, xml_filename, logo_type, xml_folder, data_mark):
    root = ET.Element("annotation")
    # root.set("version", "1.0")  # root的属性设置
    folder = ET.SubElement(root, "folder")
    folder.text = xml_folder
    filename = ET.SubElement(root, "filename")
    filename.text = xml_filename
    fullname = ET.SubElement(root, "fullname")
    fullname.text = xml_fullname
    source = ET.SubElement(root, "source")
    source.text = "201808"
    owner = ET.SubElement(root, "owner")
    owner.text = "YZN"
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(data_mark[0])
    height = ET.SubElement(size, "height")
    height.text = str(data_mark[1])
    depth = ET.SubElement(size, "depth")
    depth.text = "3"
    segmented = ET.SubElement(root, "segmented")
    segmented.text = "0"
    object = ET.SubElement(root, "object")
    name = ET.SubElement(object, "name")
    name.text = logo_type[1]  # logo_type[1]添加的是数字类别, logo_type[0]对应的是汉字类别
    meaning = ET.SubElement(object, "meaning")
    meaning.text = logo_type[0]  # logo_type[1]添加的是数字类别, logo_type[0]对应的是汉字类别
    pose = ET.SubElement(object, "pose")
    pose.text = "Unspecified"
    truncated = ET.SubElement(object, "truncated")
    truncated.text = "0"
    difficult = ET.SubElement(object, "difficult")
    difficult.text = "0"
    bndbox = ET.SubElement(object, "bndbox")
    xmin = ET.SubElement(bndbox, "xmin")
    xmin.text = str(data_mark[2])
    ymin = ET.SubElement(bndbox, "ymin")
    ymin.text = str(data_mark[3])
    xmax = ET.SubElement(bndbox, "xmax")
    xmax.text = str(data_mark[2] + data_mark[4])
    ymax = ET.SubElement(bndbox, "ymax")
    ymax.text = str(data_mark[3] + data_mark[5])
    # print(data_mark)  # [1280, 1024, 1122, 121, 94, 99]
    return root


# 添加水印函数
# base_im :打开的背景图 jpg格式
# logo_im :打开的logo图片 png格式
# k_line :需要调的参  表示logo的透视直线的斜率
# logo_im_min :需要调的参 logo像素点的大小 最远时
# logo_im_max :需要调的参 logo像素点的大小 最近时

# 给背景图片添加logo,并返回打标数据
def add_logo(base_im, logo_im, logo_start_x=0.5, logo_start_y=0.31, direction='level', k_line=0.31, logo_im_min=60,
             logo_im_max=120):
    # base_im = base_im.resize((1280, 124))  # 统一改变背景的大小
    base_im = base_im.resize((1280, 1024))
    base_im_w = base_im.size[0] - random.randint(0, 300)  # 随机改变背景图片的尺寸
    base_im_h = base_im.size[1] - random.randint(0, 200)
    # base_im = base_im.resize((base_im_w, base_im_h))  # 统一改变背景的大小
    base_im = base_im.crop((random.randint(1, 10), random.randint(1, 10), base_im_w, base_im_h))  # 裁剪图片 改变背景的内容
    base_im = base_im.resize((1280, 1024))  # 最后输出的图片大小统一成 比赛时需要的数据大小


    logo_start_x = int(logo_start_x * base_im_w)  # 需要调的参 logo预测起点的x横坐标，常数是宽度比例
    logo_start_y = int(logo_start_y * base_im_h)  # 需要调的参 logo预测起点的y纵坐标， 常数是高度比例
    if direction == 'right':
        # logo_x = random.randint(logo_start_x, base_im_w - logo_im_max + 150)  # 随机设置放置logo的x 列坐标 均匀分布的
        logo_x = random.randint(logo_start_x, base_im_w)
        logo_y = int(- k_line * (logo_x - logo_start_x) + logo_start_y)
        logo_y += int(random.uniform(-0.5, 0.5) * 200)  # 设置logo高度随机波动，这里的常数表示logo高度随机波动的像素幅度
        k_logo = (logo_im_max - logo_im_min) / (base_im_w - logo_start_x)

        logo_size = int(k_logo * (logo_x - logo_start_x)) + logo_im_min  # 根据透视规则写出来的logo图片变化规律，线性变化的，近大远小。
        logo_size += int(random.uniform(-0.5, 0.5) * 10)  # 设置logo大小随机波动， 这里的系数表示大小随机波动的logo的像素幅度
    elif direction == 'left':
        logo_x = random.randint(logo_im_max - 46, logo_start_x)  # 随机设置放置logo的x 列坐标 均匀分布的。 10 是图像显示调试出来的 不符合逻辑啊
        logo_y = int(- k_line * (logo_start_x - logo_x) + logo_start_y)
        logo_y += int(random.uniform(-0.5, 0.5) * 100)  # 设置logo高度随机波动， # 这里的系数表示高速随机波动的logo的像素幅度
        k_logo = (logo_im_max - logo_im_min) / logo_start_x

        logo_size = int(k_logo * (logo_start_x - logo_x)) + logo_im_min  # 根据透视规则写出来的logo图片变化规律，线性变化的，近大远小。
        logo_size += int(random.uniform(-0.5, 0.5) * 10)  # 设置logo大小随机波动， 这里的系数表示大小随机波动的logo的像素幅度
    else:  # direction == 'level'
        logo_x = random.randint(0, base_im_w)  # logo合成定位的横坐标区间范围
        logo_y = random.randint(50, 400)
        logo_size = random.randint(60, 120)
    if logo_x + logo_size > base_im_w:  # 超出边界就放在边界上
        logo_x = base_im_w - logo_size - random.randint(0, 20)
        print("0000000000000000000000000000000000000 logo超出右边界")
    if logo_y < 0:
        print("1111111111111111111111111111111111111 logo超出左边界")
        logo_y = 0

    logo_size_x = int(random.uniform(0.9, 1) * logo_size)  # 随机改变logo图片的宽度
    logo_size_y = logo_size
    logo_im = logo_im.resize((logo_size_x, logo_size_y))  # 随机改变logo的x宽度 最大变窄比例是0.9
    logo_im = ImageEnhance.Color(logo_im).enhance(0.6 + 0.4 * random.random())  # Adjust the saturation
    logo_im = ImageEnhance.Contrast(logo_im).enhance(0.7 + 0.3 * random.random())  # Adjust the color
    logo_im = ImageEnhance.Sharpness(logo_im).enhance(0.7 + 0.3 * random.random())  # Adjust the sharpness
    logo_im = logo_im.filter(ImageFilter.GaussianBlur(radius=1 + 0.4 * random.random()))  # 需要对logo进行模糊化处理

    base_im = ImageEnhance.Color(base_im).enhance(0.8 + 0.5 * random.random())  # Adjust the color
    base_im = ImageEnhance.Contrast(base_im).enhance(0.8 + 0.5 * random.random())  # Adjust the contrast
    base_im = ImageEnhance.Sharpness(base_im).enhance(0.8 + 0.5 * random.random())  # Adjust the sharpness

    base_im.paste(logo_im, (logo_x, logo_y), logo_im)  # (logo_x, logo_y)坐标是粘贴的坐标, 将logo图片粘贴到背景上去

    # 确定打标数据
    data_mark = [base_im_w, base_im_h, logo_x, logo_y, logo_size_x,
                 logo_size_y]  # base_im:背景尺寸，  logo_x:logo左上角的定位，logo_size:logo尺寸
    return base_im, data_mark  # 返回添加logo的图片


def go(work_dir, loop=5):
    number = 0
    save_main_dir = os.path.join(work_dir, "ImageSets\\Main")
    in_file_train = open(os.path.join(save_main_dir, "train.txt"), 'w')
    in_file_test = open(os.path.join(save_main_dir, "test.txt"), 'w')
    start = time.time()
    for k in range(loop):
        # 分别设置背景图片，logo图片，最后存储图片的文件夹 # 工作路径
        base_dir = os.path.join(work_dir, "before\\base")
        logo_dir = os.path.join(work_dir, "before\\logo")
        logo_txt_dir = os.path.join(work_dir, "before")
        save_im_dir = os.path.join(work_dir, "JPEGImages")
        save_xml_dir = os.path.join(work_dir, "Annotations")
        logo_inf_name = "information.txt"  # logo分类的文件
        logo_inf_path = os.path.join(logo_txt_dir, logo_inf_name)  # logo信息文件的完整路径
        inf_dict = txt2dict(logo_inf_path)  # logo编码后面作为字典的键。如：{'1001': ['禁止通行', '01'],
        base_list = os.listdir(base_dir)
        for base_name in base_list:
            base_name_first = os.path.splitext(base_name)[0]  # 提取背景图片的文件名（不包含后缀.jpg）
            base_im_path = os.path.join(base_dir, base_name)  # 组成完整的路径：路径加文件名
            logo_list = os.listdir(logo_dir)
            for logo_dir_list in logo_list:  # 文件夹列表
                logo_path = os.path.join(logo_dir, logo_dir_list)
                logo_list = os.listdir(logo_path)  # 文件夹下面的文件列表
                for logo_name in logo_list:  # 遍历logo图片
                    logo_im_path = os.path.join(logo_path, logo_name)
                    logo_name_first = os.path.splitext(logo_name)[0]
                    base_im = Image.open(base_im_path)  # 打开背景图片
                    logo_im = Image.open(logo_im_path)  # 打开logo图片

                    di = random.random()  # 分配三种方式数量比例
                    if di < 0.6:
                        direction = "right"
                    elif di > 0.2:
                        direction = "light"
                    else:
                        direction = "level"
                    base_im, data_mark = add_logo(base_im, logo_im, direction=direction)  # 返回图片和用于打标的数据
                    number += 1  # 用于统计生成图片的数量，即当前图片的编号
                    save_im_name = "%06d.jpg" % number  # 6位整数保存，前面用零补齐
                    save_im_path = os.path.join(save_im_dir, save_im_name)
                    base_im.save(save_im_path)  # 保存图片到指定路径
                    save_xml_name = "%06d.xml" % number  # 拼凑保存时，XML标记文件的名称

                    save_xml_path = os.path.join(save_xml_dir, save_xml_name)
                    logo_type = inf_dict[logo_name_first]  # 找到这个编号的logo对应的类型（汉字） ['旅游', '08']
                    xml_folder = os.path.split(logo_dir)[-1]  # 获取当前所在文件夹的名称
                    xml_fullname = base_name_first + '_' + logo_name_first + '.jpg'  # 拼凑保存时，图片文件的名称
                    root = edit_xml(xml_fullname, save_im_name, logo_type, xml_folder, data_mark)  # ########
                    tree = ET.ElementTree(root)
                    tree.write(save_xml_path, encoding="UTF-8", xml_declaration=True)  # 将tree内容写入save_xml_path
                    root = ET.parse(save_xml_path)  # 解析（读取）save_xml_path文件
                    file_lines = minidom.parseString(ET.tostring(root, encoding="Utf-8")).toprettyxml(
                        indent="\t")  # 转多行格式
                    file_line = open(save_xml_path, "w", encoding="utf-8")  # 打开原来的单行格式文件
                    file_line.write(file_lines)  # 将多行内容写入之前的单行文件中（单行文件内容格式化后写入的，之前内容全部消失）
                    file_line.close()
                    if random.random() < 0.7:  # 设置训练数据集的比例
                        in_file_train.write("%06d\n" % number)
                    else:
                        in_file_test.write("%06d\n" % number)
                    # print(u'已合成图片%s，已生成标记文件%s' % (save_im_name, save_xml_name))
            end = time.time()
            print(u'logo添加成功———logo添加成功———logo添加成功——————————已完成%d张,用时%d秒，平局1000张图片用时%d秒' % (
                number, (end - start), (1000 * (end - start)) / number))
    in_file_train.close()
    in_file_test.close()
