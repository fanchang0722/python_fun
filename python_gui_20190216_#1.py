"""Python Tkinter GUI"""

import Tkinter as tk
import ttk
import ScrolledText
from Tkinter import Menu
import tkMessageBox as mBox


# Create instance
win = tk.Tk()


# Add title
win.title("Python GUI")


# Create container to hold all widgets
monty = ttk.LabelFrame(win, text="Monty Python")
monty.grid(column=0, row=0, padx=8, pady=4)

# Modify button click function
def clickMe():
	action.configure(text="Hello " + name.get())


# change our label
ttk.Label(monty, text="Enter your name:").grid(column=0, row=0, sticky="W")

# Adding a textbox entry widget
name = tk.StringVar()

nameEntered = ttk.Entry(monty, width=12, textvariable=name)
nameEntered.grid(column=0, row=1, sticky='W')

# Adding a Button
action = ttk.Button(monty, text="Click Me!", command=clickMe)   
action.grid(column=2, row=1)

ttk.Label(monty, text="Choose a number:").grid(column=1, row=0)
number = tk.StringVar()
numberChosen = ttk.Combobox(monty, width=12, textvariable=number)
numberChosen['values'] = (1, 2, 4, 42, 100)
numberChosen.grid(column=1, row=1)
numberChosen.current(0)

# Creating three checkbuttons
chVarDis = tk.IntVar()
check1 = tk.Checkbutton(monty, text="Disabled", variable=chVarDis, state='disabled')
check1.select()
check1.grid(column=0, row=4, sticky=tk.W, columnspan=3)                   

chVarUn = tk.IntVar()
check2 = tk.Checkbutton(monty, text="UnChecked", variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=4, sticky=tk.W, columnspan=3)                   

chVarEn = tk.IntVar()
check3 = tk.Checkbutton(monty, text="Toggle", variable=chVarEn)
check3.deselect()
check3.grid(column=2, row=4, sticky=tk.W, columnspan=3)                   

# GUI Callback function 
def checkCallback(*ignoredArgs):
    # only enable one checkbutton
    if chVarUn.get(): check3.configure(state='disabled')
    else:             check3.configure(state='normal')
    if chVarEn.get(): check2.configure(state='disabled')
    else:             check2.configure(state='normal') 

# trace the state of the two checkbuttons
chVarUn.trace('w', lambda unused0, unused1, unused2 : checkCallback())    
chVarEn.trace('w', lambda unused0, unused1, unused2 : checkCallback())   

# Using a scrolled Text control    
scrolW  = 30; scrolH  =  3
scr = ScrolledText.ScrolledText(monty, width=scrolW, height=scrolH, wrap=tk.WORD)
scr.grid(column=0, sticky='WE', columnspan=3)

# Radiobutton list
colors = ["Blue", "Gold", "Red"]

# Radiobutton callback function
def radCall():
    radSel=radVar.get()
    if   radSel == 0: win.configure(background=colors[0])
    elif radSel == 1: win.configure(background=colors[1])
    elif radSel == 2: win.configure(background=colors[2])

radVar = tk.IntVar()

# Selecting a non-existing index value for radVar
radVar.set(99)    

# Creating all three Radiobutton widgets within one loop
for col in range(3):
    curRad = 'rad' + str(col)  
    curRad = tk.Radiobutton(monty, text=colors[col], variable=radVar, value=col, command=radCall)
    curRad.grid(column=col, row=6, sticky=tk.W, columnspan=3)       
    
# Create a container to hold labels
labelsFrame = ttk.LabelFrame(monty, text=' Labels in a Frame ')
labelsFrame.grid(column=0, row=7)
 
# Place labels into the container element - vertically
ttk.Label(labelsFrame, text="Label1").grid(sticky='W')
ttk.Label(labelsFrame, text="Label2").grid(sticky='W')
ttk.Label(labelsFrame, text="Label3").grid(sticky='W')

# Add some space around each label
for child in labelsFrame.winfo_children(): 
    child.grid_configure(padx=8, pady=1)

# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit() 
    
# Creating a Menu Bar
menuBar = Menu(win)
win.config(menu=menuBar)

# Add menu items
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="New")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=_quit)
menuBar.add_cascade(label="File", menu=fileMenu)

### SCREENSHOT 1 ##############################
# Display a Message Box
def _msgBox():
    # mBox.showinfo('Python Message Info Box', 'A Python GUI created using tkinter:\nThe year is 2015.') 
    mBox.showwarning('Python Message Info Box', 'A Python GUI created using tkinter:\nThe year is 2015.')   
    # mBox.showerror('Python Message Info Box', 'A Python GUI created using tkinter:\nThe year is 2015.')   

# Add another Menu to the Menu Bar and an item
helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label="About", command=_msgBox)
menuBar.add_cascade(label="Help", menu=helpMenu)
win.iconbitmap(r"C:\Users\fanchang\Downloads\fan_test.ico")
# win.iconbitmap(r'C:\python_27_amd64\files\DLLs\py.ico')

spin = tk.Spinbox(monty, from_=0, to=10, width=5, bd=8)
spin.grid(column=0, row=2)
spin = tk.Spinbox(monty, from_=0, to=10, width=5, bd=8, relief=tk.RIDGE)
spin.grid(column=1, row=2)
def _spin():
	value = spin.get()
	print(value)
	# scr.insert(tk.Insert, value + '\n')

# Place cursor into name Entry
nameEntered.focus()      
#======================
# Start GUI
#======================
win.mainloop()
