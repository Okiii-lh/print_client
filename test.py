import wx
import win32api
import sys, os

APP_TITLE = u'远程打印机'
APP_ICON = 'icon/print.ico'


class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    id_open = wx.NewId()
    id_save = wx.NewId()
    id_quit = wx.NewId()

    id_help = wx.NewId()
    id_about = wx.NewId()

    def __init__(self, parent):
        '''构造函数'''

        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((300, 300))
        self.Center()

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)

        self._CreateMenuBar()  # 菜单栏
        self._CreateStatusBar()  # 状态栏

    def _CreateMenuBar(self):
        '''创建菜单栏'''

        self.mb = wx.MenuBar()

        # 文件菜单
        m = wx.Menu()
        m.Append(self.id_open, u"打开文件")
        m.Append(self.id_save, u"保存文件")
        m.AppendSeparator()
        m.Append(self.id_quit, u"退出系统")
        self.mb.Append(m, u"文件")

        self.Bind(wx.EVT_MENU, self.OnOpen, id=self.id_open)
        self.Bind(wx.EVT_MENU, self.OnSave, id=self.id_save)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=self.id_quit)

        self.SetMenuBar(self.mb)


    def _CreateStatusBar(self):
        '''创建状态栏'''

        self.sb = self.CreateStatusBar()
        self.sb.SetFieldsCount(3)
        self.sb.SetStatusWidths([-2, -1, -1])
        self.sb.SetStatusStyles([wx.SB_RAISED, wx.SB_RAISED, wx.SB_RAISED])

        self.sb.SetStatusText(u'状态信息0', 0)
        self.sb.SetStatusText(u'', 1)
        self.sb.SetStatusText(u'状态信息2', 2)

    def OnOpen(self, evt):
        '''打开文件'''

        self.sb.SetStatusText(u'打开文件', 1)

    def OnSave(self, evt):
        '''打印'''

        self.sb.SetStatusText(u'打印', 1)

    def OnQuit(self, evt):
        '''退出系统'''

        self.sb.SetStatusText(u'退出系统', 1)
        self.Destroy()


class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame(None)
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
