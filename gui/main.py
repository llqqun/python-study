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
        # 创建一个面板
        pnl = wx.Panel(self)
         # 绑定鼠标右键事件
        pnl.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        # 在面板上添加一个静态文本
        st = wx.StaticText(pnl, label="Hello World!")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # 创建一个垂直布局的盒子
        # sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        # pnl.SetSizer(sizer)

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
            img = wx.Image(img_path, wx.BITMAP_TYPE_PNG)
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