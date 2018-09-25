import os


def get_inf(work_dir):
    inf_dict = {}  # 定义一个空字典
    inf_path = os.path.join(os.path.join(work_dir, "before"),  "information.txt")  # logo信息文件的完整路径
    file = open(inf_path, "r", encoding="gbk", errors="ignore")  # 注意编码格式 近影响结果 print可以测试文件内容的显示效果  utf-8  gbk
    while True:
        mystr = file.readline()  # 表示一次读取一行
        if not mystr:
            break  # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
        # print(mystr.split()[1:])
        inf_dict[mystr.split()[0]] = mystr.split()[1:]
    # print(inf_dict)
    # C:\Users\young\Desktop\test\before\information.txt
    # information.txt
    # {'1001': ['禁止驶入', '1'], '1002': ['解除限制速度', '禁止非机动车进入', '2'], '1003': ['禁止超车', '3
    return inf_dict


if __name__ == "__main__":
    work_dir = 'C:\\Users\\young\\Desktop\\test'
    get_inf(work_dir)
