import os


def make_folder(work_dir):
    if not os.path.exists(os.path.join(work_dir, "Annotations")):
        os.makedirs(os.path.join(work_dir, "Annotations"))
    if not os.path.exists(os.path.join(work_dir, "ImageSets")):
        os.makedirs(os.path.join(work_dir, "ImageSets"))
        os.makedirs(os.path.join(os.path.join(work_dir, "ImageSets"), "Main"))
    if not os.path.exists(os.path.join(work_dir, "JPEGImages")):
        os.makedirs(os.path.join(work_dir, "JPEGImages"))


if __name__ == "__main__":
    work_dir = 'C:\\Users\\young\\Desktop\\test'
    make_folder(work_dir)
