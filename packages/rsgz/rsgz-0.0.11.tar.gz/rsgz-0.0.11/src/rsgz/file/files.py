import os, re



def get_files(dir_path):
    r"""
    dir_path = C:\Users\Administrator\Desktop\rsgz
    file_list = get_files(dir_path)
    返回文件列表
    """
    files_list = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file = os.path.join(dirpath, filename)
            files_list.append(file)
    return files_list

def get_file_shuliang(dir_path):
    r"""
    返回所有文件数量
    """
    return len(get_files(dir_path))

def get_base_name(the_list):
    r"""
    the_list 是文件或者文件夹列表  返回最简短文件列表或者文件夹列表
    the_list = []
    new_list = get_base_name(the_list)
    """
    short_name_list = []
    for i in range(len(the_list)):
        short_name = the_list[i].split(os.sep)[-1]
        short_name_list.append(short_name)
    return short_name_list

def compare_file(dir_fu, dir_zi):
    r"""
    文件比较文件
    返回 多出的部分列表
    dir_fu = r""
    dir_zi = r""
    extra_part = compare_file(dir_fu, dir_zi)
    """
    fu_set = set(get_base_name(get_files(dir_fu)))
    zi_set = set(get_base_name(get_files(dir_zi)))
    diff = list(fu_set.difference(zi_set))
    return diff

def paixu_file(file_list, jiangxu):
    r"""
    对文件列表 进行排序
    file_list = ['1.jpg', '10.jpg', '11.jpg', '2.jpg']
    jiangxu = 1  降序
    jiangxu = 0  升序
    new_list = paixu_file(file_list, jiangxu=0) # 升序 ['1.jpg', '2.jpg', '10.jpg', '11.jpg']
    """
    if jiangxu:
        file_list.sort(key=lambda x: int(re.findall("\d+", x)[0]), reverse=True)  # 降序
    else:
        file_list.sort(key=lambda x: int(re.findall("\d+", x)[0]), reverse=False)  # 升序
    return file_list

def get_num_from_file(file_list):
    r"""
    获取文件列表中的数字
    file_list = ['32293black.jpeg', '32294blue.jpeg', '32295green.jpeg']
    new_list = get_num_from_file(file_list) # ['32293', '32294', '32295']
    """
    return list(map(lambda x: re.findall("\d+", x)[0], file_list))

def get_not_number(file_list):
    r"""
    获取文件列表中 非数字部分
    file_list = ['32293black.jpeg', '32294blue.jpeg', '32295green.jpeg']
    new_list = get_not_number(file_list)  # ['black.jpeg', 'blue.jpeg', 'green.jpeg']
    """
    return list(map(lambda x: re.findall("\D+", x)[0], file_list))

def remove_number(fu_path):
    r"""
    fu_path = r'C:\Users\Administrator\Desktop\linshi-user'
    remove_number(fu_path)
    去除父路径下的所有文件名字中的数字部分
    """
    list1 =get_files(fu_path)
    for i in list1:
        if 'png' in i or 'jpg' in i:
            fu = os.path.dirname(i)
            pic_name = i.split(os.sep)[-1]
            num = re.findall("\d+",pic_name)[0]
            new_pic_name = pic_name.replace(num,'')
            new_pic_name = os.path.join(fu,new_pic_name)
            print(new_pic_name)
            os.rename(i,new_pic_name)
    pass

def remove_str(file_list , houzhui):
    r"""
    去除文件列表对应部分字符串，不仅仅是后缀名哈  其他部分字符串都可以批量去除
    不改变原来文件
    file_list = ['black.jpeg', 'blue.jpeg', 'green.jpeg']
    new_list = remove_str(file_list , houzhui=".jpeg")
    new_list # ['black', 'blue', 'green']
    """
    return list(map(lambda x:x.replace(houzhui, ""), file_list))

def get_bianhao_yanse(file_list, houzhui):
    r"""
    参数
    file_list = ['32293black.jpeg', '32294blue.jpeg', '32295green.jpeg']
    bianhao, yanse = get_bianhao_yanse(file_list, houzhui=".jpeg")
    print(bianhao)
    print(yanse)
    """
    bianhao = get_num_from_file(file_list)
    new_list = get_not_number(file_list)
    yanse = remove_str(new_list, houzhui)
    return  bianhao, yanse

def del_pic(dir_path, geshi):
    r"""
    在目标文件夹 里面 删除指定格式图片
    dir_path = r"C:\Users\Administrator\Desktop\@2\23363-23370"
    geshi = ".png"
    del_pic(dir_path, geshi)
    """
    for i in get_files(dir_path):
        if geshi in i.split(os.sep)[-1]:
            os.remove(i)
            print("删除了 {}".format(i))



if __name__ == '__main__':
    dir_path = r"C:\Users\Administrator\Desktop\@2\23363-23370"
    geshi = ".png"
    del_pic(dir_path, geshi)