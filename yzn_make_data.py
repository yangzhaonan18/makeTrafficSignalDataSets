# -*- coding:utf-8 -*-
# ImageDraw, ImageFont, ImageEnhance


from PIL import Image, ImageFilter, ImageEnhance
from lxml import etree as ET
from xml.dom import minidom
import os
import time
import random


def get_logo_name_dict(logo_dir):  # 输入的是存放logo 的文件夹
    logo_list = os.listdir(logo_dir)
    logo_name_dict = {}
    for i in range(len(logo_list)):  # 遍历文件夹下面的文件夹
        path = os.path.join(logo_dir, logo_list[i])  # 获取文件夹的绝对路径
        path_list = os.listdir(path)  # 获取文件夹下的文件列表
        for j in range(len(path_list)):  # 去掉文件名中的后缀，只提取前面的四位编码  遍历文件夹下面的文件夹下的文件
            # index = path_list[j].rfind('.')
            # logo_name_dict[path_list[j][:index]] = logo_list[i]
            logo_name_dict[path_list[j]] = logo_list[i]

    # print(logo_name_dict)
    # print(sorted(logo_name_dict.items()))
    return logo_name_dict  # 返回logo文件名列表，不包含.后缀


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
def edit_xml(xml_fullname, xml_filename, xml_folder, data_mark):
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
    width.text = str(1280)  # str(data_mark[0][0])
    height = ET.SubElement(size, "height")
    height.text = str(1024)  # str(data_mark[0][1])
    depth = ET.SubElement(size, "depth")
    depth.text = "3"
    segmented = ET.SubElement(root, "segmented")
    segmented.text = "0"
    for i in range(len(data_mark) - 1):
        object = ET.SubElement(root, "object")
        name = ET.SubElement(object, "name")
        name.text = data_mark[i + 1][0][1]  # logo_type[1]添加的是数字类别, logo_type[0]对应的是数字类别
        meaning = ET.SubElement(object, "meaning")
        meaning.text = data_mark[i + 1][0][0]  # logo_type[0]添加的是数字类别, logo_type[0]对应的是汉字类别
        pose = ET.SubElement(object, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(object, "truncated")
        truncated.text = "0"
        difficult = ET.SubElement(object, "difficult")
        difficult.text = "0"
        bndbox = ET.SubElement(object, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(data_mark[i + 1][1])
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(data_mark[i + 1][2])
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(data_mark[i + 1][1] + data_mark[i + 1][3])
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(data_mark[i + 1][2] + data_mark[i + 1][4])

    return root


# 添加水印函数
# base_im :打开的背景图 jpg格式
# logo_im :打开的logo图片 png格式
# k_line :需要调的参  表示logo的透视直线的斜率
# logo_im_min :需要调的参 logo像素点的大小 最远时
# logo_im_max :需要调的参 logo像素点的大小 最近时

def resize_light(light_im):  # 将light统一最窄宽度# 对light_im 进行处理
    light_min = 13 + random.randint(5, 15)
    if (light_im.size[1] < light_im.size[0]):
        light_im = light_im.resize((int(light_min * light_im.size[0] / light_im.size[1]), light_min))
    else:
        light_im = light_im.resize((light_min, int(light_min * light_im.size[1] / light_im.size[0])))

    return light_im


# 给背景图片添加logo,并返回打标数据
def add_logo(base_im, logo_im, light0_im, light1_im, logo_start_x=0.5, logo_start_y=0.31, direction='level',
             k_line=0.31,
             logo_im_min=40,
             logo_im_max=120):
    light0_im = resize_light(light0_im)
    light1_im = resize_light(light1_im)
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
        logo_x = random.randint(0, base_im_w - logo_im.size[0])  # logo合成定位的横坐标区间范围
        logo_y = random.randint(100, 450)
        logo_size = random.randint(40, 120)

    if logo_x + logo_size > base_im_w:  # 超出边界就放在边界上
        logo_x = base_im_w - logo_size - random.randint(0, 20)
        print("0000000000000000000000000000000000000 logo超出右边界")
    if logo_y < 0:
        print("1111111111111111111111111111111111111 logo超出左边界")
        logo_y = 0

    logo_size_x = int(random.uniform(0.9, 1) * logo_size)  # 随机改变logo图片的宽度
    logo_size_y = logo_size
    logo_im = logo_im.resize((logo_size_x, logo_size_y))  # 随机改变logo的x宽度 最大变窄比例是0.9
    logo_im = ImageEnhance.Color(logo_im).enhance(0.8 + 0.6 * random.random())  # Adjust the saturation
    logo_im = ImageEnhance.Contrast(logo_im).enhance(0.7 + 0.3 * random.random())  # Adjust the color
    # logo_im = ImageEnhance.Sharpness(logo_im).enhance(0.7 + 0.3 * random.random())  # Adjust the sharpness
    logo_im = logo_im.filter(ImageFilter.GaussianBlur(radius=1.0 + 0.4 * random.random()))  # 需要对logo进行模糊化处理

    base_im = ImageEnhance.Color(base_im).enhance(0.8 + 0.5 * random.random())  # Adjust the color
    base_im = ImageEnhance.Contrast(base_im).enhance(0.8 + 0.5 * random.random())  # Adjust the contrast
    base_im = ImageEnhance.Sharpness(base_im).enhance(0.8 + 0.5 * random.random())  # Adjust the sharpness
    base_im.paste(logo_im, (logo_x, logo_y), logo_im)  # 粘贴logo (logo_x, logo_y)坐标是粘贴的坐标, 将logo图片粘贴到背景上去

    # if(base_im_w - logo_x >  )
    light0_x = base_im_w - logo_x
    light0_y = int(0.5 * base_im_h - logo_y) if (0.5 * base_im_h - logo_y < logo_y) else (
            logo_y + logo_size_y + random.randint(1, 5))
    if light0_y < 5:
        light0_y = random.randint(3, 10)
    light0_im = ImageEnhance.Color(light0_im).enhance(0.8 + 0.5 * random.random())  # Adjust the color
    # light0_im = ImageEnhance.Contrast(light0_im).enhance(0.8 + 0.5 * random.random())  # Adjust the contrast
    light0_im = ImageEnhance.Sharpness(light0_im).enhance(0.8 + 0.5 * random.random())  # Adjust the sharpness
    base_im.paste(light0_im, (light0_x, light0_y))  # 粘贴light0

    light1_x = (light0_x + int((2 * random.random() + 1.5) * light0_im.size[0]))  # 第二个灯在第一个的右边1.5倍 灯的宽度距离 高度上下4个像素偏移
    light1_y = light0_y + 2 - random.randint(0, 4)
    light1_im = ImageEnhance.Color(light1_im).enhance(0.8 + 0.5 * random.random())  # Adjust the color
    # light1_im = ImageEnhance.Contrast(light1_im).enhance(0.8 + 0.5 * random.random())  # Adjust the contrast
    light1_im = ImageEnhance.Sharpness(light1_im).enhance(0.8 + 0.5 * random.random())  # Adjust the sharpness
    base_im.paste(light1_im, (light1_x, light1_y))  # 粘贴light1

    # 确定打标数据
    data_mark = [[base_im_w, base_im_h], [logo_x, logo_y, logo_size_x, logo_size_y],
                 [light0_x, light0_y, light0_im.size[0], light0_im.size[1]],
                 [light1_x, light1_y, light1_im.size[0],
                  light1_im.size[1]]]  # base_im:背景尺寸，  logo_x:logo左上角的定位，logo_size:logo尺寸
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
        light_dir = os.path.join(work_dir, "before\\light")
        logo_txt_dir = os.path.join(work_dir, "before")
        save_im_dir = os.path.join(work_dir, "JPEGImages")
        save_xml_dir = os.path.join(work_dir, "Annotations")
        logo_inf_name = "information.txt"  # logo分类的文件
        logo_inf_path = os.path.join(logo_txt_dir, logo_inf_name)  # logo信息文件的完整路径
        inf_dict = txt2dict(logo_inf_path)  # logo编码后面作为字典的键。如：{'1001': ['禁止通行', '01'],
        base_list = os.listdir(base_dir)  # 获取背景图片列表

        logo_name_dict = get_logo_name_dict(logo_dir)
        base_name = base_list[random.randint(0, len(base_list) - 1)]  # 随机选择一个背景图片
        base_name_first = os.path.splitext(base_name)[0]  # 提取背景图片的文件名（不包含后缀.jpg）
        base_im_path = os.path.join(base_dir, base_name)  # 组成完整的路径：路径加文件名

        light_list = os.listdir(light_dir)  # 获取light 列表
        light_name = []
        light_name_first = []
        light_im_path = []
        for i in range(2):
            # print(i)
            light_name.append(light_list[random.randint(0, len(light_list) - 1)])  # 随机选择一个light图片
            # print(light_name)
            light_name_first.append(os.path.splitext(light_name[i])[0])  # 提取light图片的文件名（不包含后缀.jpg .png）
            # print(light_name_first)
            light_im_path.append(os.path.join(light_dir, light_name[i]))

        logo_name_list = sorted(logo_name_dict.items())  # 将logo的字典信息转化成 列表信息（logo名称（不含后缀）：所属的文件夹）
        logo_name = logo_name_list[random.randint(0, len(list(logo_name_dict))) - 1][0]  # 随机选取一个logo图片
        logo_dir = os.path.join(logo_dir, logo_name_dict[logo_name])
        logo_im_path = os.path.join(logo_dir, logo_name)

        logo_name_first = os.path.splitext(logo_name)[0]  # logo前四位是标志编号（同一种标志的编号相同），后四位是标志的版本号
        base_im = Image.open(base_im_path)  # 打开背景图片
        logo_im = Image.open(logo_im_path)  # 打开logo图片
        light0_im = Image.open(light_im_path[0])  # 打开light图片
        light1_im = Image.open(light_im_path[1])  # 打开light图片

        di = random.random()  # 分配三种方式数量比例

        if di < 0.6:
            direction = "right"
        elif di > 0.2:
            direction = "light"
        else:
            direction = "level"

        base_im, data_mark = add_logo(base_im, logo_im, light0_im, light1_im, direction=direction)  # 返回图片和用于打标的数据
        number += 1  # 用于统计生成图片的数量，即当前图片的编号
        save_im_name = "%06d.jpg" % number  # 6位整数保存，前面用零补齐
        save_im_path = os.path.join(save_im_dir, save_im_name)
        base_im.save(save_im_path)  # 保存图片到指定路径
        save_xml_name = "%06d.xml" % number  # 拼凑保存时，XML标记文件的名称

        save_xml_path = os.path.join(save_xml_dir, save_xml_name)
        logo_type = inf_dict[logo_name_first[:4]]  # 找到这个编号的logo对应的类型（汉字） ['旅游', '08']
        light_type = []
        light_type.append(inf_dict[light_name_first[0][:4]])
        light_type.append(inf_dict[light_name_first[1][:4]])
        xml_folder = os.path.split(logo_dir)[-1]  # 获取当前所在文件夹的名称
        xml_fullname = 'base' + base_name_first + '__' + 'logo' + logo_name_first + '__' + 'light0' + \
                       light_name_first[0][0] + 'light1' + light_name_first[1][0] + '.jpg'  # 拼凑保存时，图片文件的名称
        data_mark[1].insert(0, logo_type)
        # print(data_mark)
        data_mark[2].insert(0, light_type[0])
        data_mark[3].insert(0, light_type[1])
        # print(data_mark)
        root = edit_xml(xml_fullname, save_im_name, xml_folder, data_mark)  # ########
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
        if (number % 10 == 0)| (number==loop):
            print(u'logo添加成功——已完成%d张---用时%d秒 = %d分 = %f小时，已完成比例%f,还需用时%f小时---平均10000张图片用时%d分' % (
                number,end - start, (end - start) / 60, (end - start) / 3600, number / loop,
                ((loop - number) * ((end - start) / 3600)) / number, (10000 * (end - start)) / number / 60))
    in_file_train.close()
    in_file_test.close()


if __name__ == '__main__':
    # work_dir = os.getcwd()
    work_dir = 'C:\\Users\\young\\Desktop\\YZN20180901'
    if not os.path.exists(os.path.join(work_dir, "Annotations")):
        os.makedirs(os.path.join(work_dir, "Annotations"))
    if not os.path.exists(os.path.join(work_dir, "ImageSets\\Main")):
        os.makedirs(os.path.join(work_dir, "ImageSets\\Main"))
    if not os.path.exists(os.path.join(work_dir, "JPEGImages")):
        os.makedirs(os.path.join(work_dir, "JPEGImages"))
    go(work_dir, loop=150)
    print("程序执行完成")
