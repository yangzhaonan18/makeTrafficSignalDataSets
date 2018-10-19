# Making traffic signal data sets
- 函数作用：根据少量的背景和logo图片,合成大量训练需要的数据集。
- 函数：yzn_make_data.py   yzn_voc_label.py  modifyXML.py
## 1.yzn_make_data.py 
1. make_folder.py  # 初始化文件夹,创建需要的文件夹
2. get_base.py  # 随机提取一张背景图片
3. get_logo.py  # 随机提取一张标志图片
3. get_other.py  # 随机提取一张负样本图片
4. get_inf.py  # 读取存放标志命名与编号对应的文件，打标时需要编号信息
5. add_logo.py  # 将背景图片和标志图片合成一张图
6. edit_xml.py  # 编辑打标文件
7. edit_txt.py  # 编辑YOLOv3训练数据集时需要的图片名称文件

## 2.yzn_voc_label.py
函数作用：将VOC数据集的点坐标格式存放XML文件，转化成YOLOv3使用的坐标比例存放的TXT文件。
## 3.modifyXML.py
函数作用：纠正所有XML文件中的背景图片的长度和宽度值：1280*1024。
## 4.correct_result.py
函数作用：纠正每一个视频序列中检测错误的目标。
