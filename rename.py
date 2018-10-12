import os
from PIL import Image


def init_logo_name(logo_dir):
    listdir01 = os.listdir(logo_dir)
    for i in range(len(listdir01)):
        # print(i)
        path01 = os.path.join(logo_dir, listdir01[i])
        listdir02 = os.listdir(path01)
        for j in range(len(listdir02)):
            print(j)
            # print("%s%04d" % (listdir01[i], i))  # 10010000
            path02 = os.path.join(path01, listdir02[j])
            # print(path02)
            # x = os.path.splitext(path02)
            # img = Image.open(path02)
            # img.save(os.path.join(path01, ('%s%04d' % (listdir01[i], j) + ".png")))
            os.rename(path02, os.path.join(path01, ('1%05d' % j) + ".xml"))


if __name__ == "__main__":
    # logo_dir = 'C:\\Users\\young\\Desktop\\test\\before\\logo'.replace("\\", "/")
    logo_dir = 'C:\\Users\\young\\Desktop\\121'
    init_logo_name(logo_dir)
