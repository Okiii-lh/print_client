# coding=utf-8
"""
@File    :   main.py    
@Contact :   13132515202@163.com

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2019/12/12 21:58   LiuHe      1.0         客户端
"""
import os
import socket


def client():
    IP_PORT = ('127.0.0.1', 9999)

    sk = socket.socket()

    sk.connect(IP_PORT)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    while True:
        inp = input('>>>').strip()
        cmd, path = inp.split('|')

        path = os.path.join(BASE_DIR, path)
        file_name = os.path.basename(path)
        file_size = os.stat(path).st_size
        file_info = 'post|%s|%s'%(file_name, file_size)
        sk.sendall(bytes(file_info, 'utf-8'))

        has_sent = 0
        with open(path, 'rb') as fp:
            while has_sent != file_size:
                data = fp.read(1024)
                sk.sendall(data)

                has_sent += len(data)

                print('\r'+'[上传进度]：%s%.02f%%'%('>'*int((has_sent/file_size)*50),
                                               float(has_sent/file_size)*100), end='')
        print()
        print("%s上传成功"%file_name)


if __name__ == "__main__":
    client()