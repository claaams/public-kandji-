import json
import requests

### https://api.kandji.io/#f8cd9733-89b6-40f0-a7ca-76829c6974df

url = "https://yourtenant.clients.us-1.kandji.io/api/"
device_url = "v1/devices/"
device_apps_url = "v1/devices/"
bearer = ''


payload = {}
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {bearer}'
}

# Get the name of the app to find

def GetAppTarget():
    appname = input("What is the name of the app you are looking for? \n")
    lowerappname = appname.lower()
    return str(lowerappname)

target_app = GetAppTarget()

# Get all devices listed

def GetDevices():
    response = requests.request("GET",  url + device_url , headers=headers)
    #print(response.json())
    return response.json()

deviceList = GetDevices()

# create a list of all device IDs and their hostnames in a dictionary

device_dict = {}

def MakeDict():
    for i in range(len(deviceList)):
        device_dict[deviceList[i]['device_id']] = deviceList[i]['device_name']


MakeDict()

# print device list to audit that its working
# print(device_dict)

# iterate through the list of device ID's and get all listed apps
# search the listed apps for mozilla vpn.app if true return hostname, if false, continue

def GetApps():
    appInstalled = []
    nothing = "No devices with the app found. Please run a manual check on a known device to make sure the app name is spelled correctly"
    for id in device_dict:
        response = requests.request("GET", url + device_apps_url + id + '/apps', headers=headers)
        applist = response.json()
        #print(applist['apps'])
        for things in range(len(applist['apps'])):
            if applist['apps'][things -1]['app_name'].lower() == target_app:
                #print(id)
                appInstalled.append(id)
    if appInstalled == False:
        return nothing
    else:
        return appInstalled

#Get hostnames of devices from appInstalled list
hostlist = GetApps()

def GetHostnames(hostlist):
    hostnames = []
    for host in hostlist:
        hostnames.append(device_dict[host])
    return hostnames

victory = GetHostnames(hostlist)

print(victory)
