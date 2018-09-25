import os
import random


def get_base(work_dir):
    base_dir = os.path.join(work_dir, "before\\base")
    base_list = os.listdir(base_dir)  # 获取背景图片列表
    # print(random.randint(0, len(base_list) - 1))
    base_name = base_list[random.randint(0, len(base_list) - 1)]  # 随机选择一个背景图片 左闭右闭
    # base_name = os.path.splitext(base_name)[0]  # 提取背景图片的文件名（不包含后缀.jpg）
    base_path = os.path.join(base_dir, base_name)  # 组成完整的路径：路径加文件名

    # print(base_path, base_name)
    return base_path, base_name


if __name__ == "__main__":
    work_dir = 'C:\\Users\\young\\Desktop\\test'
    get_base(work_dir)
