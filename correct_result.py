# encoding="UTF-8"
from lxml import etree as ET
from xml.dom import minidom
import os


def edit_xml2(xml_dir, dir, result_list):
    root = ET.Element("opencv_storage")
    for i in range(len(result_list)):
        Frame1 = ET.SubElement(root, "Frame%05dTargetNumber" % i)
        Frame1.text = str(len(result_list[i]))
        for j in range(len(result_list[i])):
            Frame2 = ET.SubElement(root, "Frame%05dTarget%05d" % (i, j))
            Type = ET.SubElement(Frame2, "Type")
            Type.text = str(result_list[i][j][0])
            Position = ET.SubElement(Frame2, "Position")
            pos = str("")
            for result in result_list[i][j][2]:
                pos += str(int(result)) + " "
            pos = pos.rstrip()  # del right " "
            Position.text = str(pos)
    tree = ET.ElementTree(root)
    save_xml_path = os.path.join(xml_dir, dir + "-Result.xml")
    tree.write(save_xml_path, encoding="UTF-8", xml_declaration=True)  # 将tree内容写入save_xml_path
    root = ET.parse(save_xml_path)  # 解析（读取）save_xml_path文件
    file_lines = minidom.parseString(ET.tostring(root, encoding="UTF-8")).toprettyxml(
        indent="\t")  # 转多行格式
    file_line = open(save_xml_path, "w", encoding="UTF-8")  # 打开原来的单行格式文件
    file_line.write(file_lines)  # 将多行内容写入之前的单行文件中（单行文件内容格式化后写入的，之前内容全部消失）
    file_line.close()
    return None


def calculate_IOU(box_1, box_2):
    area_1 = box_1[2] * box_1[3]  # C的面积
    area_2 = box_2[2] * box_2[3]  # G的面积
    x1 = max(box_1[0], box_2[0])  # 左边上边求最大值 右边下边的求最小值
    y1 = max(box_1[1], box_2[1])
    x2 = min(box_1[0] + box_1[2], box_2[0] + box_2[2])
    y2 = min(box_1[1] + box_1[3], box_2[1] + box_2[3])
    w = max(0, x2 - x1)  # 右边减左边 下边减上边 计算出交集区域的左右宽度和上下高度
    h = max(0, y2 - y1)
    area = w * h  # C∩G的面积
    iou = area / (area_1 + area_2 - area)
    return iou


def find_rs(results, type):
    for i in range(len(results)):
        if results[i][0] == type:
            return results[i][2]
    return None

    # if len(results) > 0:  # 某一帧的目标非空
    #     for result in results:
    #         if len(result) > 0:
    #             if result[0] == type:
    #                 return result[2]  # 返回type类型的坐标
    # return None


def creat_new_rs(results_list, k, type):
    coor12, coor11, coor01, coor02 = None, None, None, None
    if k - 2 >= 0:
        coor12 = find_rs(results_list[k - 2], type)  # 前一个值
    if k - 1 >= 0:
        coor11 = find_rs(results_list[k - 1], type)  # 前一个值
    if k + 1 < len(results_list):
        coor01 = find_rs(results_list[k + 1], type)  # 后一个值
    if k + 2 < len(results_list):
        coor02 = find_rs(results_list[k + 2], type)  # 后后那个值

    if coor12 and coor11 and coor01 and coor02:
        results_list[k].append(
            [type, 1, [int((coor12[i] + coor11[i] + coor01[i] + coor02[i]) / 4) for i in range(0, 4)]])
    elif coor11 and coor01:
        results_list[k].append([type, 1, [int((coor11[i] + coor01[i]) / 2) for i in range(0, 4)]])
    elif coor01 and coor02:
        results_list[k].append([type, 1, [int(2 * coor01[i] - coor02[i]) for i in range(0, 4)]])
    elif coor12 and coor11:
        results_list[k].append([type, 1, [int(2 * coor11[i] - coor12[i]) for i in range(0, 4)]])

    return None


def add_results(results_list, type_list):
    for type in type_list:
        flag_list = [0] * len(results_list)
        while sum(flag_list) != len(results_list):
            print("flag_list", flag_list)
            print("666results_list", )
            for i in results_list:
                print(i)

            for k in range(len(results_list)):
                # print([k]*100)
                for i in range(len(results_list[k])):
                    if results_list[k][i] and results_list[k][i][0] == type:
                        print("results_list[k][i]", k, i, results_list[k][i])
                        flag_list[k] = 1
                    print("sum(flag_list)", sum(flag_list))
                if flag_list[k] != 1:  # 没有type这个类型
                    creat_new_rs(results_list, k, type)
    return None


def del_results(results_list, type_list):
    """
    :param results_list:
    :param type_list:
    :return:

    # print("type_list", type_list)
    # 补齐缺失的目标
    # flag = [0] * len(results_list)
    """

    # 纠正误检测的目标 更正目标的类别，位置保持不变
    flag = False
    while not flag:
        flag = True  # 停止循环
        for k in range(len(results_list) - 1):
            for i in range(len(results_list[k])):
                for j in range(len(results_list[k + 1])):
                    # print("k, i, j:", k, i, j)  # 纠正检测错误的
                    if calculate_IOU(results_list[k][i][2], results_list[k + 1][j][2]) > 0:  # 参数
                        if results_list[k][i][0] in type_list and results_list[k + 1][j][0] not in type_list:
                            results_list[k + 1][j][0] = results_list[k][i][0]
                            print("纠正后面的那个了,第", k + 1)
                            flag = False  # 继续循环
                        if results_list[k][i][0] not in type_list and results_list[k + 1][j][0] in type_list:
                            results_list[k][i][0] = results_list[k + 1][j][0]
                            print("纠正前面的那个了,第", k)
                            flag = False  # 继续循环

                            # for k in range(len(results_list) - 1):
        #     for i in range(len(results_list[k])):
        #         for j in range(len(results_list[k + 1])):
    print("results_list", )
    for i in results_list:
        print(i)
    # 删除不需要的目标（不在type_listz中的目标）  遍历一遍就可以删除完
    for k in range(len(results_list)):
        results = results_list[k]
        index = []
        for t in range(len(results)):
            if results[t][0] not in type_list:  # 删除不在出现的种类type_list中的目标
                index.insert(0, t)
        index = sorted(list(set(index)), reverse=True)

        for i in index:
            print("del *************** results[i]:", results[i])
            del results[i]

    # 删除每一帧中相同类型且有重叠的目标（删除后面那一个）
    for results in results_list:
        index = []
        for i in range(len(results) - 1):

            for j in range(i + 1, len(results)):
                # if results[i] not in type_list:
                #     index.insert(0, i)
                # if results[j] not in type_list:
                #     index.insert(0, j)
                iou = calculate_IOU(results[i][2], results[j][2])
                if iou > 0 and results[i][0] == results[j][0]:  # 删除相同类型且有重叠的目标（删除后面那一个）
                    index.insert(0, j)
                    # print(str(results[i]) + " and " + str(results[j]) + " IOU > 0.1 " + str(i) + " " + str(j))
        for i in sorted(set(index), reverse=True):
            # print("del *************** results[i]:", results[i])
            del results[i]

    print("results_list", )
    for i in results_list:
        print(i)

    return None


def correct_result(results_list, type_list):
    # 判断单目标还是多目标：
    print("results_list:", results_list)
    del_results(results_list, type_list)
    add_results(results_list, type_list)

    print("results_list", )
    for i in results_list:
        print(i)
    print("len(results_list)", len(results_list))

    return None


def find_frequent_obj(result_list):
    num_dict = {}  # 统计一个视频中所有帧检测到的目标数量 num_dict {0: 1, 2: 1, 1: 18} 1张图检测到0个目标，1图检测1个目标，18张图检测到1个目标
    type_dict = {}  # 统计一个视频中所有帧检测到的目标种类 type_dict {1: 19, 2: 1} 19次检测到1目标 1次检测到2目标
    for i in range(len(result_list)):
        if len(result_list[i]) not in num_dict:
            num_dict[len(result_list[i])] = 1
        else:
            num_dict[len(result_list[i])] += 1

        for obj in result_list[i]:
            if obj[0] not in type_dict:
                type_dict[obj[0]] = 1
            else:
                type_dict[obj[0]] += 1
    #
    # print("num_dict", num_dict)  # num_dict {0: 2, 2: 1, 1: 18}
    # print("type_dict", type_dict)  # type_dict {3: 15, 2: 1, 1: 3, 6: 1}

    num_dict = sorted(num_dict.items(), key=lambda item: item[1], reverse=True)  # 将字典按照value 降序排列，并转成列表
    type_dict = sorted(type_dict.items(), key=lambda item: item[1], reverse=True)  # 将字典按照value 降序排列，并转成列表
    frequent_num = num_dict[0][0] if num_dict[0][0] != 0 else num_dict[1][0]  # frequent_num 1

    print("frequent_num", frequent_num)  # num_dict [(1, 18), (0, 2), (2, 1)]
    print("num_dict", num_dict)  # type_dict [(3, 15), (1, 3), (2, 1), (6, 1)]
    print("type_dict", type_dict)  # type_list [3]

    type_list = [i[0] for i in type_dict][0:frequent_num]
    print("type_list", type_list)

    return type_list


if __name__ == "__main__":
    xml_dir = "C:\\Users\\young\\Desktop\\TSD-Signal-Result-TeamName"  # 存储xml文件的文件夹
    dir = "TSD-Signal-00120"  # 从这个文件夹中读取的视频序列
    # rs_list表示的是 dir = "TSD-Signal-00120" 文件夹下面的所有图片 检测到的目标信息
    results_list = [
        [],
        [],
        [],
        [],
        [[3, 1, [1026, 296, 61, 51]], [0, 1, [11026, 1296, 61, 51]]],
        [[3, 1, [1026, 296, 61, 51]], [0, 1, [11026, 1296, 61, 51]]],
        [[3, 1, [1026, 296, 61, 51]], [2, 1, [11026, 1296, 61, 51]]],
        [],
        [],
        [[3, 1, [1026, 296, 61, 51]], [2, 1, [11026, 1296, 61, 51]]],
        [[3, 1, [1026, 296, 61, 51]], [2, 1, [11026, 1296, 61, 51]]],
        [[3, 1, [1026, 296, 61, 51]], [2, 1, [11026, 1296, 61, 51]]],
        [[3, 1, [1026, 296, 61, 51]], [0, 1, [11026, 1296, 61, 51]]],
        [[3, 1, [1026, 296, 61, 51]]],
        [[7, 1, [1026, 296, 61, 51]], [2, 1, [11026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [],
        [],
        [],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [[9, 1, [1027, 296, 61, 51]], [4, 1, [2026, 2196, 61, 51]], [5, 1, [1026, 296, 61, 52]],
         [6, 1, [1026, 296, 61, 51]]],
        [],

        [],
        [[3, 1, [1027, 293, 57, 53]]],
        [[3, 1, [1027, 299, 62, 51]]],
        [[1, 1, [1027, 299, 89, 77]]],
        [[6, 1, [1027, 299, 97, 83]]],
        [],
        [],
        [],
        [],
        []
    ]

    type_list = find_frequent_obj(results_list)  # find frequent object  type_list [3, 2]
    correct_result(results_list, type_list)
    # edit_xml2(xml_dir, dir, results_list)
