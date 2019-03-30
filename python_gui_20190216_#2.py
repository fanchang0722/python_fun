"""Python Tkinter GUI"""

import Tkinter as tk
import ttk
import ScrolledText
from Tkinter import Menu
import tkMessageBox as mBox

root = tk.Tk()
root.withdraw()
# mBox.showwarning('Python Message Info Box', 'A Python GUI created using tkinter:\nThe year is 2015.')   
mBox.showerror('Python Message Info Box', 'A Python GUI created using tkinter:\nThe year is 2015.')   

