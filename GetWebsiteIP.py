from cgitb import text
from cmath import e
from ctypes import alignment
import requests
from tkinter import *

root = Tk()
root.title('Get your IP Location')
root.geometry("430x200")

class Main:

    def __init__(self, root) -> None:
        mainwindow = Frame(root)
        mainwindow.pack()

        self.Lbl_Infos = Label(root, text="Enter the IP-Adress:",justify="left", font=('Arial',15))
        self.Lbl_Rslts = Label(root, text="sjkdakjdkjasbdkjasbdkjsabd", justify=LEFT, font=('Arial',15))
        self.Ent_ipA = Entry(root, text="",justify="left", font=('Arial',15))
        self.Btn_Search = Button(root, text="Search", font=('Arial',15), command=self.get_location)

        self.Lbl_Infos.place(x=5, y=10, width=200, height=20)
        self.Ent_ipA.place(x=215, y=5, width=200, height=30)
        self.Btn_Search.place(x=340, y=50, width=70, height=40)
        self.Lbl_Rslts.place(x=5, y=50, width=360, height=100)

    def get_ip(self,ipA_):
        response = requests.get(ipA_).json()
        return response["ip"]

    def get_location(self):
        enteredIP = self.Ent_ipA.get()
        #'https://api64.ipify.org?format=json'
        ip_address = self.get_ip(enteredIP)
        response = requests.get(f'https://ipinfo.io/{ip_address}').json()
        location_data = {
            "ip": ip_address,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country")
        }
        
        thisIp = location_data["ip"]
        thisCity = location_data["city"]
        thisRegion = location_data["region"]
        thisCountry = location_data["country"]
        
        Answer = thisIp + '\n' + thisCity + '\n' + thisRegion + '\n' + thisCountry
        self.Lbl_Rslts.config(text = Answer)

        return location_data

m = Main(root)

root.mainloop()