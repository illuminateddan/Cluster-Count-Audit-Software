#!/usr/bin/python3

# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2022 Dan Cook, Queensland University of Technology
# Created for, and funded by Hort Innovation Project PH17001
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

version = 1.1


import os
import tkinter
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import keyboard
import csv
from datetime import datetime
import math
#install keyboard using: pip install keyboard


#set up our sizes so we can scale and make it all pretty
winWidth = 1400
winHeight = 800
topFrHeight = 50
btmFrHeight = 50
btmFr2Height = 50
sidebarLwidth = 100
sidebarRwidth = 100

#image browser stuff
imgNum = 0      #primary index
imgMax = 0

dirPath = os.getcwd()
dirPath = os.path.join(dirPath,"images")    #temporary to speed up testing**************
os.chdir(dirPath)                           #temporary to speed up testing**************


dirSelected = False
navButtonClick = False  # stupid variable to aid working with Treeview.
manual_audit = False    #manual audit mode toggle: will allow manual entry of count number
hive_type_set = False
hive_number = 0

#data structure

dataAudit =[] #recordNum (from imgNum), filename, marked?, score, audit type
#second index broken into vars for readability, i.e. type = dataAudit[0][DAtype]
DAindex = 0
DAfilename = 1
DAmarked = 2
DAscore = 3
DAtype = 4   #Type of audit: Manual (Man), Frame (NOF_o or NOF_r or NOF_l), Interframe (IFB)
DAhive_num = 5
DAhive_type = 6
DAframes = 7
DAdepth = 8
DAdensity = 9
DAbroodbox = 10

graphicDataStart = 11 #change the number on this one!
DAflen_x1 =graphicDataStart    #frame length coords
DAflen_y1 =graphicDataStart+1
DAflen_x2 =graphicDataStart+2
DAflen_y2 =graphicDataStart+3

DAax = graphicDataStart+4   #these four are used for ovals and rectangle coordinate storage
DAay = graphicDataStart+5
DAbx = graphicDataStart+6
DAby = graphicDataStart+7

data_draw = []
data_draw_index = 0

drawing = False
frame_length_button_bool = False
frame_length_set = False
frame_length_scale_factor = 0
frame_length_total_possible = 0
hive_area = 0

first_run = True

points = 20 #number of points that can be drawn for frame analysis


#************************************************************************************
#Init grid system --------------------------------------------------------------
#************************************************************************************

root = Tk()
stngtmp = "Cluster Counter V" + str(version)
root.title(stngtmp)
root.geometry('{}x{}+{}+{}'.format(winWidth, winHeight,10,10)) #10s = positions on screen
root.minsize(winWidth, winHeight)
root.resizable(0,0)


# create all of the main containers
top_frame = Frame(root, bg='#f0f0f0', width=winWidth, height=topFrHeight, padx=1,pady=3)
center = Frame(root, bg='gray1', width=winWidth, height=40, padx=0, pady=1,borderwidth=0)
btm_frame = Frame(root, bg='#f0f0f0', width=winWidth, height=btmFrHeight, padx=1,pady=3)
btm_frame2 = Frame(root, bg='#f0f0f0', width=winWidth, height=btmFr2Height, padx=1, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")
btm_frame2.grid(row=4, sticky="ew")


#************************************************************************************
# create the widgets for the top frame
#************************************************************************************
button_exit = Button(top_frame,text="Quit", command=root.quit)
button_save = Button(top_frame,text="Save to CSV", command=lambda: save_data_csv())
button_load = Button(top_frame,text="Load CSV", command=lambda: load_data_csv() )
helptips = IntVar()
checkbox_help = Checkbutton(top_frame,text="Help tips", variable=helptips)
autoscroll = IntVar()
checkbox_autoscroll = Checkbutton(top_frame,text="Autoscroll", variable=autoscroll)
autoscroll.set(1) #switch off by default

autoprogress = IntVar()
checkbox_autoprogress = Checkbutton(top_frame,text="Autoprogress", variable=autoprogress)
autoprogress.set(1) #switch off by default

# layout the widgets in the top frame
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(3, weight=200)

button_save.grid(row=0, column = 0, sticky=W, pady=2, padx = 2)
button_load.grid(row=0, column = 1, sticky=W, pady=2, padx = 2)
checkbox_help.grid(row=0, column = 2, sticky=W, pady=2, padx = 2)
checkbox_autoscroll.grid(row=0, column = 3, sticky=E, pady=2, padx = 2)
checkbox_autoprogress.grid(row=0, column = 4, sticky=E, pady=2, padx = 2)
button_exit.grid(row=0, column = 5, sticky=E, pady=2, padx = 2)



#************************************************************************************
#-----------------------------------------
# create the center widgets
#************************************************************************************

ctr_left = Frame(center, bg='#f0f0f0', width=sidebarLwidth)
ctr_mid = Frame(center, bg='grey', padx=0, pady=0) #width doesn't matter really as it fills in all available
ctr_right = Frame(center, bg='#f0f0f0', width=sidebarRwidth, padx=3, pady=3)

# layout the widgets
center.grid_rowconfigure(0, weight=1)   #help with resizing
center.grid_columnconfigure(1, weight=1)

ctr_left.grid(row=0, column=0, sticky="ns")
ctr_mid.grid(row=0, column=1, sticky="nsew")
ctr_right.grid(row=0, column=2, sticky="ns")



#************************************************************************************
#Left Grid widgets--------------------------------------------------------
#************************************************************************************

#option menus--------------------
hiveType = StringVar(ctr_left)
hiveType.set("Langstroth") #default
hiveWidth = StringVar(ctr_left)
hiveWidth.set("9 Frame") #default
hiveDepth = StringVar(ctr_left)
hiveDepth.set("Full Depth") #default

label_hiveParam = Label(ctr_left, text="-- Box Config --")
optHiveType = OptionMenu(ctr_left, hiveType, "Langstroth","Langstroth Mex.",
                         "National(UK)", "Commercial(UK)", "Smith", "Dadant", "Warre" )
#L = 483,#L mex =495, Nat=431.8,commerical = 438.15, smith =393.7, dadant=482.6, Warre=323
optHiveWdith = OptionMenu(ctr_left, hiveWidth, "10 Frame", "9 Frame", "8 Frame", "6 Frame", "5 Frame Nuc","4 Frame Nuc")
optHiveDepth = OptionMenu(ctr_left, hiveDepth, "Full","3/4", "1/2", "WSP", "Ideal")
button_set_hive_type = Button(ctr_left, text="Set Hive Type", command=lambda: set_hive_type(), bg='lightcoral')

label_draw = Label(ctr_left, text="-- Drawing --")
button_set_frame_length = Button(ctr_left, text="Set Frame Length", bg='lightcoral',
                                 command=lambda: set_frame_length())
label_spacer = Label(ctr_left,text="Density %", bg="#f0f0f0")
entry_density = Entry(ctr_left, width=10)
entry_density.insert(0, "100") #sets start value
button_drawClusterOval = Button(ctr_left,text="Cluster Oval (NOF)", command=lambda:cluster_oval())
button_drawClusterRectangle = Button(ctr_left,text="Cluster Rectangle (NOF)", command=lambda:cluster_rect())
button_drawClusterFrames = Button(ctr_left,text="Cluster Frames (NOF)", command=lambda:cluster_frame())
button_drawInterFrames = Button(ctr_left,text="Inter-Frames (IFB)", command=lambda:inter_frame())

label_spacer2 = Label(ctr_left,text="", bg="#f0f0f0")
label_draw2 = Label(ctr_left, text="-- Manual --")
button_manual = Button(ctr_left,text="Manual audit", bg='#f0f0f0', command=lambda:manual_mode() )
label_manual = Label(ctr_left, text="", fg='grey')

#lay them out...
ctr_left.grid_columnconfigure(0, weight=1)

label_hiveParam.grid(row=1, column = 0, sticky=W+E, pady=5, padx = 2)
optHiveType.grid(row=2, column = 0, sticky=W+E, pady=0, padx = 2)
optHiveWdith.grid(row=3, column = 0, sticky=W+E, pady=0, padx = 2)
optHiveDepth.grid(row=4, column = 0, sticky=W+E, pady=0, padx = 2)
button_set_hive_type.grid(row=5, column = 0, sticky=W+E, pady=0, padx = 2)

#
label_draw.grid(row=7, column = 0, sticky=W+E, pady=2, padx = 2)
button_set_frame_length.grid(row=8, column = 0, sticky=W+E, pady=2, padx = 2)
label_spacer.grid(row=9, column = 0, sticky=W, pady=2, padx = 2)
entry_density.grid(row=9, column = 0, sticky=E, pady=2, padx = 4)
button_drawClusterOval.grid(row=10, column = 0, sticky=W+E, pady=2, padx = 2)
button_drawClusterRectangle.grid(row=11, column = 0, sticky=W+E, pady=2, padx = 2)
button_drawClusterFrames.grid(row=12, column = 0, sticky=W+E, pady=2, padx = 2)
button_drawInterFrames.grid(row=13, column = 0, sticky=W+E, pady=2, padx = 2)

label_spacer2.grid(row=14, column = 0, sticky=W+E, pady=2, padx = 2)
label_draw2.grid(row=15, column = 0, sticky=W+E, pady=2, padx = 2)
button_manual.grid(row=16, column = 0, sticky=W+E, pady=2, padx = 2)
label_manual.grid(row=17, column = 0,sticky=W+E, pady=2, padx = 20)


#************************************************************************************
#Setup the centre window  --------------------------------------------------------------
#************************************************************************************

ctr_mid.grid_rowconfigure(0, weight=1)   #help with resizing
ctr_mid.grid_columnconfigure(0, weight=1)

#imgLabel = Label(ctr_mid, text="Select a directory to begin. One data file is created for each image directory.", borderwidth=2, bg='black',fg='white')
#imgLabel.grid(row=0, column=0, sticky="nsew")

img_canvas = Canvas(ctr_mid,borderwidth=2, bg='black' )
img_canvas.grid(row=0, column=0, sticky="nsew")


#************************************************************************************
#Setup the right hand File Bar  --------------------------------------------------------------
#************************************************************************************

#--- File widgets and layout-------------------------------------------
ctr_right.grid_columnconfigure(0, weight=1)

button_selectFolder = Button(ctr_right,text="Set Image Folder",bg='lightcoral', command=lambda:get_dir())

tree = ttk.Treeview(ctr_right, column=("number","file", "marked", "type", "score","hivenum","density","broodbox"),
                    selectmode="browse", show="headings", height=15)
tree.column("#1", anchor=W, width=15)
tree.column("#2", anchor=W, width=50)
tree.column("#3", anchor=W, width=20)
tree.column("#4", anchor=W, width=35)
tree.column("#5", anchor=W, width=40)
tree.column("#6", anchor=W, width=35)
tree.column("#7", anchor=W, width=35)
tree.column("#8", anchor=W, width=45)


tree.heading("#1", text="#", anchor=W)
tree.heading("#2", text="File", anchor=W)
tree.heading("#3", text="?", anchor=W)
tree.heading("#4", text="Type", anchor=W)
tree.heading("#5", text="Score", anchor=W)
tree.heading("#6", text="Hv#", anchor=W)
tree.heading("#7", text="Dens.", anchor=W)
tree.heading("#8", text="BroodBx", anchor=W)

tree.tag_configure("evenrow",background='whitesmoke',foreground='black')
tree.tag_configure("oddrow",background='white',foreground='black')

label_info1 = Label(ctr_right,text="Hive#:", bg="#f0f0f0", justify=LEFT)
label_info2 = Label(ctr_right,text="Audit type", bg="#f0f0f0", justify=LEFT)
label_info3 = Label(ctr_right,text="Frames score:", bg="#f0f0f0", justify=LEFT)
label_info4 = Label(ctr_right,text="Density %:", bg="#f0f0f0", justify=LEFT)
label_info5 = Label(ctr_right, text="Hive Configuration: ", bg="#f0f0f0", justify=LEFT)

button_selectFolder.grid(row=0, column = 0, sticky=W+E, pady=2, padx = 2)
tree.grid(row=1,column=0,sticky=W+E,pady=2,padx=2)
label_info1.grid(row=2,column=0,sticky=W,pady=2,padx=2)
label_info2.grid(row=3,column=0,sticky=W,pady=2,padx=2)
label_info3.grid(row=4,column=0,sticky=W,pady=2,padx=2)
label_info4.grid(row=5,column=0,sticky=W,pady=2,padx=2)
label_info5.grid(row=6,column=0,sticky=W,pady=2,padx=2)



#************************************************************************************
#bottom frame image nav bar -------------------------------------------------------
#************************************************************************************
btm_frame.grid_rowconfigure(0, weight=1)

btm_frame.grid_columnconfigure(0, weight=1)   #help with resizing
btm_frame.grid_columnconfigure(1, weight=1)

btm_frame_left = Frame(btm_frame,  padx=0, pady=0)
btm_frame_right = Frame(btm_frame,  padx=0, pady=0)

btm_frame_left.grid(row=0, column=0, sticky="w")
btm_frame_right.grid(row=0, column=1, sticky="e")


label_imageCtrl = Label(btm_frame_left, text="Image Navigation:")
button_first = Button(btm_frame_left,text="|<< First", bg='lightblue', command=lambda: first_img())
button_back = Button(btm_frame_left,text="<Prev", bg='lightblue', command=lambda: prev_img())
label_imgnum = Label(btm_frame_left, text="Set Directory!")
button_forward = Button(btm_frame_left,text="Next>", bg='lightblue', command=lambda: next_img())
button_last = Button(btm_frame_left,text="Last >>|", bg='lightblue', command=lambda: last_img())

label_imageCtrl.grid(row=0, column = 0, sticky=W+E, pady=0, padx = 5)
button_first.grid(row=0, column = 1, sticky=W+E, padx = 5)
button_back.grid(row=0, column = 2, sticky=W+E, padx = 5)
label_imgnum.grid(row=0, column = 3, sticky=W+E, padx = 15)
button_forward.grid(row=0, column = 4, sticky=W+E, padx = 5)
button_last.grid(row=0, column = 5, sticky=W+E, padx = 5)


label_hiveNum = Label(btm_frame_right, text="Hive Number")
button_hive_num_down = Button(btm_frame_right,text="-1",bg='lightblue', command=lambda: hive_num_decrement())
entry_hive_num = Entry(btm_frame_right, width=10)
entry_hive_num.insert(0, "0") #sets start value
button_hive_num_up = Button(btm_frame_right,text="+1",bg='lightblue', command=lambda: hive_num_increment())
button_hive_num_set = Button(btm_frame_right,text="Set",bg='lightblue', command=lambda: hive_num_set())
button_hive_num_repeat = Button(btm_frame_right,text="Repeat",bg='lightblue', command=lambda: hive_num_repeat())

label_hiveNum.grid(row=0, column = 0, sticky=W+E, pady=0, padx = 5)
button_hive_num_down.grid(row=0, column = 1, sticky=W+E, padx = 5)
entry_hive_num.grid(row=0, column = 2, sticky=W+E, padx = 5)
button_hive_num_up.grid(row=0, column = 3, sticky=W+E, padx = 5)
button_hive_num_set.grid(row=0, column = 4, sticky=W+E, padx = 5)
button_hive_num_repeat.grid(row=0, column = 5, sticky=W+E, padx = 5)


#************************************************************************************
#bottom frame (2) status bar -------------------------------------------------------
#************************************************************************************

status = Label(btm_frame2,text="Press \"Set Hive Type\"",bd=1, relief=SUNKEN, anchor=W)

statusImg = Label(btm_frame2,text="Image Details TBC",bd=1, relief=SUNKEN, anchor=E)

btm_frame2.grid_columnconfigure(0, weight=1)
btm_frame2.grid_columnconfigure(1, weight=1)
status.grid(row=0, column=0, columnspan= 4, sticky=W) #stretch West and East
statusImg.grid(row=0, column=0, columnspan= 4, sticky=E) #stretch West and East



# Functions---------------------------------------------------------------------------------------


#---------------Load and save-----------------------------------
def save_data_csv():
    header = ['imgNum','fileName','marked','score','auditType','hiveNum','hiveType','numFrames','hiveDepth','density',
              'broodbox','frame1x','frame1y','frame2x','frame2y','marker data->']
    directory = [dirPath]

    #file_exists = os.path.exists('AuditData.csv')
    now = datetime.now()
    dt_string= now.strftime("%Y%m%d_%H%M%S")
    filestr = 'AuditData_'+dt_string+'.csv'

    os.chdir(dirPath) #change dir to working directory
    with open(filestr, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(directory)
        writer.writerow(header)
        writer.writerows(dataAudit)

    msgstr = "File saved as {} in directory {}".format(filestr,directory)
    tkinter.messagebox.showinfo(title='File saved', message=msgstr)
    return

def load_data_csv():
    global dataAudit
    global imgMax
    global imgNum
    global dirPath
    global dirSelected

    if len(dataAudit)>0:
        answer = messagebox.askokcancel(title="Save your Work?",
                                       message="Press OK to delete exisiting work and load new,"
                                               "\nor press Cancel to stop and save your work.",
                                        )

        if not answer:
            save_data_csv()
            return


    getfile = filedialog.askopenfile(initialdir=os.getcwd(), title="Select audit data directory",
                                       filetypes=[('Comma Seperated', ['.csv'])] )
    if not getfile:
        return None

    dataAudit.clear()    #clear existing array

    with open(getfile.name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        dataAudit = list(csv_reader)

    getfile.close()

    dirPath = dataAudit[0][0]   #first line of a csv is the file path
    print("Dir path: ",dirPath)
    dirSelected = True

    dataAudit.pop(0)    #remove directory data
    dataAudit.pop(0)    #remove headings

    print("read ",len(dataAudit),"records")
    #print("first record: ",dataAudit[0])

    #convert to correct datatypes
    for i in range(len(dataAudit)):
        dataAudit[i][DAindex] = int(dataAudit[i][DAindex]) #index
        if dataAudit[i][DAmarked] == "True":
            dataAudit[i][DAmarked] = True
        else:
            dataAudit[i][DAmarked] = False

        dataAudit[i][DAscore] = float(dataAudit[i][DAscore])
        dataAudit[i][DAhive_num] = int(dataAudit[i][DAhive_num])
        dataAudit[i][DAdensity] = int(dataAudit[i][DAdensity])
        dataAudit[i][DAbroodbox] = int(dataAudit[i][DAbroodbox])

        for j in range(9,56+9):
            dataAudit[i][j] = int(dataAudit[i][j])


    imgNum = 0
    imgMax = len(dataAudit)
    #update_record_treeview() #in the treeview # Now just does single line. Swap for...
    build_file_tree() #rebuild whole list
    tree.selection_set(0)  # selects first image
    update_data_driven_labels()

    button_selectFolder = Button(ctr_right, text="Set Image Folder" ,command=lambda: get_dir())
    button_selectFolder.grid(row=0, column=0, sticky=W + E, pady=2, padx=2)

#----------Open directory, build array------------------------
def get_dir():
    #Used to set the directory when the set dir button is pressed
    #Also initialises the arrays
    global dirPath
    global dirSelected
    global imgMax

    dirPath = filedialog.askdirectory(initialdir=os.getcwd(),title="Select image directory")
    dirSelected = True
    os.chdir(dirPath)  # change working directory to selected dirpath
    dataAudit.clear()

    fileList = os.listdir(dirPath)
    i=0
    for f in fileList:
                    # recordNum, filename, marked?, score, audit type, hive#, hiveType, NumFrames, Depth, Density, broodbox
        dataAudit.append([i,        f,      False,    0,    "?",        -1,   "Langstroth", -1,     "full",  -1,      0,
                          -1,-1,-1,-1, #4xframe DAflen_x1, etc
                          -1,-1,-1,-1,    # 4xoval or rect DAax,DAay, etc
                          -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,  #plus 40 more for lines
                          -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
                          -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] )
        i+=1

    imgMax = len(dataAudit)
    build_file_tree()
    update_data_driven_labels()

    button_selectFolder = Button(ctr_right, text="Set Image Folder", command=lambda: get_dir())
    button_selectFolder.grid(row=0, column=0, sticky=W + E, pady=2, padx=2)


    return

#----------Complete filelist rebuild------------------
def build_file_tree():  # Rebuild files in the treeview

    global tree

    i = 0
    for r in tree.get_children():    #delete all records
        tree.delete(r)

    for d in dataAudit:             #rebuild treeview
        if dataAudit[i][DAmarked]:  #show a nice Y or N for marked rather than bool
            marked = 'Y'
        else:
            marked ='N'

        if i % 2 ==0:           #even row
            tree.insert('', 'end', iid=i, values=(i + 1,dataAudit[i][DAfilename], marked,
                                        dataAudit[i][DAtype], round(dataAudit[i][DAscore],2),
                                        dataAudit[i][DAhive_num], dataAudit[i][DAdensity],
                                        dataAudit[i][DAbroodbox]),
                                        tags="evenrow")
        if i % 2 !=0:           #even row
            tree.insert('', 'end', iid=i, values=(i + 1, dataAudit[i][DAfilename], marked,
                                          dataAudit[i][DAtype], round(dataAudit[i][DAscore],2),
                                          dataAudit[i][DAhive_num], dataAudit[i][DAdensity],
                                          dataAudit[i][DAbroodbox]),
                                        tags="oddrow")
        i += 1

    tree.grid(row=1, column=0, sticky=W + E, pady=2, padx=2)
    scrollbar = ttk.Scrollbar(ctr_right, orient='vertical', command=tree.yview)
    scrollbar.grid(row=1, column=1, sticky=N + S)

    tree.focus(imgNum)  #set selection bar
    tree.selection_set(imgNum)


    return

#----------Single record update---------------------------------
def update_record_treeview():  # Rebuild files in the listbox

    #New method: if a record is updated, delete the item at X location and then reinsert that item.
    # use tree.delete(selected_item) then:
    # use tree.insert('', 0, values=contact)
    # rename this to "build_file_list"
    global tree

    i = imgNum
    tree.delete(i) #delete the record

    if dataAudit[i][DAmarked]:  #show a nice Y or N for marked rather than bool
        marked = 'Y'
    else:
        marked ='N'

    if i % 2 ==0:           #even row
        tree.insert('', i, iid=i, values=(i + 1,dataAudit[i][DAfilename], marked,
                                    dataAudit[i][DAtype], round(dataAudit[i][DAscore],2),
                                    dataAudit[i][DAhive_num], dataAudit[i][DAdensity],
                                    dataAudit[i][DAbroodbox]),
                                    tags="evenrow")
    if i % 2 !=0:           #even row
        tree.insert('', i, iid=i, values=(i + 1, dataAudit[i][DAfilename], marked,
                                      dataAudit[i][DAtype], round(dataAudit[i][DAscore],2),
                                      dataAudit[i][DAhive_num], dataAudit[i][DAdensity],
                                      dataAudit[i][DAbroodbox]),
                                    tags="oddrow")


# File selected is called everytime a file is selected in the treeview by mouse, keyboard or buttons
def file_selected(event): #event for list box selection- ties in with image show and nav
    global imgNum
    global navButtonClick
    global frame_length_set
    global frame_length_button_bool

    sel = tree.selection()  # get tuple of whats selected

    if sel: #test if its something and not nothing.
        sel = int(sel[0])
        if imgNum != sel:
            imgNum = sel
        #print("file_selected() try ok.. imgNum=", imgNum)
        img_show()
        update_data_driven_labels()

    if autoscroll.get() == 1:
        # tree.yview_moveto(imgNum / len(dataAudit))
        bits = 1 / len(dataAudit)
        if imgNum < 7:
            tree.yview_moveto(0)
        if imgNum >= 7 and imgNum <= len(dataAudit)-7: #more than half the list window
            tree.yview_moveto(imgNum / len(dataAudit) - bits*7)
        if imgNum > len(dataAudit)-7:
            tree.yview_moveto(1)


    frame_length_set = False
    frame_length_button_bool = False
    button_set_frame_length = Button(ctr_left, text="Set Frame Length", bg='lightcoral',
                                     command=lambda: set_frame_length())
    button_set_frame_length.grid(row=8, column=0, sticky=W + E, pady=2, padx=2)
    return




#--------------------------------------------------------------------

def update_data_driven_labels():
    global label_info1
    global label_info2
    global label_info3
    global label_info4
    global label_info5
    #nav bar image counter - update it
    label_imgnum = Label(btm_frame_left, text="Image " + str(imgNum+1) + " of " + str(imgMax))
    label_imgnum.grid(row=0, column=3, sticky=W + E, padx=15)

    if dataAudit[imgNum][DAflen_x1]<0:
        frame_length_set=False
    else:
        frame_length_set = True
    frame_length_button_bool = False

    if dataAudit[imgNum][DAdensity] > -1:       #update density values
        entry_density.delete('0', 'end')
        entry_density.insert(0, dataAudit[imgNum][DAdensity])  # sets the value for density
    else:
        entry_density.delete('0', 'end')
        entry_density.insert(0, 100)  # sets the value for density

    if dataAudit[imgNum][DAhive_num] > -1:       #update density values
        entry_hive_num.delete('0', 'end')
        entry_hive_num.insert(0, dataAudit[imgNum][DAhive_num])  # sets the value for density
    else:
        entry_hive_num.delete('0', 'end')
        entry_hive_num.insert(0, -1)  # sets the value for density

    label_info1.destroy()
    label_info2.destroy()
    label_info3.destroy()
    label_info4.destroy()
    label_info5.destroy()

    label_info1 = Label(ctr_right, text="Hive#: "+str(dataAudit[imgNum][DAhive_num]), bg="#f0f0f0", justify=LEFT)
    label_info2 = Label(ctr_right, text="Audit type: "+str(dataAudit[imgNum][DAtype]), bg="#f0f0f0", justify=LEFT)
    label_info3 = Label(ctr_right, text="Frames score: "+str(round(dataAudit[imgNum][DAscore],2)), bg="#f0f0f0", justify=LEFT)
    label_info4 = Label(ctr_right, text="Density %: "+str(dataAudit[imgNum][DAdensity]), bg="#f0f0f0", justify=LEFT)
    label_info5 = Label(ctr_right, text="Hive Configuration: "
                                        +str(dataAudit[imgNum][DAhive_type])+" "
                                        +str(dataAudit[imgNum][DAframes])+" "
                                        +str(dataAudit[imgNum][DAdepth]), bg="#f0f0f0", justify=LEFT)

    label_info1.grid(row=2, column=0, sticky=W, pady=2, padx=2)
    label_info2.grid(row=3, column=0, sticky=W, pady=2, padx=2)
    label_info3.grid(row=4, column=0, sticky=W, pady=2, padx=2)
    label_info4.grid(row=5, column=0, sticky=W, pady=2, padx=2)
    label_info5.grid(row=6, column=0, sticky=W, pady=2, padx=2)

    return

# Centre Window image functions ------------------------------------------------------

def img_show():
    global imgNum
    global imgList
    global imgResized
    global tree

    #print("img_show() imgNum =",imgNum)

    if dirSelected == True:
        imgPath = os.path.normpath(os.path.join(dirPath, dataAudit[imgNum][DAfilename]))

        if imgPath.endswith(('.jpg', '.jpeg', '.gif', '.png','.bmp')):
            img = Image.open(imgPath)
            imgOrigSize = img.size
            root.update()  # force update to get centre frame dimensions
            imgMaxWidth = ctr_mid.winfo_width()
            imgMaxHeight = ctr_mid.winfo_height()

            # rescale - find the ratio and rescale
            [imageSizeWidth, imageSizeHeight] = img.size
            if imageSizeWidth > imageSizeHeight:
                imgRatio = imageSizeHeight / imageSizeWidth
                img = img.resize((imgMaxWidth, int(imgMaxWidth * imgRatio)), Image.ANTIALIAS)
            else:
                imgRatio = imageSizeWidth / imageSizeHeight
                img = img.resize((int(imgMaxHeight * imgRatio), imgMaxHeight), Image.ANTIALIAS)

            imgScaledSize = img.size
            imgResized = ImageTk.PhotoImage(img)

            img_canvas.delete("all")

            [new_imageSizeWidth, new_imageSizeHeight] = img.size

            #centred image----------
            img_canvas.create_image(imgMaxWidth/2-new_imageSizeWidth/2,
                                    imgMaxHeight/2-new_imageSizeHeight/2,
                                    anchor='nw',image=imgResized)   #image start coords, where to measure from (anchor)
            img_canvas.grid(row=0, column=0, sticky="nsew")

            status_message(str("Image:"+ dataAudit[imgNum][DAfilename] +" of size(pixels) " + str(imgOrigSize)))

            if dataAudit[imgNum][DAmarked]:
                draw_prev_count_data()

        else:
            img_canvas.delete("all")
            status_message(str("This is not a valid image file!"))
    return


def draw_prev_count_data():
    x1=dataAudit[imgNum][DAflen_x1]
    y1=dataAudit[imgNum][DAflen_y1]
    x2=dataAudit[imgNum][DAflen_x2]
    y2=dataAudit[imgNum][DAflen_y2]
    img_canvas.create_line(x1,y1,x2,y2,width=2, fill='red')

    if dataAudit[imgNum][DAtype] == "NOF_o" or dataAudit[imgNum][DAtype] == "NOF_r":
        ax = dataAudit[imgNum][DAax]
        ay = dataAudit[imgNum][DAay]
        bx = dataAudit[imgNum][DAbx]
        by = dataAudit[imgNum][DAby]

        if dataAudit[imgNum][DAtype] == "NOF_o":
            img_canvas.create_oval(ax, ay, bx, by, outline='yellow', width=2)
        else:
            img_canvas.create_rectangle(ax, ay, bx, by, outline='yellow', width=2)

    else:
        for i in range(DAax,DAax+points*2,4):
            if dataAudit[imgNum][i]>-1:
                img_canvas.create_line(dataAudit[imgNum][i], dataAudit[imgNum][i+1],
                                       dataAudit[imgNum][i+2], dataAudit[imgNum][i+3],
                                       width=2, fill='yellow')
    return

##Left Side Bar button functions-----------------------------------------------

def set_hive_type():
    global status
    global hive_type_set
    hive_type_set = True
    status.grid_forget()
    status = Label(btm_frame2,
                   text="Hive Config: {} {} {}".format(hiveWidth.get(), hiveDepth.get(), hiveType.get()),
                   bd=1, relief=SUNKEN, anchor=W)

    status.grid(row=0, column=0, columnspan=4, sticky=W)  # stretch West and East
    button_set_hive_type = Button(ctr_left, text="Set Hive Type", command=lambda: set_hive_type())
    button_set_hive_type.grid(row=5, column=0, sticky=W + E, pady=0, padx=2)

    return

# Helper functions*********************************************************************

def warn_set_hive_type():
    tkinter.messagebox.showwarning(title="Oops!", message="You need to set the hive type first!")
    return

def warn_dir_selected():
    tkinter.messagebox.showwarning(title="Oops!", message="You need to set image directory first!")
    return

def warn_frame_select():
    tkinter.messagebox.showwarning(title="Oops!", message="You need to define the frame length first!")
    return

def status_message(message):
    global statusImg
    messageStr=str(message)

    statusImg.destroy()
    statusImg = Label(btm_frame2, text=message, bd=1,
                      relief=SUNKEN, anchor=E)
    statusImg.grid(row=0, column=0, columnspan=4, sticky=E)  # stretch West and East
    return


def get_frame_score(coverage):
    score = 0
    tmp = 0

    #if hiveType.get() == "Langstroth":
    if hiveWidth.get() == "10 Frame":
        tmp = 10
    elif hiveWidth.get() == "9 Frame":
        tmp = 9
    elif hiveWidth.get() == "8 Frame":
        tmp = 8
    elif hiveWidth.get() == "6 Frame":
        tmp = 6
    elif hiveWidth.get() == "5 Frame":
        tmp = 5
    else:  # 4 frame
        tmp = 4

    global density

    try:
        density = int(entry_density.get())
    except:
        density = 100
        tkinter.messagebox.showinfo(title="How to...",
                                    message="Density must be an integer between 0 and 100")

    score = tmp * coverage * (density/100)
    print("result is ",score, "frames")
    return score

# Drawing functions********************************************

def check_drawing(drawtype):
    global drawing
    drawing = True

    if drawtype == 0:
        print("draw type nada!")

    if drawtype == 1:
        print("frame length mode")
        img_canvas.bind("<Button-1>", draw_frame_length)

    if drawtype == 2:
        print("Cluster Oval Mode")
        img_canvas.bind("<Button-1>", draw_oval_cluster )

    if drawtype == 3:
        print("Cluster Rectangle Mode")
        img_canvas.bind("<Button-1>", draw_rect_cluster )

    if drawtype == 4:
        print("Cluster Frames Mode")
        img_canvas.bind("<Button-1>", draw_frame_cluster )
        img_canvas.bind("<Button-3>", draw_frame_cluster)

    if drawtype == 5:
        print("Inter-Frames Mode")
        img_canvas.bind("<Button-1>", draw_interframe_cluster)
        img_canvas.bind("<Button-3>", draw_interframe_cluster)

    return

def set_frame_length(): #button press function
    global drawing
    global frame_length_button_bool
    global frame_length_set
    global frame_length

    if not hive_type_set:
        warn_set_hive_type()
        return
    if not dirSelected:
        warn_dir_selected()


    status_message("Select the two end points on a single central frame to calibrate.")


    if frame_length_button_bool and not frame_length_set:    #set frame length mode
        frame_length_set = True

        button_set_frame_length = Button(ctr_left, text="Set Frame Length", bg='lightgreen',
                                         command=lambda: set_frame_length())

    else:   # !frame_length_button_bool and !frame_length_set:
        frame_length_button_bool = True
        frame_length_set = False
        button_set_frame_length = Button(ctr_left, text="Set Frame Length", bg='lightblue',
                                         command=lambda: set_frame_length())

        img_show()  # clears and resets canvas
        check_drawing(1)

    button_set_frame_length.grid(row=8, column=0, sticky=W + E, pady=2, padx=2)

    return

def draw_frame_length(event):
    global data_draw_index
    global data_draw
    global drawing

    x,y=event.x,event.y
    if drawing:
        if data_draw_index<2:
            data_draw.append([x,y])
            img_canvas.create_oval(x-5,y-5,x+5,y+5, fill='red', outline='yellow',width=1)
            if data_draw_index==1:
                img_canvas.create_line(data_draw[0][0], data_draw[0][1], data_draw[1][0], data_draw[1][1],
                                       width=2,fill='red')

                width = data_draw[0][0] - data_draw[1][0]
                height = data_draw[0][1] - data_draw[1][1]
                hypo_length = abs(math.hypot(width, height))
                #print("frame length in pixels:", hypo_length)  #in pixels
                scale=frame_scaling_factor_maker(hypo_length)

                #store frame length data
                dataAudit[imgNum][DAflen_x1] = data_draw[0][0]
                dataAudit[imgNum][DAflen_y1] = data_draw[0][1]
                dataAudit[imgNum][DAflen_x2] = data_draw[1][0]
                dataAudit[imgNum][DAflen_y2] = data_draw[1][1]

                #clear out data array
                data_draw_index = 0
                data_draw=[]
                drawing = False     #stop the drawing thingy from adding more points
                set_frame_length()  #to update button colour
                status_message(str("Frame calibrated at "+ str(round(hypo_length,1))+
                                    " pixels and scale factor of "+ str(round(scale,2)) ))
            else:
                data_draw_index += 1
    return


# Used to get the multiplication factor of mm/pixel for calculating areas and lengths
def frame_scaling_factor_maker(length):
    global frame_length_scale_factor
    global hive_area
    global frame_length_total_possible
    #ALL DIMS ARE INTERNAL and.. LENGTH IS TOP BAR LENGTH!!
    # L = 463.6,#L mex =477, Nat=431.8,commerical = 438.15, smith =393.7, dadant=482.6, Warre=323

    langX, langY = 362,480 #http://www.dave-cushman.net/bee/lang.html
    langMX, langMY = 367,495 #http://www.dave-cushman.net/bee/lang.html
    natX,natY = 442, 432    #http://www.dave-cushman.net/bee/natbrood.html ,
    # http://www.dave-cushman.net/bee/bsframedimensions.html
    commX, commY = 447,438  #https://dorchesterandweymouthbka.com/hive-sizes/  (assume 18mm thickness)
    #http: // www.dave - cushman.net / bee / comframedims.html
    smithX,smithY = 445,394 #https://dorchesterandweymouthbka.com/hive-sizes/ (assume 18mm thickness)
    #http: // www.dave - cushman.net / bee / bs_smframes.html
    dadX,dadY = 368,441   #(20 ") - (2 * (7/8) ") =463.55 mm (and -22.225 for frames) x 368.3mm
    #http://www.scottishbeekeepers.org.uk/images/education/techdatasheets/TDS%20number%205%20langstroth%20and%20md%20hive.pdf
    warX,warY = 331,324  #353-22 x 353-22 https://warre.biobees.com/plans.htm
    #https: // hornsby - beekeeping.com / warre - frames - assembled /

#NEED TO CHECK HOW MANY FRAMES EACH HIVE TAKES (i.e. non-langstroth)

    if hiveType.get() == "Langstroth": #483mm x 362
            frame_length_scale_factor =  langY / length   #mm per pixel
            if hiveWidth.get() == "10 Frame":
                hive_area = langY * langX           #9 / 10 frame
                frame_length_total_possible = langY * 10
            elif hiveWidth.get() == "9 Frame":
                hive_area = langY * langX
                frame_length_total_possible = langY * 9
            elif hiveWidth.get() == "8 Frame":
                hive_area = langY * 310
                frame_length_total_possible = langY * 8
            elif hiveWidth.get() == "6 Frame":
                hive_area = langY * 218         #Guestimate based on 35mm hoffman +1.2mm spacing per frame
                frame_length_total_possible = langY * 6
            elif hiveWidth.get() == "5 Frame":
                hive_area = langY * 181
                frame_length_total_possible = langY * 5
            else:
                hive_area = langY * 150
                frame_length_total_possible = langY * 4

            #print("pixels ", length, " mm length:", langY)
            print("Langstroth ",hiveWidth.get(), " scale factor: ",frame_length_scale_factor)

    elif hiveType.get() == "Langstroth Mex.": #477mm x 367
            frame_length_scale_factor = langMY / length
            hive_area = 367*477
            frame_length_total_possible = langY * 10
            print("Langstroth Mexico scale factor: ",frame_length_scale_factor)

    elif hiveType.get() == "National(UK)": #442 x 442mm (460mm - 18mm thickness)
            frame_length_scale_factor = natY / length
            hive_area =natX*natY
            frame_length_total_possible = natY * 10
            print("National(UK) scale factor: ",frame_length_scale_factor)

    elif hiveType.get() == "Commercial(UK)": #447 x 447 (465mm by 465 mm - 18mm thickness)
            frame_length_scale_factor = commY / length
            hive_area = commX * commY
            frame_length_total_possible = commY * 10
            print("Commercial(UK) scale factor: ",frame_length_scale_factor)

    elif hiveType.get() == "Smith": #393.7mm
            frame_length_scale_factor = smithY / length
            hive_area = smithX * smithY
            frame_length_total_possible = smithX * 10
            print("Smith scale factor: ",frame_length_scale_factor)

    elif hiveType.get() == "Dadant": #482.6mm
            frame_length_scale_factor = dadY / length
            hive_area = dadX * dadY
            frame_length_total_possible = dadY * 10
            print("Dadant scale factor: ",frame_length_scale_factor)

    elif hiveType.get() == "Warre": #323mm
            frame_length_scale_factor = warY / length
            hive_area = warX * warY
            frame_length_total_possible = warX * 10
            print("Warre scale factor: ",frame_length_scale_factor)

    return frame_length_scale_factor

#-------------------------------
def cluster_oval():         #Called on cluster oval button press
    global drawing

    if not hive_type_set:
        warn_set_hive_type()
        return
    if not dirSelected:
        warn_dir_selected()
        return
    if not frame_length_set:
        warn_frame_select()
        return


    if helptips.get() == 1:
        tkinter.messagebox.showinfo(title="How to...",
                                    message="Select the centre of the cluster, then the top and side of the oval")

    img_show()  # clears and resets canvas
    check_drawing(2)
    return

def draw_oval_cluster(event):
    global data_draw
    global data_draw_index
    global drawing

    points = 3
    x, y = event.x, event.y
    if drawing:
        if data_draw_index<points:
            data_draw.append([x,y])
            img_canvas.create_oval(x-5,y-5,x+5,y+5, fill='green', outline='yellow',width=1)
            img_canvas.create_text(x+15,y,text=data_draw_index,fill= 'yellow')
            #print(data_draw[data_draw_index])

            if data_draw_index==points-1:

                sf = frame_length_scale_factor  # for ease of reading forumla

                ctr_x, ctr_y = data_draw[0][0],data_draw[0][1]
                x1 = abs(ctr_x - data_draw[1][0])
                y1 = abs(ctr_y - data_draw[1][1])
                x2 = abs(ctr_x - data_draw[2][0])
                y2 = abs(ctr_y - data_draw[2][1])
                #print(x1, y1, x2, y2)

                if x1>x2 and y2>y1:   #covers all where X is plotted first
                    ax=ctr_x - x1
                    ay=ctr_y - y2
                    bx=ctr_x + x1
                    by=ctr_y + y2

                    oval_area_mm = (x1 * sf) * (y2 * sf) * math.pi
                    rect_area = (x1 * 2 * sf) * (y2 * 2 * sf)
                else:                   #covers all where y is plotted first
                    ax = ctr_x - x2
                    ay = ctr_y - y1
                    bx = ctr_x + x2
                    by = ctr_y + y1

                    oval_area_mm = (x2 * sf) * (y1 * sf) * math.pi
                    rect_area = (x2 * 2 * sf) * (y1 * 2 * sf)


                img_canvas.create_rectangle(ax, ay, bx, by, outline='green', width=1)
                img_canvas.create_oval(ax, ay, bx, by,outline='yellow', width=2)

                #print("Oval area: ", oval_area_mm, "mm2 from ", hive_area, "mm2 total area")

                coverage = oval_area_mm / hive_area
                score = get_frame_score(coverage)

                #write the data to the record
                dataAudit[imgNum][DAscore] = score
                dataAudit[imgNum][DAmarked] = True
                dataAudit[imgNum][DAtype] = "NOF_o"
                dataAudit[imgNum][DAhive_num] = hive_number
                dataAudit[imgNum][DAhive_type] = hiveType.get()
                dataAudit[imgNum][DAframes] = hiveWidth.get()
                dataAudit[imgNum][DAdepth] = hiveDepth.get()
                dataAudit[imgNum][DAdensity] = density

                # 4x frame length coordinates
                dataAudit[imgNum][DAax] = ax
                dataAudit[imgNum][DAay] = ay
                dataAudit[imgNum][DAbx] = bx
                dataAudit[imgNum][DAby] = by

                data_draw_index = 0
                data_draw=[]
                drawing = False     #stop the drawing thingy from adding more points

                update_record_treeview() #update the file window with the data
                msg="Oval area: " + str(oval_area_mm), "mm2 from " + str(hive_area) + "mm2 total area"
                status_message(msg)
            else:
                data_draw_index += 1

    return
#-------------------------------
def cluster_rect():         #Called on cluster rect button press
    global drawing

    if not hive_type_set:
        warn_set_hive_type()
        return
    if not dirSelected:
        warn_dir_selected()
        return
    if not frame_length_set:
        warn_frame_select()
        return

    if helptips.get() == 1:
        tkinter.messagebox.showinfo(title="How to...",
                                    message="Select the two opposite corners of the rectangle")

    img_show()  # clears and resets canvas after frame length graphic
    check_drawing(3)

    return

def draw_rect_cluster(event):
    global data_draw
    global data_draw_index
    global drawing

    points = 2
    x, y = event.x, event.y
    if drawing:
        if data_draw_index<points:
            data_draw.append([x,y])
            img_canvas.create_oval(x-5,y-5,x+5,y+5, fill='green', outline='yellow',width=1)
            img_canvas.create_text(x+15,y,text=data_draw_index,fill= 'orange')
            #print(data_draw[data_draw_index])

            if data_draw_index==points-1:

                ax = data_draw[0][0]
                ay = data_draw[0][1]
                bx = data_draw[1][0]
                by = data_draw[1][1]
                #print(x1, y1, x2, y2)

                rect_area = (abs(ax-bx)*frame_length_scale_factor ) * (abs(ay -by)*frame_length_scale_factor )

                img_canvas.create_rectangle(ax, ay, bx, by, outline='yellow', width=2)

                #print("Rect area: ", rect_area, "mm2 from ", hive_area, "mm2 total area")

                coverage = rect_area / hive_area
                score = get_frame_score(coverage)

                # write the data to the record
                dataAudit[imgNum][DAscore] = score
                dataAudit[imgNum][DAmarked] = True
                dataAudit[imgNum][DAtype] = "NOF_r"
                dataAudit[imgNum][DAhive_num] = hive_number
                dataAudit[imgNum][DAhive_type] = hiveType.get()
                dataAudit[imgNum][DAframes] = hiveWidth.get()
                dataAudit[imgNum][DAdepth] = hiveDepth.get()
                dataAudit[imgNum][DAdensity] = density

                # 4x frame length coordinates
                dataAudit[imgNum][DAax] = ax
                dataAudit[imgNum][DAay] = ay
                dataAudit[imgNum][DAbx] = bx
                dataAudit[imgNum][DAby] = by

                data_draw_index = 0
                data_draw=[]
                drawing = False     #stop the drawing thingy from adding more points

                update_record_treeview()  # update the file window with the data

            else:
                data_draw_index += 1

    return
#-------------------------------
def cluster_frame():
    global drawing
    global lengths

    if hive_type_set == False:
        warn_set_hive_type()
        return
    if not dirSelected:
        warn_dir_selected()
        return
    if not frame_length_set:
        warn_frame_select()
        return

    if helptips.get() == 1:
        tkinter.messagebox.showinfo(title="How to...",
                                message="Select the two end points of groups of bees on each frame. "
                                        "You may use multiple lines per frame")
    img_show()  # clears and resets canvas after frame length graphic
    lengths = 0
    check_drawing(4)
    return

def draw_frame_cluster(event):
    global data_draw
    global data_draw_index
    global drawing
    global lengths

    points = 20
    x, y, but = event.x, event.y, event.num
    ended=False

    status_message("Left clicks to draw lines on frames, right click to end. Max 10 lines")

    if drawing and but == 1:
        if data_draw_index<points:
            data_draw.append([x,y])
            img_canvas.create_oval(x-5,y-5,x+5,y+5, fill='blue', outline='yellow',width=1)

            if data_draw_index % 2 !=0:
                img_canvas.create_line(data_draw[data_draw_index][0], data_draw[data_draw_index][1],
                                       data_draw[data_draw_index-1][0], data_draw[data_draw_index-1][1],
                                       width=2, fill='yellow')

                width = data_draw[data_draw_index][0] - data_draw[data_draw_index-1][0]
                height = data_draw[data_draw_index][1] - data_draw[data_draw_index-1][1]
                hypo_length = abs(math.hypot(width, height))
                lengths += hypo_length

            if data_draw_index==points-1:   #finish condition
                ended=True
            else:
                data_draw_index += 1

    else:   #End if right mouse button clicked
        ended = True

    if ended:
        print("total length of bee frames = ", lengths * frame_length_scale_factor,
              "mm of possible", frame_length_total_possible, "mm")
        coverage = (lengths * frame_length_scale_factor) / frame_length_total_possible
        print("So frames : ", coverage * 100, "%")  # percentage of frames covered

        score=get_frame_score(coverage)

        # write the data to the record
        dataAudit[imgNum][DAscore] = score
        dataAudit[imgNum][DAmarked] = True
        dataAudit[imgNum][DAtype] = "NOF_l"
        dataAudit[imgNum][DAhive_num] = hive_number
        dataAudit[imgNum][DAhive_type] = hiveType.get()
        dataAudit[imgNum][DAframes] = hiveWidth.get()
        dataAudit[imgNum][DAdepth] = hiveDepth.get()
        dataAudit[imgNum][DAdensity] = density

        #clear and then write all coordinates for the marker lines

        for i in range(0,40):
            dataAudit[imgNum][DAax + i] = -1

        x=0
        for i in range(0,len(data_draw)):
            for j in range(2):
                dataAudit[imgNum][DAax+x] = data_draw[i][j]
                x+=1


        data_draw_index = 0
        data_draw = []
        drawing = False  # stop the drawing thingy from adding more points

        update_record_treeview()  # update the file window with the data

    return
#------------------------------
def inter_frame():      #bees BETWEEN frames
    global drawing
    global lengths

    if hive_type_set == False:
        warn_set_hive_type()
        return
    if not dirSelected:
        warn_dir_selected()
        return
    if not frame_length_set:
        warn_frame_select()
        return

    if helptips.get() == 1:
        tkinter.messagebox.showinfo(title="How to...",
                                    message="Select the two end points of groups of bees on each frame. "
                                            "You may use multiple lines per frame")
    img_show()  # clears and resets canvas after frame length graphic
    lengths = 0
    check_drawing(5)
    return

def draw_interframe_cluster(event):
    global data_draw
    global data_draw_index
    global drawing
    global lengths

    points = 20
    x, y, but = event.x, event.y, event.num
    ended = False

    status_message("Left clicks to draw lines on frames, right click to end. Max 10 lines")

    if drawing and but == 1:
        if data_draw_index < points:
            data_draw.append([x, y])
            img_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='orange', outline='yellow', width=1)

            if data_draw_index % 2 != 0:
                img_canvas.create_line(data_draw[data_draw_index][0], data_draw[data_draw_index][1],
                                       data_draw[data_draw_index - 1][0], data_draw[data_draw_index - 1][1],
                                       width=2, fill='yellow')

                width = data_draw[data_draw_index][0] - data_draw[data_draw_index - 1][0]
                height = data_draw[data_draw_index][1] - data_draw[data_draw_index - 1][1]
                hypo_length = abs(math.hypot(width, height))
                lengths += hypo_length

            if data_draw_index == points - 1:  # finish condition
                ended = True
            else:
                data_draw_index += 1

    else:  # End if right mouse button clicked
        ended = True

    if ended:
        print("total length of bee frames = ", lengths * frame_length_scale_factor,
              "mm of possible", frame_length_total_possible, "mm")
        coverage = (lengths * frame_length_scale_factor) / frame_length_total_possible
        print("So frames : ", coverage * 100, "%")  # percentage of frames covered

        score = get_frame_score(coverage)

        # write the data to the record
        dataAudit[imgNum][DAscore] = score
        dataAudit[imgNum][DAmarked] = True
        dataAudit[imgNum][DAtype] = "IFB"
        dataAudit[imgNum][DAhive_num] = hive_number
        dataAudit[imgNum][DAhive_type] = hiveType.get()
        dataAudit[imgNum][DAframes] = hiveWidth.get()
        dataAudit[imgNum][DAdepth] = hiveDepth.get()
        dataAudit[imgNum][DAdensity] = density

        # clear and then write all coordinates for the marker lines

        for i in range(0, 40):
            dataAudit[imgNum][DAax + i] = -1

        x = 0
        for i in range(0, len(data_draw)):
            for j in range(2):
                dataAudit[imgNum][DAax + x] = data_draw[i][j]
                x += 1

        data_draw_index = 0
        data_draw = []
        drawing = False  # stop the drawing thingy from adding more points

        update_record_treeview()  # update the file window with the data
    return

#---------------------------manual audit input----------------------------------------

def manual_mode():
    global manual_audit
    global label_manual


    if hive_type_set == False:
        warn_set_hive_type()
        return

    if manual_audit == True:
        manual_audit = False


        button_manual = Button(ctr_left, text="Manual audit", bg='#f0f0f0', command=lambda: manual_mode())

        # make the frame length button highlighted to show the first step
        button_set_frame_length = Button(ctr_left, text="Set Frame Length", bg='lightcoral',
                                         command=lambda: set_frame_length())
        button_set_frame_length.grid(row=8, column=0, sticky=W + E, pady=2, padx=2)
        entry_density.config(state="normal")
    else:
        manual_audit = True

        button_manual = Button(ctr_left, text="Manual audit", bg='cornflowerblue', fg='white', command=lambda: manual_mode())

        #make the frame length button normal
        button_set_frame_length = Button(ctr_left, text="Set Frame Length", bg='#f0f0f0',
                                         command=lambda: set_frame_length())
        button_set_frame_length.grid(row=8, column=0, sticky=W + E, pady=2, padx=2)
        label_manual = Label(ctr_left, text="Keypad to score:\n\n0-9 and '*'=10\n '+' & '-' to move\n'b' to set brood box", fg='black')
        label_manual.grid(row=17, column=0, sticky=W + E, pady=2, padx=10)

        entry_density.config(state="disabled")

    button_manual.grid(row=16, column=0, sticky=W + E, pady=2, padx=2)
    check_keyboard()  # set the keyboard mode

    return

#-------------------------------- Keyboard functions
def check_keyboard():

    keyboard.unhook_all()

    if manual_audit:
        list = ("-", "+", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "b", "r")
    else:
        list = ("-", "+", "b", "r")
    for x in list:
        keyboard.on_press_key(x, keypress_manual_entry)

    entry_density.bind("<Return>",set_density)
    return

def keypress_manual_entry(event):
    print("focus check" , focus_check)
    if manual_audit == True:
        score=99
        if event.name == "*":  #ten pointer!
            score = 10
            dataAudit[imgNum][DAscore] = score
            dataAudit[imgNum][DAmarked] = True
            dataAudit[imgNum][DAtype] = "Man"
            dataAudit[imgNum][DAhive_num] = hive_number
            dataAudit[imgNum][DAhive_type] = hiveType.get()
            dataAudit[imgNum][DAframes] = hiveWidth.get()
            dataAudit[imgNum][DAdepth] = hiveDepth.get()

            update_record_treeview()
            if autoprogress.get() == 1:
                next_img()
            else:
                tree.selection_set(imgNum) #highlight current record again
        else:
            try:        #Need this as arrow keys still cause the event
                score = int(event.name)
                dataAudit[imgNum][DAscore] = score
                dataAudit[imgNum][DAmarked] = True
                dataAudit[imgNum][DAtype] = "Man"
                dataAudit[imgNum][DAhive_num] = hive_number
                dataAudit[imgNum][DAhive_type] = hiveType.get()
                dataAudit[imgNum][DAframes] = hiveWidth.get()
                dataAudit[imgNum][DAdepth] = hiveDepth.get()

                update_record_treeview() #update current record
                if autoprogress.get() == 1:
                    next_img()
                else:
                    tree.selection_set(imgNum)  # highlight current record again

            except:
                score = 99

    if event.name == "+" or event.name=="=":
        next_img()
    if event.name == "-" or event.name=="_":
        prev_img()

    if event.name == "b":
        if dataAudit[imgNum][DAbroodbox] == 0:
            dataAudit[imgNum][DAbroodbox] = 1
        else:
            dataAudit[imgNum][DAbroodbox] = 0

        update_record_treeview()
        if autoprogress.get() == 1:
            next_img()
        else:
            tree.selection_set(imgNum)  # highlight current record again
    return


def set_density(event):
    try:
        percentage = int(entry_density.get())
        if percentage >= 0 and percentage <= 100:
            dataAudit[imgNum][DAdensity] = int(entry_density.get())
            update_record_treeview()

        else:
            density = 100
            tkinter.messagebox.showinfo(title="How to...",
                                        message="Density must be an integer between 0 and 100")
            entry_density.delete('0', 'end')
            entry_density.insert(0, 100)
    except:
        density = 100
        tkinter.messagebox.showinfo(title="How to...",
                                    message="Density must be an integer between 0 and 100")
        entry_density.delete('0', 'end')
        entry_density.insert(0, 100)

#nav bar functions Functions ----------------------------------------------------------------------

def next_img():
    global imgNum

    if imgNum <imgMax-1:
        imgNum+=1
        update_record_treeview() #update current record
        tree.selection_set(imgNum) #move to next
    return

def prev_img():
    global imgNum

    if imgNum >0:
        imgNum-=1
        update_record_treeview()
        tree.selection_set(imgNum)
    return

def first_img():
    global imgNum

    imgNum = 0
    update_record_treeview()
    tree.selection_set(imgNum)
    return

def last_img():
    global imgNum

    imgNum = imgMax-1
    update_record_treeview()
    tree.selection_set(imgNum)
    return

def hive_num_decrement():
    global hive_number
    if hive_number >0:
        hive_number -=1
        entry_hive_num.delete('0','end')
        entry_hive_num.insert(0, hive_number)  # sets start value
        entry_hive_num.grid(row=0, column=2, sticky=W + E, padx=5)
        hive_num_set()
    return

def hive_num_increment():
    global hive_number
    hive_number +=1
    entry_hive_num.delete('0', 'end')
    entry_hive_num.insert(0, hive_number)  # sets start value
    entry_hive_num.grid(row=0, column=2, sticky=W + E, padx=5)
    hive_num_set()
    return

def hive_num_set():
    global entry_hive_num
    global hive_number
    global dataAudit

    new_num = entry_hive_num.get()
    try:
        hive_number = int(new_num)
        dataAudit[imgNum][DAhive_num] = hive_number
        update_record_treeview()
    except:
        tkinter.messagebox.showwarning(title='Ooops!', message="That's not a number!\nEnter a number between 0 and 99 bazillion...")


    return

def hive_num_repeat():
    global entry_hive_num
    global hive_number
    global dataAudit

    entry_hive_num.delete('0', 'end')
    entry_hive_num.insert(0, hive_number)  # sets start value
    entry_hive_num.grid(row=0, column=2, sticky=W + E, padx=5)
    dataAudit[imgNum][DAhive_num] = hive_number
    update_record_treeview()
    return




#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

def window_foc(event):

    if "FocusIn" in str(event):
        #print("focus in!")
        focus_check = True
    if "FocusOut" in str(event):
        #print("focus out!")
        focus_check = False
    #print("focus check" , focus_check)

focus_check = False
root.bind('<FocusOut>', window_foc)
root.bind('<FocusIn>', window_foc)



status_message("To start, set hive type and image folder, then set frame length or use manual mode.")

check_keyboard()

tree.bind('<<TreeviewSelect>>', file_selected) #when a file is selected

root.mainloop()

# Collapse all/ expand all : Ctrl+Shift+NumPad - / Ctrl+Shift+NumPad +
"""
# To do list.... 
Zero button for shape modes
Add %age buttons for density
Extract EXIF DATA

-Doesn't redraw line data whenmax lines reached and score calculated.
Doesnt force set frame length anymore... Done - too much - even when redrawing shapes
reclaculate frame score on density change
Add a big file number somewhere...
When redrawing shapes, remove old one
Allow drawing point dragging.
div by zero error in the frame length calbration..... occasional..

Done.. show_files() - This REALLY SLOWS THNGS DOWN - Can we update without redoing the entire window?
        .. became update_record_treeview() and build_treeview

Done..-Audit data save file not in image folder!!! Fixed 17-6-22
Done.. Persistent hive number - but frame lines sets last hive num...

Done... -repeat last hive num button (i.e repeat!)
Done...-hive numb hot key?
Done...-main (brood) box column?

Done...-auto next image function, i.e. when you score or number it moves to the next record.
Done...-auto center current record in the file window

Done... Centre image
-Rotate image
-Zero Frames button ????
-Scalable: At the moment, resizing the window(disabled) will resize the image but the original line pixel data do not scale
    May need to store the image size at which the data was added, then use this to compute a scale factor for the 
    data coordinates.
"""




