import os
import re
from rsgz.mulu.dirs import rename_dir_1_2_3
from rsgz.tupian.normal import remove_pic_str


# 给 图集文件夹 批量设置编号   里面的图片也设置编号
def set_bianhao(path_fu, bian_hao_start):
    r"""
    给文件夹批量设置编号
    里面的图片也设置编号
    注意：使用之前 将所有的数字都去掉

    bian_hao_start = 85000
    path_fu = r"C:\Users\Administrator\Desktop\xxxx"
    set_bianhao(path_fu, bian_hao_start)
    """

    # 这个是可以改  但是不处理一些不干净数据会报错
    def bianhao():
        r"""



        C:\Users\Administrator\Desktop\all\1\blue.jpg
        C:\Users\Administrator\Desktop\all\1\green.jpg
        C:\Users\Administrator\Desktop\all\1\grey.jpg
        C:\Users\Administrator\Desktop\all\1\light blue.jpg
        C:\Users\Administrator\Desktop\all\1\pink.jpg
        C:\Users\Administrator\Desktop\all\1\purple.jpg
        C:\Users\Administrator\Desktop\all\1\rose.jpg
        C:\Users\Administrator\Desktop\all\1\yellow.jpg
        --->
        编号25415开始 改成
        C:\Users\Administrator\Desktop\all\25415blue.jpg
        C:\Users\Administrator\Desktop\all\25416green.jpg
        C:\Users\Administrator\Desktop\all\25417grey.jpg
        C:\Users\Administrator\Desktop\all\25418light blue.jpg
        C:\Users\Administrator\Desktop\all\25419pink.jpg
        C:\Users\Administrator\Desktop\all\25420purple.jpg
        C:\Users\Administrator\Desktop\all\25421rose.jpg
        C:\Users\Administrator\Desktop\all\25422yellow.jpg

        大文件夹改成
        25415-25422
        """
        org_num  = bian_hao_start

        # 获取文件夹集合
        path_list = os.listdir(path_fu)

        # 文件夹集合排序
        path_list.sort(key=lambda x: int(x), reverse=False)  # path_list ['1', '2', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        # print("path_list", path_list)

        # 拼接完整文件夹路径
        path_list_full = [os.path.join(path_fu, i) for i in path_list]  # ['C:\\Users\\Administrator\\Desktop\\all\\1', 'C:\\Users\\Administrator\\Desktop\\all\\2']
        # print("path_list_full", path_list_full)

        # 迭代每个文件夹
        for i in range(len(path_list_full)):
            old_file_path = path_list_full[i]  # 老图片 路径短名
            print("old_file_path:", old_file_path)

            # 这是老文件
            file_path = old_file_path
            old_file_path_list = [os.path.join(file_path, j) for j in os.listdir(file_path)]  # 老图片 文件全名
            print("old_file_path_list:", old_file_path_list)

            pic_len = len(old_file_path_list)

            # 这是新文件
            zen = path_list_full[i]
            m = re.findall("\d+", zen)[0]  # 会匹配所有数字
            # print("m:",m)

            # 不能保证 每个一文件夹 数字都是一位 所以需要正则表达式
            # new_file_path = path_list_full[i][:-1] + str(org_num)+"-"+str(org_num+pic_len-1)  # 文件短名
            new_file_path = path_list_full[i][:-len(str(m))] + str(org_num) + "-" + str(org_num + pic_len - 1)  # 文件短名

            # 解决了 25415-25424 问题
            print("new_file_path:", new_file_path)

            # 这是新文件
            # file_path = new_file_path
            # new_file_path_list = [os.path.join(file_path, j) for j in os.listdir(file_path)]  # 文件全名

            # num_pic_i_count = 0 # 记录图片迭代位置
            for k in range(len(old_file_path_list)):
                old_pic = old_file_path_list[k]
                # print(old_pic)
                new_pic = str(org_num + k) + old_pic.split(os.sep)[-1]  # 25525red.jpg
                new_pic = os.path.join(os.path.dirname(old_pic), new_pic)
                # print("new_pic:", new_pic)
                os.rename(old_pic, new_pic)
                print("{}--->\n{}".format(old_pic, new_pic))

            os.rename(old_file_path, new_file_path)
            print("{}--->\n{}".format(old_file_path, new_file_path))
            org_num = org_num + pic_len

    # 文件夹序号重命名 并且 排序
    rename_dir_1_2_3(path_fu)

    # 去除额外的字符串
    remove_str = ['-removebg-preview','_','0','1','2','3','4','5','6','7','8','9']  # 这个就是需要去除的字符串列表  元素数量任意
    remove_pic_str(path_fu, *remove_str)

    # 数据干净了  直接设置编号
    # bian_hao_start = 80000
    bianhao()



if __name__ == '__main__':
    bian_hao_start = 85000
    path_fu = r"C:\Users\Administrator\Desktop\xxxx"
    set_bianhao(path_fu, bian_hao_start)