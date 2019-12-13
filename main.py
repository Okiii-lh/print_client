# coding=utf-8
"""
@File    :   main.py    
@Contact :   13132515202@163.com

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2019/12/12 21:58   LiuHe      1.0         远程打印客户端
"""
import os
import socket
import wx


def client():
    def __init__(self):
        wx.Frame.__init__(self, None, title='SiteLog', size=(640, 480))
        self.SelBtn = wx.Button(self, label='>>', pos=(305, 5), size=(80, 25))
        self.SelBtn.Bind(wx.EVT_BUTTON, self.OnOpenFile)
        self.OkBtn = wx.Button(self, label='OK', pos=(405, 5), size=(80, 25))
        self.OkBtn.Bind(wx.EVT_BUTTON, self.ReadFile)
        self.FileName = wx.TextCtrl(self, pos=(5, 5), size=(230, 25))
        self.FileContent = wx.TextCtrl(self, pos=(5, 35), size=(620, 480),
                                       style=(wx.TE_MULTILINE))

    def OnOpenFile(self, event):
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(None, 'select', os.getcwd(), '', wildcard,
                               wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.FileName.SetValue(dialog.GetPath())
            dialog.Destroy

    def ReadFile(self, event):
        file = open(self.FileName.GetValue())
        self.FileContent.SetValue(file.read())
        file.close()


def conn():
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
        file_info = 'post|%s|%s' % (file_name, file_size)
        sk.sendall(bytes(file_info, 'utf-8'))

        has_sent = 0
        with open(path, 'rb') as fp:
            while has_sent != file_size:
                data = fp.read(1024)
                sk.sendall(data)

                has_sent += len(data)

                print('\r' + '[上传进度]：%s%.02f%%' % (
                '>' * int((has_sent / file_size) * 50),
                float(has_sent / file_size) * 100), end='')
        print()
        print("%s上传成功" % file_name)


if __name__ == "__main__":
    app = wx.App()
    site_frame = client()
    site_frame.Show()
    app.MainLoop()