r"""
批量命名文件夹为 1 2 3
"""
import os


def rename_dir_1_2_3(fu):
    r"""
    fu = r"C:\Users\Administrator\Desktop\V领长袖\V领长袖"
    rename_dir_1_2_3(fu)
    """

    num=0
    for dirpath, dirnames, filenames in os.walk(fu):
        for dirname in dirnames:
            num=num+1
            dir1 = os.path.join(dirpath, dirname)
            xin = os.path.join(os.path.dirname(dir1), "xxxaaaxxx"+str(num))
            # print(xin)
            os.rename(dir1, xin)
    num=0
    for dirpath, dirnames, filenames in os.walk(fu):
        for dirname in dirnames:
            num=num+1
            dir1 = os.path.join(dirpath, dirname)
            xin = os.path.join(os.path.dirname(dir1), str(num))
            # print(xin)
            os.rename(dir1, xin)