import wx

class PySimpleApp(wx.App):
  def __init__(self, redirect=False, filename=None, useBestVisaul=False, clearSigInt=True):
    wx.App.__init__(self, redirect, filename, useBestVisaul, clearSigInt)
    self.frame = wx.Frame(parent=None, title='Spare')
    self.frame.Show()
    self.SetTopWindow(self.frame)

  def OnInit(self):
    return True

if __name__ == '__main__':
    app = PySimpleApp()
    app.MainLoop()