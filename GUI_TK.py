from cgitb import text
from cmath import e
from ctypes import alignment
import ipInfo
from tkinter import *

root = Tk()
root.title('Get your IP Location')
root.geometry("430x200")
var = IntVar()

class Main:

    def __init__(self, root) -> None:
        mainwindow = Frame(root)
        mainwindow.pack()

        self.ChsType = 0

        self.Lbl_Infos = Label(root, text="Enter the IP-Adress:",justify="left", font=('Arial',15))
        self.Lbl_Rslts = Label(root, text="", justify=LEFT, font=('Arial',15))
        self.Ent_ipA = Entry(root, text="",justify="left", font=('Arial',15))
        self.Btn_Search = Button(root, text="Search", font=('Arial',15), command=self.clickedButton)
        self.R1 = Radiobutton(root, text="URL Adress", variable=var, value=1, command=self.sel)
        self.R2 = Radiobutton(root, text="IP Adress", variable=var, value=2, command=self.sel)

        self.Lbl_Infos.place(x=5, y=10, width=200, height=20)
        self.Ent_ipA.place(x=215, y=5, width=200, height=30)
        self.Btn_Search.place(x=340, y=50, width=70, height=40)
        self.Lbl_Rslts.place(x=5, y=50, width=360, height=100)
        self.R1.place(x=280, y=100)
        self.R2.place(x=280, y=140)

    def clickedButton(self):
        print(self.ChsType)
        if self.ChsType == 0:
            self.Lbl_Rslts.config(text="Please choose \nIP or URL Mode.")
        else:
            enteredURL = self.Ent_ipA.get()
            gtnAdrs = ipInfo.getIp(enteredURL)
            if gtnAdrs == "Null":
                self.Lbl_Rslts.config(text="Please enter a valid Adress.")
            location_data = ipInfo.getLocation(gtnAdrs)

            thisIp = location_data["ip"]
            thisCity = location_data["city"]
            thisRegion = location_data["region"]
            thisCountry = location_data["country"]

            self.Lbl_Rslts.config(text=thisIp + "\n" + thisCity + "\n" + thisRegion + "\n" + thisCountry)

    def sel(self):
        self.ChsType = str(var.get())

m = Main(root)

root.mainloop()