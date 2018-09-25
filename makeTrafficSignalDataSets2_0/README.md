# makeTrafficSignalDataSets2_0
主函数：yzn_make_data02.py
## 1.make_folder.py
函数作用：在工作目录下生成三个文件夹：1.Annotations（存放标记文件.xml） 2.ImageSets\\Main（存放含图片编号的train.txt和test.txt文件）  JPEGImages（存放图片文件.jpg）
## 2.get_base.py
函数作用：从before\\base文件夹下随机选择一个背景图片，return 绝对路径和图片名称。
## 3.get_logo.py
函数作用：从before\\logo文件夹下随机选择一个logo图片，return 绝对路径和图片名称。
## 4.get_inf.py
函数作用：将before\\information.txt文件中的内容转化成字典存储。如：1001 禁止驶入 1 转化成{1001：[禁止驶入,1] }
## 5.add_logo.py
函数作用：将一张背景图和logo图片合成(生成)一张图，return logo的左上角坐标和logo图片
## 6.edit_xml.py
函数作用：生成标记文件.xml
## 7.edit_txt.py
函数作用：生成含图片编号文件 train.txt和test.txt。