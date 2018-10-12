import os


def get_dir_file_dict(logo_dir):  # 输入的是存放logo 的文件夹
    logo_list = os.listdir(logo_dir)
    logo_name_dict = {}
    for i in range(len(logo_list)):  # 遍历文件夹下面的文件夹
        path = os.path.join(logo_dir, logo_list[i])  # 获取文件夹的绝对路径
        path_list = os.listdir(path)  # 获取文件夹下的文件列表
        logo_name_dict[logo_list[i]] = path_list

    # print(logo_name_dict)  # {'1001': ['10010020.png', '10010024.png'], '1002': ['10020001.png', '10020004.png']}
    # print(sorted(logo_name_dict.items()))
    return logo_name_dict  # 返回logo文件名列表，不包含.后缀


if __name__ == "__main__":
    logo_dir = 'C:\\Users\\young\\Desktop\\test\\before\\logo'
    get_dir_file_dict(logo_dir)
