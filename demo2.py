
#-*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        模块mainFrame
# Purpose:     应用程序的主界面
#
# Author:      ankier
#
# Created:     28-10-2012
# Copyright:   (c) ankier 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx
import os

## @detail MainFrame主界面窗口类
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,  'FileDialog study', pos=wx.DefaultPosition,
            size=(800, 600), style=wx.DEFAULT_FRAME_STYLE)
        self.CreateStatusBar()
        self.__BuildMenus() 
        
        label = wx.StaticText(self, -1, u"当前选择的文件")
        textBox = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE, size =(-1, 300))    
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, wx.ALL|wx.ALIGN_CENTRE)
        sizer.Add(textBox, 1, wx.ALL|wx.ALIGN_CENTRE)
        self.__TextBox = textBox
        self.SetSizerAndFit(sizer)
        
    def __BuildMenus(self):
        mainMenuBar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        
        fileMenuItem = fileMenu.Append(-1, "打开单个文件")
        self.Bind(wx.EVT_MENU, self.__OpenSingleFile, fileMenuItem)
        
        saveMenuItem = fileMenu.Append(-1, "保存文件")
        self.Bind(wx.EVT_MENU, self.__SaveFile, saveMenuItem)
        
        savePromptMenuItem = fileMenu.Append(-1, "保存文件及提示覆盖")
        self.Bind(wx.EVT_MENU, self.__SavePromptFile, savePromptMenuItem)
        
        multipleOpenMenuItem = fileMenu.Append(-1, "多文件选择")
        self.Bind(wx.EVT_MENU, self.__MultipleSelectFiles, multipleOpenMenuItem)
        
        mainMenuBar.Append(fileMenu, title =u'&文件')
        
        self.SetMenuBar(mainMenuBar)
   
    ## @detail wx.FileDialog style：wx.FD_OPEN
    def __OpenSingleFile(self, event):
        filesFilter = "Dicom (*.dcm)|*.dcm|" "All files (*.*)|*.*"
        fileDialog = wx.FileDialog(self, message ="选择单个文件", wildcard = filesFilter, style = wx.FD_OPEN)
        dialogResult = fileDialog.ShowModal()
        if dialogResult !=  wx.ID_OK:
            return
        path = fileDialog.GetPath()
        self.__TextBox.SetLabel(path)
        
    ## @detail wx.FileDialog style：wx.FD_SAVE
    def __SaveFile(self, event):
        filesFilter = "Dicom (*.dcm)|*.dcm|" "All files (*.*)|*.*"
        fileDialog = wx.FileDialog(self, message ="保存文件", wildcard = filesFilter, style = wx.FD_SAVE)
        dialogResult = fileDialog.ShowModal()
        if dialogResult !=  wx.ID_OK:
            return
        path = fileDialog.GetPath()
        self.__TextBox.SetLabel(path)
    
    ## @detail wx.FileDialog style：wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
    def __SavePromptFile(self, event):
        filesFilter = "Dicom (*.dcm)|*.dcm|" "All files (*.*)|*.*"
        fileDialog = wx.FileDialog(self, message ="保存&prompt文件", wildcard = filesFilter, style = wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        dialogResult = fileDialog.ShowModal()
        if dialogResult !=  wx.ID_OK:
            return
        path = fileDialog.GetPath()
        self.__TextBox.SetLabel(path)        
    
    ## @detail wx.FileDialog style：wx.FD_OPEN | wx.FD_MULTIPLE
    def __MultipleSelectFiles(self, event):
        filesFilter = "Dicom (*.dcm)|*.dcm|" "All files (*.*)|*.*"
        fileDialog = wx.FileDialog(self, message ="多文件选择", wildcard = filesFilter, style = wx.FD_OPEN|wx.FD_MULTIPLE)
        dialogResult = fileDialog.ShowModal()
        if dialogResult !=  wx.ID_OK:
            return
        paths = fileDialog.GetPaths()
        self.__TextBox.SetLabel('')
        for path in paths:
            self.__TextBox.AppendText(path+'\n')
        
        