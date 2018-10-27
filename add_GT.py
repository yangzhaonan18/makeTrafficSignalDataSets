# -*- coding:utf-8 -*-
# Program role: Calculate the score by comparing two XML files
import os
import xml.etree.ElementTree as ET2
from PIL import Image, ImageDraw, ImageFont


def get_coor(xml_path):
    print("xml_path", xml_path)
    tree01 = ET2.parse(xml_path)
    root01 = tree01.getroot()
    result_dict = {}
    for child01 in root01:
        # print(child01.tag[5:10])
        # print(child01.tag[16:21])
        if child01.tag[5:10] < str("99999") and child01.tag[16:21] < str("99999"):  # <Frame00001Target00000>
            # dic[child01.tag[5:10]] = child01.
            if child01.tag[16:21] == str("00000"):
                result_dict[child01.tag[5:10]] = []
            result_dict[child01.tag[5:10]].append(
                child01.find("Type").text.split() + child01.find("Position").text.split())
            # print(child01.find("Type").text)
            # print(child01.find("Position").text.split())
    # print(result_dict)
    return result_dict


def add_GT(save_path, img_path, coor_dict, i):
    print("img_path:", img_path)
    if str(i).zfill(5) in coor_dict:
        img = Image.open(img_path)
        drawObject = ImageDraw.Draw(img)
        Font1 = ImageFont.truetype("impact", 60)
        coors = coor_dict[str(i).zfill(5)]
        # print("coor_dict[str(i).zfill(5)]: ", coor)
        for j in range(len(coors)):
            # print("coor:", coor)
            for r in coors:
                print("r:", r)
                # for coor in coors:
                #     int(coor)
                drawObject.line(
                    [int(r[1]) - int(r[3]) / 2, int(r[2]) - int(r[4]) / 2, int(r[1]) + int(r[3]) / 2,
                     int(r[2]) - int(r[4]) / 2],
                    fill=(255, 0, 0), width=3)
                drawObject.text((int(r[2][0]) - int(r[2]) / 2, int(r[1]) + int(r[3]) / 2 + 60), "%s+%s" % (r[0], r[1]),
                                font=Font1, fill=(255, 0, 0))
        print("save_path:", save_path)
        img.save(save_path)
    else:
        img = Image.open(img_path)
        drawObject = ImageDraw.Draw(img)
        Font1 = ImageFont.truetype("impact", 60)
        drawObject.text((100, 100), "NO", font=Font1, fill=(255, 0, 0))
        img.save(save_path)


def mark_area(img_dir, xml_dir, save_dir1):
    img_dir_list = os.listdir(img_dir)
    for dir in img_dir_list:
        save_dir = os.path.join(save_dir1, dir)
        # print("save_dir:", save_dir)
        if not os.path.exists(save_dir):  # 创建一个问价存放图片
            os.makedirs(save_dir)
        gt_name = dir + "-GT.xml"
        img_dir_path = os.path.join(img_dir, dir)
        xml_path = os.path.join(xml_dir, gt_name)
        coor_dict = get_coor(xml_path)
        print("coor_list", coor_dict)
        print("xml_path", xml_path)
        img_list = os.listdir(img_dir_path)  # 一个视频的所有图片
        for i in range(len(img_list)):
            img_path = os.path.join(img_dir_path, img_list[i])
            save_path = os.path.join(save_dir, img_list[i])
            print("save_path:", save_path)
            print("img_path", img_path)
            add_GT(save_path, img_path, coor_dict, i)  # 添加方框GT


if __name__ == "__main__":
    work_dir = "C:\\Users\\young\\Desktop\\data"
    img_dir = os.path.join(work_dir, "TSD-Signal")
    xml_dir = os.path.join(work_dir, "TSD-Signal-GT")
    save_dir = os.path.join(work_dir, "TSD-Save")
    mark_area(img_dir, xml_dir, save_dir)
