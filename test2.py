# coding=utf-8
"""
@File    :   test2.py    
@Contact :   13132515202@163.com

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2019/12/13 14:44   LiuHe      1.0         None
"""

import time
import wx
import socket
#import sys
import threading
import struct
#import logging
#logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')

#Receive message
class Receiver(threading.Thread):
    def __init__(self,threadName,window):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        #连接服务器
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            self.sock.connect((self.window.host, self.window.port))
            self.window.LogMessage("连接服务器成功...\n")
            self.runT = True
        except Exception:
            self.window.LogMessage("连接服务器失败...\n")
            self.sock.close()

    def stop(self):
        self.window.LogMessage("关闭Socket连接...\n")
        self.sock.close()
        self.runT = False
        self.timeToQuit.set()

    def sendMsg(self,msg):
        logMsg = (u"发送：%s\n" % (msg))
        self.window.LogMessage(logMsg)
        self.sock.sendall(msg)

    def run(self):
        try:
            while self.runT:
                data = self.sock.recv(4)
                if data:
                    dataLen, = struct.unpack_from("i",data)
                    wx.CallAfter(self.window.LogMessage,(u"返回数据长度:%s\n" % (dataLen)))
                    wx.CallAfter(self.window.LogMessage,(u"返回数据:%s\n" % (self.sock.recv(dataLen))))
        except Exception:
            pass
class InsertFrame(wx.Frame):

    def __init__(self, parent, id):

        #创建父框
        wx.Frame.__init__(self, parent, id, 'Socket Client', size=(640, 450))
        #创建画板
        self.panel = wx.Panel(self,-1)
        self.panel.SetBackgroundColour("White")
        #创建按钮
        self.createButtonBar(self.panel)
        #创建静态文本
        self.createTextFields(self.panel)
        #创建文本框
        self.creatTextInput(self.panel)

        #Socket 地址
        self.host, self.port = "localhost", 12340
        self.runT = True
###############################
    #创建文本
    def createTextFields(self, panel):
        for eachLabel, eachPos in self.textFieldData():
            self.createCaptionedText(panel, eachLabel, eachPos)

    def createCaptionedText(self, panel, label, pos):
        static = wx.StaticText(panel, wx.NewId(), label, pos)
        static.SetBackgroundColour("White")
#########################
    #创建按钮
    def createButtonBar(self, panel):
        for eachLabel,eachSize,eachPos, eachHandler in self.buttonData():
            self.buildOneButton(panel, eachLabel,eachSize,eachHandler,eachPos)
    def buildOneButton(self, parent, label,buttonsize,handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos,buttonsize)
        #绑定按钮的单击事件
        self.Bind(wx.EVT_BUTTON, handler, button)
#########################
    #按钮栏数据
    def buttonData(self):#(按钮名称，按钮大小，按钮坐标，按钮事件）
        return (("连 接",(50, 25),(310, 30),self.OnConnection),
                ("断 开", (50, 25),(370, 30),self.OnCloseSocket),
                ("清 空", (50, 25),(430, 30),self.OnClearLog),
                ("发 送", (50, 25),(540, 400),self.OnSend))
    #文本内容
    def textFieldData(self):
        return (("Please Input socket address AND port：", (10, 10)),
                ("输入消息：", (10, 380)))
########################
    #创建文本框
    def creatTextInput(self,panel):
        #服务器地址输入框
        self.socketHostText = wx.TextCtrl(self.panel, wx.NewId(), "", size=(230, 25),pos=(10, 30))
        #服务器端口输入框
        self.socketPortText = wx.TextCtrl(self.panel, wx.NewId(), "", size=(50, 25),pos=(250, 30))
        #信息显示
        self.log = wx.TextCtrl(self.panel, -1, "",size=(620, 310),pos=(10, 60),style=wx.TE_RICH|wx.TE_MULTILINE|wx.TE_READONLY)
        #信息输入
        self.inputMessage = wx.TextCtrl(self.panel, wx.NewId(), size=(520, 25),style=wx.TE_PROCESS_ENTER,pos=(10, 400))
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSend, self.inputMessage)
########################

    #事件处理器(关闭窗口）
    def OnCloseWindow(self, event):
        self.thread.stop()
        self.Destroy()

    #事件处理器(关闭Socket）
    def OnCloseSocket(self, event):
        self.thread.stop()

    #事件处理器(连接到SOCKET）
    def OnConnection(self,event):
        if self.socketHostText.GetValue()!='' and self.socketPortText.GetValue()!='':
            self.host, self.port = str(self.socketHostText.GetValue()),int(self.socketPortText.GetValue())
        threadName = "socketclient"
        self.thread = Receiver(threadName, self)#创建一个线程
        self.thread.setDaemon(True)
        self.thread.start()#启动线程

    #事件处理器(显示LOG）
    def LogMessage(self, msg):#注册一个消息
        self.log.AppendText(msg)

    #事件处理器(清空LOG）
    def OnClearLog(self,event):#注册一个消息
        self.log.Clear()

    #事件处理器(给SOCKET发送消息,并清空输入框）
    def OnSend(self, event):
        self.thread.sendMsg(self.inputMessage.GetValue())
        self.inputMessage.Clear()



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = InsertFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()