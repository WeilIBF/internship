from statistics import mode
import youtube_dl
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import tkinter.filedialog
import os
import threading

#create root window
root = Tk()
root.title('YouTube Download')
root.minsize(460, 200)
root.maxsize(460, 200)

class Main:
    def __init__(self, root) -> None:
        
        self.entry_text = StringVar()
        self.path_text = ""
        
        self.mainframe = Frame(root)
        self.ety_link = Entry(root,width=60)
        self.ety_link.grid(row=0,column=0,padx=5,pady=5)
        self.btn_link = Button(root, text="Download", command=self.download)
        self.btn_link.grid(row=0,column=1,padx=5,pady=5)
        self.ety_path = Entry(root, text="", width=60, state=DISABLED, textvariable=self.entry_text)
        self.ety_path.grid(row=1,column=0,padx=5,pady=5)
        self.btn_path = Button(root, text="Choose Path", command=self.select_path)
        self.btn_path.grid(row=1,column=1,columnspan=2,padx=5,pady=5)
        self.lbl_fdbck = Label(root, text="")
        self.lbl_fdbck.grid(row=2,column=0,padx=5,pady=5)
        self.lbl_info = Label(root, text='If no folder has been chosen the file will be saved in the "videos" subfolder.')
        self.lbl_info.grid(row=3,column=0,columnspan=2,padx=5,pady=5)

        self.win = Toplevel(root)
        self.win.transient()
        self.win.withdraw()
        self.prb_loading = Progressbar(self.win, orient=HORIZONTAL, mode='indeterminate', length=280)
        self.prb_loading.grid(row=0,column=0, padx=20, pady=20)
        self.lbl_loading = Label(self.win, text="Downloading...")
        self.lbl_loading.grid(row=1,column=0,padx=20,pady=20)
    
    def select_path(self):        
        currdir = os.getcwd()
        self.path_text = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        self.entry_text.set(self.path_text)

    def my_hook(self,d):
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
            self.prb_loading.stop()
            self.win.grab_release()
            self.win.withdraw()
            self.lbl_fdbck.config(text="DOWNLOAD FINISHED")

    def download(self):
        entered_link = self.ety_link.get()
        if self.path_text == "":
            ydl_opts = {
                'outtmpl': '/videos/%(title)s.%(ext)s',
                'progress_hooks': [self.my_hook],
            }
        else:
            ydl_opts = {
                'outtmpl': '' + self.path_text + '/%(title)s',
                'progress_hooks': [self.my_hook],
            }
        self.win.deiconify()
        try:
            self.lbl_fdbck.config(text="DOWNLOADING...")
            self.win.grab_set()
            self.prb_loading.start()
            def callback():
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([entered_link])
            t = threading.Thread(target=callback)
            t.start()
        except:
            self.lbl_fdbck.config(text="Please enter a valid URL-address.")

    def on_closing(self): #closing the download window -> cancel the download
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.win.destroy()

self.win.protocol("WM_DELETE_WINDOW", Main.on_closing) #triggered when download window is being closed 
m = Main(root)
root.mainloop()