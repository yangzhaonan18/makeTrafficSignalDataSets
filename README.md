# Making traffic signal data sets
- 函数作用：根据少量的背景和logo图片,合成大量训练需要的数据集。
- 函数：yzn_make_data.py   yzn_voc_label.py  modifyXML.py
## yzn_make_data.py 
1. make_folder.py
2. get_base.py
3. get_logo.py
3. get_other.py
4. get_inf.py
5. add_logo.py
6. edit_xml.py
7. edit_txt.py

## yzn_voc_label.py
函数作用：将VOC数据集的点坐标格式存放XML文件，转化成YOLOv3使用的坐标比例存放的TXT文件。
## modifyXML.py
函数作用：纠正所有XML文件中的背景图片的长度和宽度值：1280*1024。
## correct_result.py
函数作用：纠正每一个视频序列中检测错误的目标。