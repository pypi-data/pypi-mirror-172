import os



def dabao():
    pro_dir = str(input("请输入pyproject.toml文件同级目录："))
    pan_fu = pro_dir.split(os.sep)[0]

    dabao_str = r"""
执行了以下命令：
{}
cd {}
py -m build
twine upload dist/*
    """.format(pan_fu, pro_dir)

    os.system("start cmd")
    print(dabao_str)
