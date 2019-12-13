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


class sockte_conn():
    pass

class mainFrame(wx.Frame):
    """
    程序主窗口类，继承字wx.Frame
    """

    def __init__(self):
        """
        构造函数
        """
        wx.Frame.__init__(self, None, -1, APP_TITLE,
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((500, 500))
        self.Center()

        # 以下代码处理图标
        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # 以下可以添加各类控件
        pass

    # def conn(self):
    #     IP_PORT = ('127.0.0.1', 9999)
    #
    #     sk = socket.socket()
    #
    #     sk.connect(IP_PORT)
    #
    #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #
    #     while True:
    #         inp = input('>>>').strip()
    #         cmd, path = inp.split('|')
    #
    #         path = os.path.join(BASE_DIR, path)
    #         file_name = os.path.basename(path)
    #         file_size = os.stat(path).st_size
    #         file_info = 'post|%s|%s' % (file_name, file_size)
    #         sk.sendall(bytes(file_info, 'utf-8'))
    #
    #         has_sent = 0
    #         with open(path, 'rb') as fp:
    #             while has_sent != file_size:
    #                 data = fp.read(1024)
    #                 sk.sendall(data)
    #
    #                 has_sent += len(data)
    #
    #                 print('\r' + '[上传进度]：%s%.02f%%' % (
    #                     '>' * int((has_sent / file_size) * 50),
    #                     float(has_sent / file_size) * 100), end='')
    #         print()
    #         print("%s上传成功" % file_name)


class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame()
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp(redirect=True)
    app.MainLoop()




