def txt2dict(inf_path):
    inf_dict = {}  # 定义一个空字典
    file = open(inf_path, "r", encoding="gbk", errors="ignore")  # 注意编码格式 近影响结果 print可以测试文件内容的显示效果  utf-8  gbk
    while True:
        mystr = file.readline()  # 表示一次读取一行
        if not mystr:
            break  # 读到数据最后跳出，结束循环。数据的最后也就是读不到数据了，mystr为空的时候
        inf_dict[mystr.split()[0]] = mystr.split()[1:]
    return inf_dict


if __name__ == "__main__":
    inf_path = "C:\\Users\\young\\Desktop\\test\\before\\information.txt"
    txt2dict(inf_path)
