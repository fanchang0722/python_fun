import wx

app = wx.App()
window = wx.Frame(None,  title="wxPython Frame", style=wx.DEFAULT_FRAME_STYLE, pos=(10, 10), size=(800, 600))
panel = wx.Panel(window)
label = wx.StaticText(panel, label="Hello World", pos=(0, 0))
window.Show(True)
app.MainLoop()
