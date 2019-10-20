from interface import common_interface
from db import models
import json
import struct
import socket
import os
def register_interface(user,pwd):
    user_obj = models.User.select(user)

    if user_obj:
        return '用户已存在'
    models.User(user,common_interface.encrypt(pwd))

    return f'{user}注册成功'


def login_interface(user,pwd):
    user_obj = models.User.select(user)

    if not user_obj:
        return False,'用户不存在'
    if user_obj.pwd != common_interface.encrypt(pwd):
        return False,'密码错误'

    return True,f'{user}登陆成功'


def upload_interface(file_path,user):
    file_name = os.path.abspath(file_path).rsplit('\\')[-1]

    user_obj = models.User.select(user)

    if file_name in user_obj.file_list:
        return '文件已存在'

    client  =socket.socket()
    client.connect(('127.0.0.1',9527))

    client.send('4'.encode('utf-8'))

    with open(file_path,'rb')as f:
        file_data = f.read()

    file_dic = {'file_name':file_name,'length':len(file_data)}

    json_dic = json.dumps(file_dic)
    byte_json = json_dic.encode('utf-8')

    headers = struct.pack('i',len(json_dic))

    client.send(headers)

    client.send(byte_json)

    init_data = 0
    with open(file_path,'rb')as f:
        while init_data < len(file_data):
            data = f.read(1024)
            client.send(data)
            init_data += len(data)
        msg = client.recv(1024).decode('utf-8')

    user_obj.upload_file(file_name)

    client.close()
    return msg


def check_file_interface(user):

    user_obj = models.User.select(user)

    if not user_obj.file_list:
        return False,'请先上传文件'

    return True,user_obj.file_list


def download_interface(file_name,path):
    if not os.path.exists(path):
        return '路径错误,请重新输入'

    client = socket.socket()
    client.connect(('127.0.0.1',9527))

    client.send('3'.encode('utf-8'))

    client.send(file_name.encode('utf-8'))

    headers = client.recv(4)


    data_len = struct.unpack('i', headers)[0]

    byte_json = client.recv(data_len)
    json_dic = byte_json.decode('utf-8')

    file_dic = json.loads(json_dic)

    file_name = file_dic.get('file_name')
    length = file_dic.get('length')
    file_path = os.path.join(path,file_name)
    init_data = 0
    with open(file_path, 'wb')as f:
        while init_data < length:
            data = client.recv(1024)
            f.write(data)
            init_data += len(data)
        msg = client.recv(1024).decode('utf-8')
    return msg


