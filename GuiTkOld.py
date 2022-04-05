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
        #variable for URL-/Ip-Mode Selection
        self.chs_type = 0

        #UI declarations and positions
        self.mainframe = Frame(root)
        self.lbl_info = Label(root, text="Enter the IP-Adress:",justify="left")
        self.lbl_rslts = Label(root, text="",width=25, justify="left")
        self.eny_ipA = Entry(root, text="",width=25,justify="left")
        self.btn_search = Button(root, text="Search", command=self.clicked_button)
        self.r1 = Radiobutton(root, text="URL Adress", variable=var, value=1, command=self.sel)
        self.r2 = Radiobutton(root, text="IP Adress", variable=var, value=2, command=self.sel)
        self.clr_entry = Button(root,text="Clear",command=self.clear_text)
        
        self.lbl_info.grid(row=0, column=0, padx=5, pady=5)
        self.eny_ipA.grid(row=0, column=1, padx=5, pady=5)
        self.clr_entry.grid(row=0, column=2, padx=0, pady=5)
        self.btn_search.grid(row=1, column=1, padx=5, pady=5)
        self.lbl_rslts.place(x=5,y=110)
        self.r1.grid(row=1, column=0, padx=5, pady=0)
        self.r2.grid(row=2, column=0, padx=5, pady=0)

    #executed by btn_search if clicked 
    def clicked_button(self):
        #if no Adress-Mode has been choosen the user is getting a request to do so in return
        if self.chs_type == 0:
            self.lbl_rslts.config(text="Please choose \nIP or URL Mode.")
        else:

            gtn_adrs = ""
            entered_url = self.eny_ipA.get()

            #is the Entry empty the Result-Label returns a request to do so in return (in URL or IP)
            if entered_url == "":
                if self.chs_type == "1":
                    self.lbl_rslts.config(text="Please enter an URL.")
                elif self.chs_type == "2":
                    self.lbl_rslts.config(text="Please enter an IP.")

            #this is an exception in this request
            #to keep the program consistent this request stopps the user from successfully entering an IP-Adress
            #in the URL-Mode (possibly can be resolved through optimization)  
            elif entered_url[0] == "1" and self.chs_type == "1":
                self.lbl_rslts.config(text="Please enter a valid URL-Adress.")
            
            #if there are no outliers the program continues
            else:
                #in URL-Mode the given Domain is being transformed into an IP-Adress
                if self.chs_type == "1":
                    gtn_adrs = ipInfo.get_ip(entered_url)

                    #if this check wouldn't exist the standard ipinfo.io-Ip-Adress would be looked up
                    if gtn_adrs == "Null":
                        self.lbl_rslts.config(text="Please enter a valid Adress.")

                #in IP-Mode the given Input is an Ip-Adress already. Thus, it just kopies the entry input 
                elif self.chs_type == "2":

                    gtn_adrs = entered_url
                
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

    #coordinates the URL- and IP-Selcection
    def sel(self):
        self.chs_type = str(var.get())

#Abrufung der Hauptklasse
m = Main(root)

root.mainloop()