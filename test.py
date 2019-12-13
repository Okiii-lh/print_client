import wx
import win32api
import sys, os

APP_TITLE = u'远程打印机'
APP_ICON = 'icon/print.ico'


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

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exe_name = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exe_name, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)

        self._create_menu_bar()  # 菜单栏
        self._create_status_bar()  # 状态栏

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

    def _exc_print(self):
        """
        执行打印
        :return:
        """
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
        file_dialog = wx.FileDialog(self, message="选择单个文件", wildcard=files_filter,
                                   style=wx.FD_OPEN)
        dialog_result = file_dialog.ShowModal()
        if dialog_result != wx.ID_OK:
            return
        path = file_dialog.GetPath()
        print(path)
        self.sb.SetStatusText(u'选择单个文件', 1)
        self.__TextBox.SetLabel(path)

    def _open_muti_file(self, event):
        """
        选择多个文件
        :return:
        """
        files_filter = "All files (*.*)|*.*"
        file_dialog = wx.FileDialog(self, message="多文件选择", wildcard=files_filter,
                                   style=wx.FD_OPEN | wx.FD_MULTIPLE)
        dialog_result = file_dialog.ShowModal()
        if dialog_result != wx.ID_OK:
            return
        paths = file_dialog.GetPaths()
        print(paths)
        self.__TextBox.SetLabel('')
        for path in paths:
            self.__TextBox.AppendText(path + '\n')


class MainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = MainFrame(None)
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()
