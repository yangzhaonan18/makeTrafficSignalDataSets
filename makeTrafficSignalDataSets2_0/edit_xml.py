from PIL import Image
from lxml import etree as ET
from xml.dom import minidom
import os


def edit_xml(work_dir, num, base_path, logo_path, coor, logo_im, inf_value):
    save_xml_path = os.path.join(work_dir, "Annotations")
    save_xml_path = os.path.join(save_xml_path, "%06d.xml" % num)
    root = ET.Element("annotation")
    # root.set("version", "1.0")  # root的属性设置
    folder = ET.SubElement(root, "folder")
    folder.text = work_dir
    filename = ET.SubElement(root, "filename")
    filename.text = os.path.split(base_path)[1]  # 0012.jpg
    fullname = ET.SubElement(root, "fullname")
    fullname.text = os.path.split(base_path)[1] + "+" + os.path.split(logo_path)[1]  # 0012.jpg+10010002.png
    source = ET.SubElement(root, "source")
    source.text = "201808"
    owner = ET.SubElement(root, "owner")
    owner.text = "YZN"
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(1280)  # str(data_mark[0][0])
    height = ET.SubElement(size, "height")
    height.text = str(1024)  # str(data_mark[0][1])
    depth = ET.SubElement(size, "depth")
    depth.text = "3"
    segmented = ET.SubElement(root, "segmented")
    segmented.text = "0"
    object = ET.SubElement(root, "object")
    name = ET.SubElement(object, "name")  # number
    name.text = inf_value[0]
    # meaning = ET.SubElement(object, "meaning")  # name
    # meaning.text = inf_value[0]
    pose = ET.SubElement(object, "pose")
    pose.text = "Unspecified"
    truncated = ET.SubElement(object, "truncated")
    truncated.text = "0"
    difficult = ET.SubElement(object, "difficult")
    difficult.text = "0"
    bndbox = ET.SubElement(object, "bndbox")
    xmin = ET.SubElement(bndbox, "xmin")
    xmin.text = str(coor[0])
    ymin = ET.SubElement(bndbox, "ymin")
    ymin.text = str(coor[1])
    xmax = ET.SubElement(bndbox, "xmax")
    xmax.text = str(coor[0] + logo_im.size[0])
    ymax = ET.SubElement(bndbox, "ymax")
    ymax.text = str(coor[1] + logo_im.size[1])

    tree = ET.ElementTree(root)
    tree.write(save_xml_path, encoding="UTF-8", xml_declaration=True)  # 将tree内容写入save_xml_path
    root = ET.parse(save_xml_path)  # 解析（读取）save_xml_path文件
    file_lines = minidom.parseString(ET.tostring(root, encoding="Utf-8")).toprettyxml(
        indent="\t")  # 转多行格式
    file_line = open(save_xml_path, "w", encoding="utf-8")  # 打开原来的单行格式文件
    file_line.write(file_lines)  # 将多行内容写入之前的单行文件中（单行文件内容格式化后写入的，之前内容全部消失）
    file_line.close()
    # print(u'已合成图片%s，已生成标记文件%s' % (save_im_name, save_xml_name))
    return None


if __name__ == "__main__":
    work_dir = 'C:\\Users\\young\\Desktop\\test'
    num = 1
    base_path = "C:\\Users\\young\\Desktop\\test\\before\\base\\0012.jpg"
    logo_path = "C:\\Users\\young\\Desktop\\test\\before\\logo\\1001\\10010002.png"
    coor = [999, 552]
    inf_value = ['禁止2驶入', '6']
    root = edit_xml(work_dir, num, base_path, logo_path, coor, inf_value)
