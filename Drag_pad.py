""" Dragon IDE Developed by Pralse James,
Simple IDE for coding dragon, done for the sake of coding dragon,
had to make mine due to cmd error (0xc0000142)
"""
#NOTE: this program was made for personal use so, don't come bugging the developer with stuff
#like, 'i want to change the theme to what i like', 'i want the search bar to be activated and
#deactivated how/when i like', 'i want to deactivate
#the line numbers', if you want stuff like that so bad, you can make it that way, we believe you can
#do it that way, this is all to say that you should not expect new versions of this program, and
#should not in any way judge or suggest any stuff, it is only made for personal use, so with all due
#respect... your opinions are not needed, UNLESS you're friends with the developer, and that would
#only happen privately

import subprocess
import tkinter 
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *

import tkinter as tk

class DragPad(tk.Canvas, tk.Text):
    root = Tk()
    #--default window width and height--
    the_width = 300
    the_height = 500
    textArea = Text(root, bg = "Black", insertbackground = "White", foreground = "White", font = "Calibri")
    menuBar = Menu(root)
    FileMenu = Menu(menuBar, tearoff = 0)
    EditMenu = Menu(menuBar, tearoff = 0)
    HelpMenu = Menu(menuBar, tearoff = 0)
    SetMenu = Menu(menuBar, tearoff = 0)

    #--add scroll bar--
    scr = Scrollbar(textArea)
    file = None

    def __init__(self, *args, **kwargs):

        #-open new file-
        self.FileMenu.add_command ( label = "New", command = self.newFile)
        #-open already existing file-
        self.FileMenu.add_command ( label = "Open", command = self.openFile)
        #-save current file-
        self.FileMenu.add_command(label = "Save", command = self.saveFile)
        #-create line in the dialog-
        self.FileMenu.add_command (label = "Exit", command = self.quitApplication)
        #-cut-
        self.EditMenu.add_command (label = "Cut", command = self.cut)
        #-copy-
        self.EditMenu.add_command ( label = "Copy", command = self.copy)
        #--paste--
        self.EditMenu.add_command (label = "Paste", command = self.paste)
        #SEARCH
        #self.EditMenu.add_command (label = "Find", command = init_search())
        #-about-
        self.HelpMenu.add_command (label = "About ", command = self.ShowAbout)
         #-Filing-
        self.menuBar.add_cascade ( label = "File", menu = self.FileMenu)
        #Editing
        self.menuBar.add_cascade ( label = "Edit", menu = self.EditMenu)
        self.menuBar.add_cascade(label = "Help", menu = self.HelpMenu)
        self.root.config ( menu = self.menuBar)
        self.scr.pack ( side = RIGHT,fill = Y)
        
        #Text line numbers
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        
        #custom text
        tk.Text.__init__(self, *args, **kwargs)
        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

        global text, edit
        #self.root = root
        #self.root.title("Find...")
        self.frame = Frame(self.root) 
        self.Label = Label(self.frame, text = "Search...").pack(side = LEFT)
        self.edit = Entry(self.frame)
        self.edit.pack(side = LEFT, fill = BOTH, expand = 1)
        self.edit.focus_set()
        self.btn = Button(self.frame, text = 'SEARCH')
        self.btn.pack(side = RIGHT)
        self.btn2 = Button(self.frame, text = 'CLOSE')
        self.btn2.pack(side = RIGHT)
        self.frame.grid(row = 1)

        self.text = DragPad.textArea

        self.btn.config(command = self.find)
        self.btn2.config(command = self.leave)
        #-set icon-
        try:
            self.root.wm_iconbitmap("Notepad.ico")
        except:
            pass
        #-set windows size-
        try:
            self.the_width = kwargs['width']
        except KeyError : 
            pass

        #--set windows text--
        self.root.title ("Untitled - DragPad 1.0")
        #-centre window-
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        #-For left-align-
        left = (screenWidth / 2) - (self.the_width / 2)
        #-For right align-
        top = (screenHeight / 2) - (self.the_height / 2)
        #-For top and bottom-
        self.root.geometry('%dx%d+%d+%d'  %  (self.the_width, self.the_height, left, top))
        #-make textarea resizable-
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)
        #-add controls (widget)-
        self.textArea.grid(sticky = N + E + S + W)
        
        #Scrollbar auto adjust
        self.scr.config(command = self.textArea.yview)
        self.textArea.config(yscrollcommand = self.scr.set)

    def attach(self, text_widget):self.textwidget = text_widget

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or args[0:3] == ("mark", "set", "insert") or args[0:2] == ("xview", "moveto") or args[0:2] == ("xview", "scroll") or args[0:2] == ("yview", "moveto") or args[0:2] == ("yview", "scroll")):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

    def quitApplication(self): self.root.destroy() #exit

    def ShowAbout(self): showinfo ("Drag-pad 1.0", "made by Praise James for sake of order to Dragon programming\n because of the state of his cmd(0xc0000142),\n this program run's dragon code with python's subprocess module ")

    def openFile(self):
        self.file = askopenfilename(defaultextension = " .dng", filetypes = [("All Files", "*.*"), ("Text Documents" , "*.txt") ])
        if self.file == " ":
            #no file to open
            self.file = None
        else:
            #Try to open the file
            #set the window title
            self.root.title (os.path.basename(self.file) + " - Drag-pad 1.0")
            self.textArea.delete(1.0, END)
            try:
                file = open(self.file, "r")
                self.textArea.insert(1.0, file.read())
                file.close()
            except FileNotFoundError:
                showinfo ("ALERT", "Hey, you didn't open a file")
 
    def newFile(self):
        self.root.title("Untitled - Drag-pad1.0")
        self.file = None
        self.textArea.delete(1.0, END)
        
    def saveFile(self):
        if self.file == None:
            #save as new file
            self.file = asksaveasfilename (initialfile = 'Untitled.txt', defaultextension = " .txt", filetypes = [("All Files", "*.*"), ("Text Documents", "* .txt")])

            if self.file == " ":
                self.file == None
            else:
                try:
                    file = open(self.file, "w+")
                    file.write(self.textArea.get(1.0, END))
                    file.close()

                    #Change the windows  title
                    self.root.title(os.path.basename(self.file) + " - Drag-pad 1.0")
                except FileNotFoundError:
                    pass
        else:
            try:
                file = open(self.file, "w+")
                file.write(self.textArea.get(1.0, END))
                file.close()
            except FileNotFoundError:
                pass
    
    def  cut(self):
        try:
            self.textArea.event.generate("<<Cut>>")
        except AttributeError:
            showinfo("HEY",  "Nothing to cut")
            
    def copy(self):
        try:
            self.textArea.event.generate("<<Copy>>")
        except AttributeError:
            showinfo("HEY", "you haven't written anything")

    def paste(self):
        try:
            self.textArea.event.generate("<<Paste>>")
        except AttributeError:
            showinfo("HEY", "You've got nothing to paste")

    def run (self): self.root.mainloop()          
        

    def find(self):
        self.text.tag_remove('found', '1.0', END)
        self.s = self.edit.get()
        if self.s:
            self.idx = '1.0'
            while 1:
                self.idx = self.text.search(self.s, self.idx, nocase = 1, stopindex = END)
                if not self.idx:break
                self.lastidx = '%s+%dc' % (self.idx, len(self.s))
                self.text.tag_add('found', self.idx, self.lastidx)
                self.idx = self.lastidx
            self.text.tag_config('found', background = 'blue')
        self.edit.focus_set()

    def leave(self):self.root.destroy()
    
if __name__=='__main__':
    DragPad = DragPad(width = 600, height = 400)
    DragPad
