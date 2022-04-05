from distutils.command.config import config
from sqlite3 import Cursor
import requests
import socket

#used for getting informations about the input IP-Adress
def get_location(ip_address):
    #requests a data collection from ipinfo.io about the IP-Adress
    response = requests.get(f'https://ipinfo.io/{ip_address}').json()
    
    #important values for location are being stored and send back to sender
    location_data = {
        "ip": response.get("ip"),
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country")
    }
    return location_data

#used for transforming Domains into Ip-Adresses
def get_ip(domain):
    #
    try:
        result = socket.gethostbyname(domain)
        print("Domain name : ",domain)
        print("Ip : ",result)
    except:
        result = "Null"
    return result