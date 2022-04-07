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
        
        #main Variables of the Program
        self.entry_text = StringVar()
        self.path_text = ""
        self.perc_progr = ""
        self.stop_threads = False
        
        #main window with widgets
        self.mainframe = Frame(root)
        self.ety_link = Entry(root,width=60)
        self.ety_link.grid(row=0,column=0,padx=5,pady=5)
        self.btn_link = Button(root, text="Download", command=self.main)
        self.btn_link.grid(row=0,column=1,padx=5,pady=5)
        self.ety_path = Entry(root, text="", width=60, state=DISABLED, textvariable=self.entry_text)
        self.ety_path.grid(row=1,column=0,padx=5,pady=5)
        self.btn_path = Button(root, text="Choose Path", command=self.select_path)
        self.btn_path.grid(row=1,column=1,columnspan=2,padx=5,pady=5)
        self.lbl_fdbck = Label(root, text="")
        self.lbl_fdbck.grid(row=2,column=0,padx=5,pady=5)
        self.lbl_info = Label(root, text='If no folder has been chosen the file will be saved in the "videos" subfolder.')
        self.lbl_info.grid(row=3,column=0,columnspan=2,padx=5,pady=5)

        #download window with widgets
        self.win = Toplevel(root)
        self.win.transient()
        self.win.withdraw()
        self.prb_loading = Progressbar(self.win, orient=HORIZONTAL, mode='determinate', length=280)
        self.prb_loading.grid(row=0,column=0, padx=20, pady=20)
        self.lbl_loading = Label(self.win, text="Downloading...")
        self.lbl_loading.grid(row=1,column=0,padx=20,pady=20)
        #self.win.protocol("WM_DELETE_WINDOW", self.on_closing) can  not be used due to ydl
        self.win.protocol("WM_DELETE_WINDOW", self.exit)

    #selects the destination path of your download
    def select_path(self):        
        currdir = os.getcwd()
        self.path_text = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        self.entry_text.set(self.path_text)

    #is the main Code that is being executed once the Download-Button has been clicked
    def main(self):

        #the enterd path is being validated
        #if the user didn#t give a specific path, the video will be saved in
        #a subfolder called 'video'
        entered_link = self.ety_link.get()
        if self.path_text == "":
            ydl_opts = {
                'outtmpl': '/videos/%(title)s.%(ext)s',
                'progress_hooks': [self.my_hook],
            }
        else:
            ydl_opts = {
                'outtmpl': '' + self.path_text + '/%(title)s.%(ext)s',
                'progress_hooks': [self.my_hook],
            }
        
        #the URL is being validated. If it's not, a message will be sent to a label
        valid_url = self.is_supported(entered_link)
        if valid_url == True:
            self.win.deiconify()
            self.lbl_fdbck.config(text="DOWNLOADING...")
            self.win.grab_set()
            self.download_thread(ydl_opts,entered_link)
        else:
            self.lbl_fdbck.config(text='Please enter a valid URL-Address.')

    #checks if the entered URL is a valid one, if not, a corresponding message will be displayed
    def is_supported(self,url):
        extractors = youtube_dl.extractor.gen_extractors()
        for e in extractors:
            if e.suitable(url) and e.IE_NAME != 'generic':
                return True
        return False

    #the download needs to be a parallel process so that the GUI is still functional
    def download_thread(self,ydl_opts,entered_link):
        global t
        def callback():
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([entered_link])
        t = threading.Thread(target=callback)
        t.start()

    #gibt den aktuellen Status des Downloads wieder 
    def my_hook(self,d):
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
            self.win.grab_release()
            try:
                self.win.withdraw()
                self.lbl_fdbck.config(text="DOWNLOAD FINISHED")
                self.prb_loading['value'] = 0
            except:
                pass

        if d['status'] == 'downloading':
            try:
                load_percentage = d['_percent_str']
                self.lbl_loading.config(text="Downloading..." + load_percentage) 
                print(load_percentage)
                new = self.convert_rate(load_percentage)
                self.prb_loading['value'] = new
            except:
                pass

    #converts the "load_percantage" String value into a usable float for the Loading Bar
    def convert_rate(self,input):
        input = input[:-1]
        input = input.replace(" ","")
        float(input)
        return input

    #this section was originally for cancelling the download
    #unfortunetely I couldn't find a good way to cancel said download...
    """ ***can not be used due to ydl***
    def on_closing(self): #closing the download window -> cancel the download
        if messagebox.askokcancel("Quit", "Do you want to cancel the Download?"):
            self.stop_threads = True
            self.win.destroy()
    """
    #...that is why this function stopps the user from exiting the download window
    #all together
    def exit(self):
        "dummy function"
        pass

m = Main(root)
root.mainloop()