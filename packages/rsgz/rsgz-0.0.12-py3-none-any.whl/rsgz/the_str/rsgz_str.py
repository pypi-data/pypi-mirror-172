import random




def rand_title(the_str,n):
    r"""
    返回新的 随机字符串
    the_str = r"Feature,Gorgeous,Fresh,Hot Sale,Simple,Fashion "
    new_title = rand_title(the_str, n=3) # Gorgeous Feature Simple
    """
    the_str = the_str.replace(" ,", ",").replace(", ", ",")
    the_str_list = the_str.split(",")  # ['Feature', 'Gorgeous', 'Fresh', 'Hot Sale', 'Simple', 'Fashion ']
    random.shuffle(the_str_list)
    the_str_list = the_str_list[0:n]
    the_str = ' '.join(the_str_list).title().replace("'S", "'s")
    return the_str.replace("  "," ")


def str_to_list(the_str):
    r"""
    将字符串转化为列表
    the_str = r"Feature,Gorgeous,Fresh"
    the_list = str_to_list(the_str)  # ['Feature', 'Gorgeous', 'Fresh']
    """
    return the_str.split(",")


def list_to_str(the_list, fengefu):
    r"""
    fengefu = " "
    the_list = ["123", "aabb", "jiu_s12", "rsgz"]
    the_str = list_to_str(the_list, fengefu)  # 123 aabb jiu_s12 rsgz
    注意 列表里面不能有数字 如果有请转化为字符串格式
    """
    return fengefu.join(the_list)


if __name__ == '__main__':
    pass