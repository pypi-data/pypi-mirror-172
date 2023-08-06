import os, shutil
from rsgz.file.files import get_base_name




# 返回所有的目录列表
def get_dirs(dir_path):
    r"""
    返回所有的目录列表
    """
    dir_list = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for dirname in dirnames:
            the_dir = os.path.join(dirpath, dirname)
            dir_list.append(the_dir)
    return dir_list

# 返回文件夹数量
def get_dir_shuliang(dir_path):
    r"""
    返回文件夹数量
    """
    return len(get_dirs(dir_path))

# 目录比较目录(子目录 补集)
def compare_dir(dir_fu, dir_zi):
    r"""
    目录比较目录
    返回 父列表比子列表多出的一部分  返回 多出的部分列表
    1 子列表是父列表一部分

    """
    fu_set = set(get_base_name(get_dirs(dir_fu)))
    zi_set = set(get_base_name(get_dirs(dir_zi)))
    diff = list(fu_set.difference(zi_set))

# 移动目录补集
def move_buji(dir_fu, dir_zi, move_to_dir):
    r"""
    移动一个文件夹的补集 到目标目录
    dir_fu = r'\\R1\r1\已经完成\444-900'    # 父集
    dir_zi = r'\\R1\r1\已经完成\完成'        # 子集
    move_to_dir = r'\\R1\r1\已经完成\未完成'  # 移动到
    move_buji(dir_fu, dir_zi, move_to_dir)  # 将补集移动到
    """
    fu_set = set(get_base_name(get_dirs(dir_fu)))
    zi_set = set(get_base_name(get_dirs(dir_zi)))
    diff = list(fu_set.difference(zi_set))
    if not os.path.exists(move_to_dir):
        os.mkdir(move_to_dir)
    for i in diff:
        old = os.path.join(dir_fu, i)
        # new = os.path.join(move_to_dir, i)
        shutil.move(old, move_to_dir)

# 打印目录结构
def mulu_jiegou(path, indent = 0, maxi = -1):
    '''
        按文件类型递归输出目录结构
        :param path:   str 文件路径
        :param indent: int 首次缩进空格(默认为 0，一般不用改变)
        :param maxi:   int 最大展开层数(默认为 -1，表示全部展开)
    '''
    if maxi != 0:
        try:
            lsdir = os.listdir(path)
        except PermissionError:   # 权限不够的文件  不处理
            pass
        else:
            dirs = [item for item in lsdir if os.path.isdir(os.path.join(path, item))]
            files = [item for item in lsdir if os.path.isfile(os.path.join(path, item))]
            for item in dirs:
                print(' ' * indent, '+', item)
                mulu_jiegou(os.path.join(path, item), indent + 4, maxi - 1)
            for item in files:
                print(' ' * indent, '-', item)

# 给个列表 复制列表的文件夹 到目标目录
def copytree_common_dir(the_list, fu_path, copy_to):
    r"""
    复制 fu_path 中the_list出现的目录 到 copy_to位置

    the_list 就是子文件夹 简单列表
    fu_path 是父文件夹路径  包含了子文件夹列表

    the_list = ["23377-23384","23371-23376","23363-23370"]
    fu_path = r"\\192.168.0.200\e\李江涛\图集\成品\CXCJ女士插肩长袖包臀\女士插肩长袖包臀CXCJ01"
    copy_to =r"C:\Users\Administrator\Desktop\@2"
    """
    dir_list = get_dirs(fu_path)
    for i in dir_list:
        for j in the_list:
            if i.split(os.sep)[-1] == j:
                print(i)
                shutil.copytree(i, copy_to + r"\{}".format(j))

# 文件夹命名为 1 2 3
def rename_dir_1_2_3(fu):
    r"""
    fu = r"C:\Users\Administrator\Desktop\V领长袖\V领长袖"
    rename_dir_1_2_3(fu)
    """

    num = 0
    for dirpath, dirnames, filenames in os.walk(fu):
        for dirname in dirnames:
            num = num + 1
            dir1 = os.path.join(dirpath, dirname)
            xin = os.path.join(os.path.dirname(dir1), "xxxaaaxxx" + str(num))
            # print(xin)
            os.rename(dir1, xin)
    num = 0
    for dirpath, dirnames, filenames in os.walk(fu):
        for dirname in dirnames:
            num = num + 1
            dir1 = os.path.join(dirpath, dirname)
            xin = os.path.join(os.path.dirname(dir1), str(num))
            # print(xin)
            os.rename(dir1, xin)

if __name__ == '__main__':
    # path = r"C:\Users\Administrator\Desktop\111"
    # mulu_jiegou(path, indent = 0, maxi = -1)

    fu = r"C:\Users\Administrator\Desktop\xxxx"
    rename_dir_1_2_3(fu)

