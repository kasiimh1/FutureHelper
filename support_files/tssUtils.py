import requests, subprocess, os, csv
from support_files import tssUtils, utils

def signedVersionChecker(model, isBeta):
    URL = None
    ipsw = []

    if isBeta == True:
        URL = "https://api.m1sta.xyz/betas/" + model
        print("\n[TSS] Using:", URL)
    else:
        URL = "https://api.ipsw.me/v4/device/" + model + "?type=ipsw"
        print("\n[TSS] Using:", URL)

    req = requests.get(URL)
    print("-- Checking Currently Signed iOS Versions --")
    print("[API] Response Code: [" + str(req.status_code) + "]")
    if req.status_code == 200:
        req = req.json()
        print("-- Server Response --")
        if isBeta == True:
            for i in range(len(req)):
                if req[i]['signed'] == True:
                    print("[TSS] iOS:", req[i]['version'], "build:", req[i]['buildid'], "is currently being Signed for the", model)
                    ipsw.append(req[i]['version'])
        else:
            for i in range(len(req["firmwares"])):
                if req["firmwares"][i]["signed"] == True:
                    print("[TSS] iOS:", req["firmwares"][i]["version"], "build:", req["firmwares"][i]['buildid'], "is currently being Signed for the", model)
                    ipsw.append(req["firmwares"][i]["version"])
        return ipsw
        
def ipswGrabber(model, version, isBeta):
    URL = None
    ret = None
    ipsw = []

    if isBeta == True:
        URL = "https://api.m1sta.xyz/betas/" + model
        print("\n[TSS] Using:", URL)
    else:
        URL = "https://api.ipsw.me/v4/device/" + model + "?type=ipsw"
        print("\n[TSS] Using:", URL)

    req = requests.get(URL)
    print("-- Fetching IPSW --")
    print("[API] Response Code: [" + str(req.status_code) + "]")
    if req.status_code == 200:
        req = req.json()
        print("-- Server Response --")
        if isBeta == True:
            try:
                for i in range(len(req)):
                    if req[i]['version'] == version:
                        ipsw.append({ "version": version, "buildid": req[i]['buildid'], "url": req[i]['url']})
                        print("[TSS] %s iOS:" %model, req[i]['version'], "buildid:", req[i]['buildid'], "URL:", req[i]['url'])
                        return ipsw
            except:
                ret = "No IPSW found for: %s" %model + " on: %s" %version
        if isBeta != True:
            try:
                for i in range(len(req["firmwares"])):
                    if req["firmwares"][i]["version"] == version:
                        ipsw.append({ "version": version, "buildid": req["firmwares"][i]['buildid'], "url": req['firmwares'][i]['url']})
                        print("[TSS] %s iOS:" %model, req["firmwares"][i]["version"], "buildid:", req["firmwares"][i]['buildid'], "URL:", req['firmwares'][i]['url'])
                        return ipsw
            except:
                print("No IPSW found for: %s" %model + " on: %s" %version)
    return ret

def requestDeviceTicket(d_id, d_ecid, d_boardid, d_ios, d_apnonce, d_save, d_ota):
    process = subprocess.Popen('tsschecker.exe --nocache -d %s' %d_id + ' -e %s' %d_ecid + ' --boardconfig %s' %d_boardid + ' --ios %s' %d_ios + ' --apnonce %s' %d_apnonce + ' -s --save-path %s' %d_save + ' %s' %d_ota, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    return process.communicate()
    
    # output = process.communicate()
    # stdOutput, stdErrValue = output
    # stdOutput = stdOutput.strip()
    # print(stdErrValue)
    # print(stdOutput)

def saveTicketsForCachedDevices(version, savePath):
    file = os.path.expanduser(savePath + '/SaveMe-Tickets/SaveMe-Devices')
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for i in csv_reader:
            print("------------------------------------------------------------------------")
            print("-- Found Device --")
            print("[D] Name: " + i['name'])
            print("[D] Model: " + i['model'])
            print("[D] UDID: " + i['udid'])
            print("[D] ECID: " + i['ecid'])
            print("[D] BoardID: " + i['boardid'])
            print("[D] Platform: " + i['platform'])
            print("[D] Generator: " + i['generator'])
            print("[D] APNonce: " + i['apnonce'])
            print("-- Saving Ticket For Cached Device -- ")
            utils.createSavePath(i['ecid'], savePath, version)  
            if i['boardid'].find("J105AAP") == 0 or i['boardid'].find("J42DAP") == 0 or i['boardid'].find("K66AP") == 0 or i['boardid'].find("J33IAP") == 0 or i['boardid'].find("J33AP") == 0:
                print("[*] REQUESTING tvOS OTA TICKETS")
                ota = ' -o'
                requestDeviceTicket(i['model'], i['ecid'], i['boardid'], version, i['apnonce'],  savePath + 'SaveMe-Tickets/' + i['ecid'] + '/' + version + '/', ota)
            else:
                print("[*] REQUESTING REGULAR TICKETS")
                ota = ''
                requestDeviceTicket(i['model'], i['ecid'], i['boardid'], version, i['apnonce'],  savePath + 'SaveMe-Tickets/' + i['ecid'] + '/' + version + '/', ota)
        print("------------------------------------------------------------------------")
    