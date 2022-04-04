from turtle import textinput
import requests
import socket

def getLocation(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}').json()
    location_data = {
        "ip": response.get("ip"),
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country")
    }
    return location_data

def getIp(domain):
    try:
        result = socket.gethostbyname(domain)
        print("Domain name : ",domain)
        print("Ip : ",result)
    except:
        result = "Null"
    return result