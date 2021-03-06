from turtle import left
import ipInfo
from tkinter import * 

#create root window
root = Tk()
root.title('Get your IP Location')

#set windows size as fixed
root.minsize(330, 200)
root.maxsize(330, 200)

#value for Radiobuttons
var = IntVar()

#definierung der Hauptklasse
class Main:
    #initialisierung der Hauptklasse
    def __init__(self, root) -> None:

        #UI declarations and positions
        self.mainframe = Frame(root)
        self.lbl_info = Label(root, text="Enter an IP or URL:",justify="left")
        self.lbl_rslts = Label(root, text="",width=25, justify=LEFT, anchor="w")
        self.eny_ipA = Entry(root, text="",width=25,justify="left")
        self.btn_search = Button(root, text="Search", command=self.clicked_button)
        self.clr_entry = Button(root,text="Clear",command=self.clear_text)
        
        self.lbl_info.grid(row=0, column=0, padx=5, pady=5)
        self.eny_ipA.grid(row=0, column=1, padx=5, pady=5)
        self.clr_entry.grid(row=0, column=2, padx=0, pady=5)
        self.btn_search.grid(row=1, column=1, padx=5, pady=5)
        self.lbl_rslts.place(x=5,y=40)

    #executed by btn_search if clicked 
    def clicked_button(self):

        gtn_adrs = ""
        entered_url = self.eny_ipA.get()

        #is the Entry empty the Result-Label returns a request to do so in return (in URL or IP)
        if entered_url == "":
            self.lbl_rslts.config(text="Please enter an URL or IP.")
            
        else:
            gtn_adrs = ipInfo.get_ip(entered_url)
                
            #Request of Location data for the IP-Adress
            location_data = ipInfo.get_location(gtn_adrs)
                
            #the location_data is being seperated in single values
            this_ip = location_data["ip"]
            this_city = location_data["city"]
            this_region = location_data["region"]
            this_country = location_data["country"]
                
            #if there are no problems, the program uses these values for the location output
            try:
                self.lbl_rslts.config(text=this_ip + "\n" + this_city + "\n" + this_region + "\n" + this_country)
            except:
                self.lbl_rslts.config(text="Please enter a valid Adress.")

    #clears the Entry Widget
    def clear_text(self):
        self.eny_ipA.delete(0, END)

#Abrufung der Hauptklasse
m = Main(root)

root.mainloop()