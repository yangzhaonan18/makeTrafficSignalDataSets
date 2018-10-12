# -*- coding:utf-8 -*-
# Program role: Calculate the score by comparing two XML files
import os
import xml.etree.ElementTree as ET2


def judgment(r_true, r_test):  #
    """
    # Determine if the position is correct
    :param r_true: Marked real area coordinates
    :param r_test: Detected area coordinates
    :return: True is correct
    """
    if r_true[0] == r_test[0]:  # same type
        ox2 = r_test[1] + r_test[3] / 2
        oy2 = r_test[2] + r_test[4] / 2
        if (ox2 > r_true[1] and ox2 < r_true[1] + r_true[3]) and (oy2 > r_true[2] and oy2 < r_true[2] + r_true[4]):
            return True
    return False


def calculated_score(result_dict01, result_dict02, n_tp, n_true, n_test):
    """
    :param result_dict01: (Marked real area coordinates) The coordinates of all the targets of a video
    :param result_dict02: (Detected area coordinates ) The coordinates of all the targets of a video
    :param n_tp: Number of correctly detected
    :param n_true: Mark the number of tests that need to be detected
    :param n_test: The number of targets eventually detected
    :return: n_tp, n_true, n_test
    """
    for frame in result_dict01:
        # print("GT is ", result_dict01[frame])  # [['2', '1026', '296', '61', '51'], ['3', '1026', '296', '66', '55']]
        # print("Test is ", result_dict02[frame])  # [['2', '1026', '296', '61', '51']]
        rs_true = result_dict01[frame]
        n_true += len(rs_true)
        if frame in result_dict02:
            rs_test = result_dict02[frame]
            n_test += len(rs_test)
        else:  # When a frame detection does not detect the target
            continue
        list_true = [0] * len(rs_true)  # 0: target not  successfully matched, 1:successful matching
        list_test = [0] * len(rs_test)
        # print("Before testing：")
        # print(list_true)
        # print(list_test)
        flag = 0

        while sum(list_true) < len(rs_true) and sum(list_test) < len(rs_test) and flag == 0:
            for i in range(len(rs_true)):
                if list_true[i] == 0:
                    rs_true[i] = [int(k) for k in rs_true[i]]
                    for j in range(len(rs_test)):
                        if list_test[j] == 0:
                            rs_test[j] = [int(k) for k in rs_test[j]]
                            if judgment(rs_true[i], rs_test[j]):
                                list_true[i] = 1
                                list_test[j] = 1
                                n_tp += 1
                        if i + j + 2 == len(rs_true) + len(rs_test):
                            flag = 1

        # print("检测之后的：")
        # print(list_true)
        # print(list_test)
    return n_tp, n_true, n_test


def get_result_dict(path):
    """
    # Read the information in the xml file and convert it to dictionary storage
    :param path: Absolute path
    :return: result_dict: All target coordinates in the xml file
    """
    tree01 = ET2.parse(path)
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


if __name__ == "__main__":
    """
    The test results of the same image must be saved with the same name as the standard answer.
    work_dir01：Store the standard answer XML file
    work_dir02：The submitted answer XML file is stored.
    """

    work_dir01 = "C:\\Users\\young\\Desktop\\score01"  # true
    work_dir02 = "C:\\Users\\young\\Desktop\\score02"  # test
    file_list = os.listdir(work_dir01)
    n_tp = 0  # Number of correctly detected
    n_true = 0  # Mark the number of tests that need to be detected
    n_test = 0  # The number of targets eventually detected

    for file in file_list:
        path01 = os.path.join(work_dir01, file)
        path02 = os.path.join(work_dir02, file)
        result_dict01 = get_result_dict(path01)
        result_dict02 = get_result_dict(path02)
        n_tp, n_true, n_test = calculated_score(result_dict01, result_dict02, n_tp, n_true, n_test)

    print("Number of targets detected(n_test):", n_test)
    print("Number of targets marked(n_true):", n_true)
    print("\nCorrect detection(n_tp)：", n_tp)
    print("False detection(n_test - n_tp)：", n_test - n_tp)
    print("Leak detection(n_true - n_tp)：", n_true - n_tp)

    precision = round(n_tp / n_test, 2)
    recall = round(n_tp / n_true, 2)
    f_measure = round(2 * precision * recall / (precision + recall), 2)

    print("\nPrecision, Recall, F_measure:", precision, recall, f_measure)
