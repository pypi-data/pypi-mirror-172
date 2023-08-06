r"""
这个模块的作用 是批量更改图片和文件夹的名字
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
import os
import re
import shutil



def re_pic_name(path_fu, org_num):
    path_list = os.listdir(path_fu)
    path_list.sort(key=lambda x:int(x), reverse = False)  # path_list ['1', '2', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    # print("path_list", path_list)

    path_list_full = [os.path.join(path_fu, i) for i in path_list] # ['C:\\Users\\Administrator\\Desktop\\all\\1', 'C:\\Users\\Administrator\\Desktop\\all\\2']
    # print("path_list_full", path_list_full)

    for i in range(len(path_list_full)):
        old_file_path= path_list_full[i]
        print("old_file_path:", old_file_path)

        # 这是老文件
        file_path = old_file_path
        old_file_path_list = [os.path.join(file_path,j) for j in os.listdir(file_path)]  # 文件全名
        print("old_file_path_list:", old_file_path_list)
        pic_len = len(old_file_path_list)

        # 这是新文件
        zen = path_list_full[i]
        m = re.findall("\d+", zen)[0]  # 会匹配所有数字
        # print("m:",m)

        # 不能保证 每个一文件夹 数字都是一位 所以需要正则表达式
        # new_file_path = path_list_full[i][:-1] + str(org_num)+"-"+str(org_num+pic_len-1)  # 文件短名
        new_file_path = path_list_full[i][:-len(str(m))] + str(org_num)+"-"+str(org_num+pic_len-1)  # 文件短名

        # 解决了 25415-25424 问题
        print("new_file_path:", new_file_path)


        # 这是新文件
        # file_path = new_file_path
        # new_file_path_list = [os.path.join(file_path, j) for j in os.listdir(file_path)]  # 文件全名

        # num_pic_i_count = 0 # 记录图片迭代位置
        for k in range(len(old_file_path_list)):
            old_pic = old_file_path_list[k]
            # print(old_pic)
            new_pic = str(org_num+k)+old_pic.split(os.sep)[-1]  # 25525red.jpg
            new_pic = os.path.join(os.path.dirname(old_pic), new_pic)
            # print("new_pic:", new_pic)
            os.rename(old_pic, new_pic)
            print("{}--->\n{}".format(old_pic, new_pic))

        os.rename(old_file_path, new_file_path)
        print("{}--->\n{}".format(old_file_path,new_file_path))
        org_num = org_num + pic_len


r"""
            #if len(k.split(os.sep)[-1])> len("20265blue.jpeg")+8:
                #print(k)
"""

# .sort()
# path_fu = r"C:\Users\Administrator\Desktop\原图"
path_fu = r"C:\Users\Administrator\Desktop\xxx\xxx"  # 这个是图片大根目录
org_num = 83000  # 这个是图片的初始值
re_pic_name(path_fu, org_num)

# 注意 我这个版本不能路径中不能出现数字  出现数字就会数据混乱！！！！