import youtube_dl
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
import os
import threading

"""
This Program uses youtube_dl for downloading Youtube video URLs.
"""

#create root window
root = Tk()
root.title('YouTube Download')

#set fixed window size
root.minsize(460, 200)
root.maxsize(460, 200)

class Main:
    def __init__(self, root) -> None:
        """
        Initialises Variables, Windows and Widgets of the Code.
        """
        #main Variables of the Program
        self.entry_text = StringVar()   #the String for the URL
        self.path_text = ""             #the String for the Path
        self.perc_progr = ""            #percentage progress
        
        #main window with widgets
        self.mainframe = Frame(root)
        self.ety_link = Entry(root,width=60)#Entry for Youtube URL
        self.ety_link.grid(row=0,column=0,padx=5,pady=5)
        self.btn_link = Button(root, text="Download", command=self.validate)#starts the Download
        self.btn_link.grid(row=0,column=1,padx=5,pady=5)
        self.ety_path = Entry(root, text="", width=60, state=DISABLED, textvariable=self.entry_text)#shows entered destination of Download File
        self.ety_path.grid(row=1,column=0,padx=5,pady=5)
        self.btn_path = Button(root, text="Choose Path", command=self.select_path)#determines Destination of Download File
        self.btn_path.grid(row=1,column=1,columnspan=2,padx=5,pady=5)
        self.lbl_fdbck = Label(root, text="")#returns State of the Download
        self.lbl_fdbck.grid(row=2,column=0,padx=5,pady=5)
        self.lbl_info = Label(root, text='If no folder has been chosen the file will be saved in the "videos" subfolder.')#Informationlabel
        self.lbl_info.grid(row=3,column=0,columnspan=2,padx=5,pady=5)

        #download window with widgets
        self.d_win = Toplevel(root)
        self.d_win.transient()
        self.d_win.withdraw()
        self.prb_loading = Progressbar(self.d_win, orient=HORIZONTAL, mode='determinate', length=280)#shows progress of download
        self.prb_loading.grid(row=0,column=0, padx=20, pady=20)
        self.lbl_loading = Label(self.d_win, text="Downloading...")
        self.lbl_loading.grid(row=1,column=0,padx=20,pady=20)
        #self.win.protocol("WM_DELETE_WINDOW", self.on_closing) can not be used due to ydl

    #selects the destination path of your download
    def select_path(self):
        """
        Opens a window where the user can choose the destination of his download file and puts said path in an readonly Entry
        """ 
        currdir = os.getcwd()
        self.path_text = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        self.entry_text.set(self.path_text)

    #is the main Code that is being executed once the Download-Button has been clicked
    def validate(self):
        """
        Organises all functions of the download process
        """

        #the enterd path of the end file is being validated
        #if the user didn't give a specific path, the video will be saved in
        #a subfolder called 'video'
        if self.path_text == "":

            ydl_opts = {
                #determines path when empty: /videos/
                'outtmpl': '/videos/%(title)s.%(ext)s',
                #determines status of download
                'progress_hooks': [self.my_hook],
            }

        else:
            
            ydl_opts = {
                #determines path:
                'outtmpl': '' + self.path_text + '/%(title)s.%(ext)s',
                #determines status of download
                'progress_hooks': [self.my_hook],
            }
        
        #the enterd URL is being validated
        entered_link = self.ety_link.get()
        valid_url = self.is_supported(entered_link)
        if valid_url:

            #if the url is valid, d_win Window appears and the Feedback Label is being updated
            #after that, the actual download_thread is activated 
            self.d_win.deiconify()
            self.lbl_fdbck.config(text="DOWNLOADING...")
            self.d_win.grab_set()
            self.download_thread(ydl_opts,entered_link)

        else:

            #if the URL is invalid, the Feedback Label returns an error message
            self.lbl_fdbck.config(text='Please enter a valid URL-Address.')

    #checks if the entered URL is a valid one, if not, a corresponding message will be displayed
    def is_supported(self,url):
        """
        Checks if the entered URL is valid and returns the corresponding boolean value.
        """
        #extractor is being created
        extractors = youtube_dl.extractor.gen_extractors()
        for e in extractors:
            #if the extractor finds the url suitable it returns a true value, 
            #if not it returns a false value
            if e.suitable(url) and e.IE_NAME != 'generic':
                return True
        return False

    #the download needs to be a parallel process so that the GUI is still functional
    def download_thread(self,ydl_opts,entered_link):
        """
        Activates a seperate Thread for the Youtube_dl-Download 
        """
        global t
        #creates a loop that makes the thread functioning beside the GUI Thread 
        def callback():
            #Youtube_dl starts it's own download methods
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([entered_link])
        t = threading.Thread(target=callback)
        #the thread starts
        t.start()

    #gibt den aktuellen Status des Downloads wieder 
    def my_hook(self,d):
        """
        Returns the state of the Download to the GUI.
        """
        #if the download-thread is still going, the progress is being shown in the Progressbar of d_win
        if d['status'] == 'downloading':
            try:
                load_percentage = d['_percent_str']
                self.lbl_loading.config(text="Downloading..." + load_percentage) 
                new = self.convert_rate(load_percentage)
                self.prb_loading['value'] = new
            except:
                pass

        #if the Download is finished the d_win is being closed
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
            self.d_win.grab_release()
            try:
                self.d_win.withdraw()
                self.lbl_fdbck.config(text="DOWNLOAD FINISHED")
                self.prb_loading['value'] = 0
            except:
                pass


    #converts the "load_percantage" String value into a usable float for the Loading Bar
    def convert_rate(self,input):
        """
        Converts downloading progress into usable float value to use in the download Progressbar.
        """
        input = input[:-1]
        input = input.replace(" ","")
        float(input)
        return input

m = Main(root)
root.mainloop()