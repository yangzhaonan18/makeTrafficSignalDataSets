import os
import random

def edit_txt(work_dir, num):
    save_main_dir = os.path.join(work_dir, "ImageSets/Main")
    if num == 0:
        style = 'w'
    else:
        style = 'a+'
    in_file_train = open(os.path.join(save_main_dir, "train.txt"), style)
    in_file_test = open(os.path.join(save_main_dir, "test.txt"), style)

    if random.random() < 0.8:  # 设置训练数据集的比例
        in_file_train.write("%06d\n" % num)
    else:
        in_file_test.write("%06d\n" % num)

    in_file_train.close()
    in_file_test.close()

    return None


if __name__ == "__main__":
    work_dir = 'C:\\Users\\young\\Desktop\\test'
    num = 0
    edit_txt(work_dir, num)