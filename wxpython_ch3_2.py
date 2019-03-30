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


class MenuEventFrame(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, 'Menus', size=(300, 300))
		menuBar = wx.MenuBar()
		menu1 = wx.Menu()
		menuItem1 = menu1.Append(-1, "&Exit")
		menu2 = wx.Menu()
		menuItem2 = menu2.Append(-1, "&Test")
		menuBar.Append(menu1, "&File")
		menuBar.Append(menu2, "&Fan")
		self.SetMenuBar(menuBar)
		self.Bind(wx.EVT_MENU, self.OnCloseMe, menuItem1)

	def OnCloseMe(self, event):
		self.Close(True)

if __name__ == '__main__':
	app = wx.App()
	frame = MenuEventFrame(parent=None, id=-1)
	frame.Show()
	app.MainLoop()

