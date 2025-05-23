import wx
import wx.aui
import os
import configparser
import sys
class MainFrame(wx.Frame):
    dirPath = ""
    img_path = ""
    options = {}
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw, size=(600, 400))

        self.config = self.load_ini_config()

        self.Centre()

        # 创建一个垂直布局的盒子
        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        # pnl.SetSizer(sizer)
        self.layout()
        # 创建一个菜单栏
        self.makeMenuBar()

        # 创建一个工具栏
        self.createtoolbar()

        # 创建一个状态栏
        # self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")

    def load_ini_config(self):
        # 获取应用程序的当前工作目录
        self.dirPath = os.path.dirname(os.path.abspath(__file__))
        ini_path = os.path.join(self.dirPath, "settings.ini")
        config = configparser.ConfigParser()
        if not os.path.exists(ini_path):
            print(f"配置文件未找到: {ini_path}")
            return
        config.read(ini_path, encoding="utf-8")
        # 打印所有 section 和 key-value
        for section in config.sections():
            for key, value in config.items(section):
                self.options[key] = value
        print(f'读取配置文件{self.options}')
        return config

    def layout(self):
        panel = wx.Panel(self)
        self.LoadImages(panel)
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Class Name')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel)
        hbox1.Add(tc, proportion=1)
        st2 = wx.StaticText(panel, label='测试')
        hbox1.Add(st2, flag=wx.LEFT, border=8)

        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Matching Classes')
        st2.SetFont(font)
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=10)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.CheckBox(panel, label='Case Sensitive')
        cb1.SetFont(font)
        hbox4.Add(cb1)
        cb2 = wx.CheckBox(panel, label='Nested Classes')
        cb2.SetFont(font)
        hbox4.Add(cb2, flag=wx.LEFT, border=10)
        cb3 = wx.CheckBox(panel, label='Non-Project classes')
        cb3.SetFont(font)
        hbox4.Add(cb3, flag=wx.LEFT, border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)

        return None

    def LoadImages(self, panel):
        self.mincol = wx.StaticBitmap(panel, wx.ID_ANY,
            self.setImage('1.jpg', 200, 200))
        self.mincol.SetPosition((50, 50))

    def makeMenuBar(self):
        # 创建一个菜单栏对象
        menuBar = wx.MenuBar()
        # 创建一个菜单对象 
        fileMenu = wx.Menu()
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        # 创建一个分割线
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # 创建一个自定义菜单项
        customMenu = wx.Menu()
        search = wx.MenuItem(customMenu, 99, '&搜索\tCtrl-F')
        # 设置菜单项的图标
        search.SetBitmap(self.setImage('search.png', 16, 16))
        # 将菜单项添加到菜单中
        customMenu.Append(search)

        # 创建一个子菜单
        customChildMenu = wx.Menu()
        customChildMenu.Append(wx.ID_ANY, 'Import newsfeed list...')
        customChildMenu.Append(wx.ID_ANY, 'Import bookmarks...')
        customChildMenu.Append(wx.ID_ANY, 'Import mail...')
        customMenu.Append(wx.ID_ANY, 'I&mport', customChildMenu)

        # 创建一个复选菜单项
        self.shst = customMenu.Append(wx.ID_ANY, 'Show statusbar',
            'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = customMenu.Append(wx.ID_ANY, 'Show toolbar',
            'Show Toolbar', kind=wx.ITEM_CHECK)
        
        customMenu.Check(self.shst.GetId(), True)
        customMenu.Check(self.shtl.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.shtl)

        # 创建一个状态栏
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')


        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        menuBar.Append(customMenu, "&自定义")

        self.SetMenuBar(menuBar)

        # 绑定事件处理
        self.Bind(wx.EVT_MENU, self.searchHandler, search)
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def createtoolbar(self):
        # print('createtoolbar:', wx.aui.AUI_TB_DEFAULT_STYLE | wx.aui.AUI_TB_TEXT)
        # 创建一个工具栏
        self.toolbar = self.CreateToolBar()
        # self.toolbar = wx.aui.AuiToolBar(self, -1, style = wx.aui.AUI_TB_DEFAULT_STYLE | wx.aui.AUI_TB_TEXT)
        self.toolbar.SetBackgroundColour(wx.Colour(220, 220, 250)) 
        search = self.toolbar.AddTool(15, 'Search', self.setImage('search.png'))
        edit = self.toolbar.AddTool(wx.ID_ANY, 'edit', self.setImage('edit.png'))
        self.toolbar.AddSeparator()
        setting = self.toolbar.AddTool(wx.ID_ANY, 'setting', self.setImage('setting.png'))
        # 启用或禁用工具栏按钮
        self.toolbar.EnableTool(15, False)
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, lambda e: print('search'), search)
        self.Bind(wx.EVT_TOOL, lambda e: print('edit'), edit)
        self.Bind(wx.EVT_TOOL, lambda e: print('setting'), setting)

        # 创建多个工具栏
        """ vbox = wx.BoxSizer(wx.VERTICAL)
        toolbar1 = wx.ToolBar(self)
        toolbar1.AddTool(wx.ID_ANY, '', self.setImage('search.png'))
        toolbar1.AddTool(wx.ID_ANY, '', self.setImage('setting.png'))
        toolbar1.AddTool(wx.ID_ANY, '', self.setImage('edit.png'))
        toolbar1.Realize()

        toolbar2 = wx.ToolBar(self)
        qtool = toolbar2.AddTool(wx.ID_EXIT, '', self.setImage('check.png'))
        toolbar2.Realize()

        vbox.Add(toolbar1, 0, wx.EXPAND)
        vbox.Add(toolbar2, 0, wx.EXPAND)

        self.Bind(wx.EVT_TOOL, lambda e: print('tool'), qtool)

        self.SetSizer(vbox) """
        return None

    def ToggleStatusBar(self, event):
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, event):
        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    def setImage(self, img, width = 16, height = 16):
        img_path = os.path.join(self.dirPath, self.options['imgpath'], img)
        if os.path.exists(img_path):
            # 先用 wx.Image 读取并缩放，再转为 wx.Bitmap
            img = wx.Image(img_path, wx.BITMAP_TYPE_ANY)
            img = img.Scale(width, height, wx.IMAGE_QUALITY_HIGH)  # 这里设置你想要的宽高
            return wx.Bitmap(img)
        else:
            print(f"Warning: Icon file not found at {img_path}")
            return None

    def searchHandler(self, event):
        print("searchHandler")

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)

    def OnRightDown(self, event):
        print("OnRightDown")
        popup = wx.Menu()
        mmi = wx.MenuItem(popup, wx.NewId(), 'Minimize')
        popup.Append(mmi)
        self.Bind(wx.EVT_MENU, lambda evt: self.Iconize(), mmi)

        cmi = wx.MenuItem(popup, wx.NewId(), 'Close')
        popup.Append(cmi)
        self.Bind(wx.EVT_MENU, lambda evt: self.Close(), cmi)
        self.PopupMenu(popup, event.GetPosition())
        return None

# 定义全局异常钩子函数
def global_exception_hook(exctype, value, traceback):
    # 这里可以自定义日志记录、弹窗等
    print("全局异常捕获：", exctype, value)
    wx.MessageBox(f"程序运行异常：{value}", "错误", wx.OK | wx.ICON_ERROR)

# 将全局异常钩子设置为自定义的函数
sys.excepthook = global_exception_hook
if __name__ == '__main__':
    app = wx.App()
    # frm = wx.Frame(None, title="Hello WxPython")
    frm = MainFrame(None, title="Hello WxPython")
    frm.Show()
    app.MainLoop()