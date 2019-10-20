from interface import user_interface
from lib import common
user_info = {'user':None}

def register():
    while True:
        if  user_info.get('user'):
            print('您已登录')
            break

        user = input('请输入用户名:').strip()
        pwd = input('请输入密码:').strip()
        re_pwd = input('请确认密码:').strip()

        if pwd != re_pwd:
            print('两次密码不一致')
            break

        msg = user_interface.register_interface(user,pwd)
        print(msg)
        break


def login():

    while True:
        if user_info.get('user'):
            print('您已登录')
            break

        user = input('请输入用户名:').strip()
        pwd = input('请输入密码:').strip()

        flag,msg = user_interface.login_interface(user,pwd)
        print(msg)
        if flag:
            user_info['user'] = user
        break

@common.deco
def check_file():
    while True:
        flag,file_list = user_interface.check_file_interface(user_info.get('user'))

        if not flag:
            print(file_list)
            break

        for index,file in enumerate(file_list):
            print(index,file)

        choice = input('请选择要下载的文件,q退出:').strip()

        if choice =='q':
            break

        if not choice.isdigit():
            print('请输入数字')
            continue

        choice = int(choice)

        if choice not in range(len(file_list)):
            print('请输入正确编号')
            continue
        file_name = file_list[choice]

        path = input('请输入下载的路径,默认为桌面:').strip()
        msg = user_interface.download_interface(file_name,path)
        print(msg)
        break


@common.deco
def upload():
    while True:
        dir_path = input('请输入文件路径:').strip()
        msg = user_interface.upload_interface(dir_path,user_info.get('user'))
        print(msg)
        break

def run():
    func = {
        '1':register,
        '2':login,
        '3':check_file,
        '4':upload
    }
    while True:
        print('''
        欢迎来到wick网盘
        1 注册
        2 登录
        3 查看网盘文件
        4 上传
        q 退出''')

        choice = input('请选择功能:').strip()



        if choice =='q':
            break
        if choice not in func:
            print('请输入正确编号')
            continue

        func.get(choice)()






