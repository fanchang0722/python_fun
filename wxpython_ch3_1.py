#  Copyright 2014 Google Inc. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import wx
import subprocess as sub
import time

class MyFrame(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, 'Frame With Button', size=(300, 100))
		panel = wx.Panel(self, -1)
		button = wx.Button(panel, -1, "Compute GRR", pos=(130, 15), size=(100, 30))
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)

	def OnCloseMe(self, event):
		print "Here you go"
		# time.sleep(5)
		# self.Close(True)

	def OnCloseWindow(self, event):
		print "Here you go"
		time.sleep(5)
		self.Destroy()


if __name__ == '__main__':
	app = wx.App()
	frame = MyFrame(parent=None, id=-1)
	frame.Show(True)
	app.MainLoop()
