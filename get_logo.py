import os
import random


def get_logo(work_dir):
    im_dir = os.path.join(work_dir, "before\\logo")
    im_list = os.listdir(im_dir)  # 获取背景图片列表
    im_name = im_list[random.randint(0, len(im_list) - 1)]  # 随机选择一个背景图片 左闭右闭
    # base_name = os.path.splitext(base_name)[0]  # 提取背景图片的文件名（不包含后缀.jpg）
    im_dir = os.path.join(im_dir, im_name)  # 组成完整的路径：路径加文件名
    im_list = os.listdir(im_dir)
    im_name = im_list[random.randint(0, len(im_list) - 1)]  # 随机选择一个背景图片 左闭右闭
    im_path = os.path.join(im_dir, im_name)
    # print(im_path, im_name)
    return im_path, im_name


if __name__ == "__main__":
    work_dir = 'C:\\Users\\young\\Desktop\\test'
    get_logo(work_dir)
