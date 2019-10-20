import json
import socket
import struct
import os
from conf import settings

def upload(conn):

    headers = conn.recv(4)

    data_len = struct.unpack('i', headers)[0]

    byte_json = conn.recv(data_len)
    json_dic = byte_json.decode('utf-8')

    file_dic = json.loads(json_dic)

    file_name = file_dic.get('file_name')
    length = file_dic.get('length')

    init_data = 0
    msg = f'{file_name}上传成功'
    file_path = os.path.join(settings.DIR_PATH, file_name)
    with open(file_path, 'wb')as f:
        while init_data < length:
            data = conn.recv(1024)
            f.write(data)
            init_data += len(data)
        print(msg)
        conn.send(msg.encode('utf-8'))

def download(conn):
    file_name = conn.recv(1024).decode('utf-8')

    file_path = os.path.join(settings.DIR_PATH,file_name)
    if os.path.exists(file_path):

        with open(file_path,'rb')as f:
            file_data = f.read()

        file_dic = {'file_name': file_name, 'length': len(file_data)}

        json_dic = json.dumps(file_dic)
        byte_json = json_dic.encode('utf-8')

        headers = struct.pack('i', len(json_dic))

        conn.send(headers)

        conn.send(byte_json)

        init_data = 0
        msg = f'{file_name}下载成功'
        with open(file_path, 'rb')as f:
            while init_data < len(file_data):
                data = f.read(1024)
                conn.send(data)
                print(data)
                init_data += len(data)
            conn.send(msg.encode('utf-8'))


def run():
    func = {
        '4': upload,
        '3': download,
    }

    while True:
        server = socket.socket()

        server.bind(('127.0.0.1', 9527))
        server.listen(1)
        conn, addr = server.accept()

        while True:
            try:
                choice = conn.recv(1).decode('utf-8')
                func.get(choice)(conn)
            except Exception:
                break



