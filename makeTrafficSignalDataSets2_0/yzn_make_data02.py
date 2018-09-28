# from PIL import Image, ImageFilter, ImageEnhance
# from lxml import etree as ET
# from xml.dom import minidom
import os
import time
# import random
from make_folder import make_folder
from get_base import get_base
from get_logo import get_logo
from get_inf import get_inf
from add_logo import add_logo
from edit_xml import edit_xml
from edit_txt import edit_txt


def run(work_dir, loop=5):
    start = time.time()
    inf_dict = get_inf(work_dir)
    for num in range(loop):
        # print(num)
        base_path, base_name = get_base(work_dir)
        logo_path, logo_name = get_logo(work_dir)
        # print(logo_path)
        coor, logo_im = add_logo(work_dir, num, base_path, logo_path, base_name, logo_name)
        edit_xml(work_dir, num, base_path, logo_path, coor, logo_im, inf_dict[os.path.splitext(logo_name)[0][:4]])
        edit_txt(work_dir, num)
        if num % 10 == 0 and num != 0:
            end = time.time()
            print(u'logo添加成功——已完成%d张---用时%d秒 = %d分 = %f小时，已完成比例%f,还需用时%f小时---平均10000张图片用时%d分' % (
                num, end - start, (end - start) / 60, (end - start) / 3600, num / loop,
                ((loop - num) * ((end - start) / 3600)) / num, (10000 * (end - start)) / num / 60))
    return None

if __name__ == '__main__':
    # work_dir = os.getcwd()
    work_dir = 'C:\\Users\\young\\Desktop\\test'  # .replace("\\", "/")
    make_folder(work_dir)
    run(work_dir, loop=500)
    print("程序执行完成")
