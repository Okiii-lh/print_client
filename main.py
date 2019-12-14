# coding=utf-8
"""
@File    :   main.py
@Contact :   13132515202@163.com

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2019/12/12 22:39   LiuHe      1.0         远程打印客户端实现
"""
import wx
import win32api
import sys, os
import socket
import chardet
import codecs


# TODO 多文件打印
# TODO 实时显示打印机状态
# TODO 添加打印份数功能

APP_TITLE = u'远程打印机'
APP_ICON = 'icon/print.ico'

HOST = '127.0.0.1'
PORT = 9999
MAX_SIZE = 1024*1024


class MainFrame(wx.Frame):
    """
    程序主窗口类，继承字wx.Frame
    """

    exc_print = wx.NewId()
    id_quit = wx.NewId()
    open_single_file = wx.NewId()
    open_muti_file = wx.NewId()

    def __init__(self, parent):
        """
        构造函数
        :param parent:
        """

        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((300, 300))
        self.Center()
        self.files_path = None

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exe_name = win32api.GetModuleFileName(
                win32api.GetModuleHandle(None))
            icon = wx.Icon(exe_name, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)

        self._create_menu_bar()  # 菜单栏
        self._create_status_bar()  # 状态栏

        label = wx.StaticText(self, -1, u"当前选择的文件")
        textBox = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(600, 400))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTRE)
        sizer.Add(textBox, 1, wx.ALL | wx.ALIGN_CENTRE)
        self.__TextBox = textBox
        self.SetSizerAndFit(sizer)

    def _create_menu_bar(self):
        """
        创建菜单栏
        :return:
        """

        self.mb = wx.MenuBar()

        # 文件菜单
        m = wx.Menu()
        m.Append(self.open_single_file, u"打印单个文件")
        m.Append(self.open_muti_file, u"打印多个文件")
        m.Append(self.exc_print, u"执行打印")
        m.AppendSeparator()
        m.Append(self.id_quit, u"退出系统")

        self.mb.Append(m, u"文件")

        self.Bind(wx.EVT_MENU, self._open_single_file, id=self.open_single_file)
        self.Bind(wx.EVT_MENU, self._exc_print, id=self.exc_print)
        self.Bind(wx.EVT_MENU, self._open_muti_file, id=self.open_muti_file)
        self.Bind(wx.EVT_MENU, self._on_quit, id=self.id_quit)

        self.SetMenuBar(self.mb)

    def _create_status_bar(self):
        """
        创建状态栏
        :return:
        """

        self.sb = self.CreateStatusBar()
        self.sb.SetFieldsCount(3)
        self.sb.SetStatusWidths([-2, -1, -1])
        self.sb.SetStatusStyles([wx.SB_RAISED, wx.SB_RAISED, wx.SB_RAISED])

        self.sb.SetStatusText(u'状态信息0', 0)
        self.sb.SetStatusText(u'', 1)
        self.sb.SetStatusText(u'状态信息2', 2)

    def _exc_print(self, event):
        """
        执行打印
        :return:
        """
        # 建立连接
        try:
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.connect((HOST, PORT))
        except Exception as e:
            wx.MessageBox("打印机连接失败", "错误", wx.OK | wx.ICON_INFORMATION)
            return

        if self.files_path == None:
            wx.MessageBox("未选取打印文件", "错误", wx.OK | wx.ICON_INFORMATION)
            return
        elif type(self.files_path) == str:
            self.__TextBox.SetLabel('')
            self.__TextBox.AppendText("正在打印...")
            self._socket_upload_file(sk, self.files_path)
            print("上传完成")
            sk.close()
        else:
            print("打印多个文件")
        self.sb.SetStatusText(u'打印', 1)

    def _on_quit(self, evt):
        """
        退出系统
        :param evt:
        :return:
        """
        self.sb.SetStatusText(u'退出系统', 1)
        self.Destroy()

    def _open_single_file(self, event):
        """
        选中单个文件
        :param event:
        :return:
        """
        files_filter = "All files (*.*)|*.*"
        file_dialog = wx.FileDialog(self, message="选择单个文件",
                                    wildcard=files_filter,
                                    style=wx.FD_OPEN)
        dialog_result = file_dialog.ShowModal()
        if dialog_result != wx.ID_OK:
            return
        path = file_dialog.GetPath()
        self.files_path = path
        self.sb.SetStatusText(u'选择单个文件', 1)
        self.__TextBox.SetLabel(path)

    def _open_muti_file(self, event):
        """
        选择多个文件
        :return:
        """
        files_filter = "All files (*.*)|*.*"
        file_dialog = wx.FileDialog(self, message="多文件选择",
                                    wildcard=files_filter,
                                    style=wx.FD_OPEN | wx.FD_MULTIPLE)
        dialog_result = file_dialog.ShowModal()
        if dialog_result != wx.ID_OK:
            return
        paths = file_dialog.GetPaths()
        self.files_path = paths
        self.__TextBox.SetLabel('')
        for path in paths:
            self.__TextBox.AppendText(path + '\n')

    def _socket_upload_file(self, sk, filepath):
        """
        上传文件
        :param self:
        :param sk: socket实例
        :param filepath: 文件路径
        :return:
        """
        file_name = os.path.basename(filepath)
        file_size = os.stat(filepath).st_size
        file_info = 'post|%s|%s' % (file_name, file_size)
        sk.sendall(bytes(file_info, 'utf-8'))

        has_sent = 0
        with open(filepath, 'rb') as fp:
            while has_sent != file_size:
                data = fp.read(1024)
                sk.sendall(data)

                has_sent += len(data)

                print('\r' + '[上传进度]：%s%.02f%%' % (
                        '>' * int((has_sent / file_size) * 50),
                        float(has_sent / file_size) * 100), end='')
        print()
        print("%s上传成功" % file_name)

    def _change_file_unicode_to_utf8(self, file_unicode, file_path):
        """
        将文件编码修改未utf8格式
        :param file_unicode: 文件原编码格式
        :param file_path: 文件路径
        :return:
        """
        in_enc = file_unicode.upper()
        out_enc = "UTF-8"

        try:
            f = codecs.open(file_path, 'r', in_enc)
            new_content = f.read()
            codecs.open(file_path, 'w', out_enc).write(new_content)
        except IOError as err:
            print("文件格式转换错误")

    def _get_encoding(self, file_path):
        """
        获取文件原编码格式
        :param file_path: 文件路径
        :return:
        """
        with open(file_path, 'rb') as f:
            return chardet.detect(f.read())['encoding']


class MainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = MainFrame(None)
        self.Frame.Show()
        return True


class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(MyDialog, self).__init__(parent, title=title, size=(50, 50))
        panel = wx.Panel(self)
        self.btn = wx.Button(panel, wx.ID_OK, label='ok', size=(50, 25), pos=(75, 50))


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
