from rsgz.tupian.normal import remove_pic_str

path_fu = r"C:\Users\Administrator\Desktop\xxx"  # 这个文件夹里面的所有图片
remove_str = ['_','0','1','2','3','4','5','6','7','8','9']  # 这个就是需要去除的字符串列表  元素数量任意
remove_pic_str(path_fu, *remove_str)