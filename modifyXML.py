import os
import xml.etree.ElementTree as ET


def test():
    path = "C:\\Users\\young\\Desktop\\YZN20180901\\Annotations".replace("\\", "/")
    files = os.listdir(path)
    print(files)
    for xmlFile in files:
        path = "C:\\Users\\young\\Desktop\\YZN20180901\\Annotations".replace("\\", "/")
        path = os.path.join(path, xmlFile).replace("\\", "/")
        print(path)
        tree = ET.parse(path)
        root = tree.getroot()
        size = root.find('size')
        width = size.find('width')
        height = size.find('height')
        width.text = str(1280)
        height.text = str(1024)
        tree.write(path, encoding="UTF-8", xml_declaration=True)  # 避免乱码


if __name__ == "__main__":
    test()
