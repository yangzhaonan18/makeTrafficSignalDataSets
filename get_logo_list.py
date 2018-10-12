# -*- coding:utf-8 -*-
# 这个模块写来没不用了…………不要了
import os


# 获取logo文件夹（logo_dir）下面的文件夹下面的文件名，存放在logo_name_list列表中。
def get_logo_list(logo_dir):  # 输入的是存放logo 的文件夹
    logo_list = os.listdir(logo_dir)
    logo_name_dict = {}
    for i in range(len(logo_list)):  # 遍历文件夹下面的文件夹
        path = os.path.join(logo_dir, logo_list[i])  # 获取文件夹的绝对路径
        path_list = os.listdir(path)  # 获取文件夹下的文件列表
        for j in range(len(path_list)):  # 去掉文件名中的后缀，只提取前面的四位编码  遍历文件夹下面的文件夹下的文件
            index = path_list[j].rfind('.')
            logo_name_dict[path_list[j][:index]] = logo_list[i]

    # print(logo_name_dict)
    # print("asdfasdfaf")
    # print(sorted(logo_name_dict.items()))
    return logo_name_dict  # 返回logo文件名列表，不包含.后缀


def get_base_list(base_dir):
    base_name_list = os.listdir(base_dir)
    print(base_name_list)
    return base_name_list


if __name__ == "__main__":
    logo_dir = 'C:\\Users\\young\\Desktop\\TS\\YZN20180828\\before\\logo'
    get_logo_list(logo_dir)
    base_dir = 'C:\\Users\young\\Desktop\\TS\\YZN20180828\\before\\base'
    get_base_list(base_dir)
