import requests, subprocess, os, csv, utils

def signedVersionChecker(model, isBeta):
    URL = None
    ipsw = []

    if isBeta:
        URL = "https://api.m1sta.xyz/betas/" + model
        print("\n[TSS] Using:", URL)
    if not isBeta:
        URL = "https://api.ipsw.me/v4/device/" + model + "?type=ipsw"
        print("\n[TSS] Using:", URL)

    req = requests.get(URL)
    print("-- Checking Currently Signed iOS Versions --")
    print("[API] Response Code: [" + str(req.status_code) + "]")
    if req.status_code == 200:
        req = req.json()
        print("-- Server Response --")
        if isBeta:
            for i in range(len(req)):
                if req[i]['signed'] == True:
                    print("[TSS BETA Signed] iOS:", req[i]['version'], "build:", req[i]['buildid'], "is currently being Signed for the", model)
                    ipsw.append(req[i]['buildid'])
        else:
            for i in range(len(req["firmwares"])):
                if req["firmwares"][i]["signed"] == True:
                    print("[TSS Signed] iOS:", req["firmwares"][i]["version"], "build:", req["firmwares"][i]['buildid'], "is currently being Signed for the", model)
                    ipsw.append(req["firmwares"][i]["buildid"])
    return ipsw
     
def ipswGrabber(model, version, isBeta):
    URL = None
    ipsw = []

    if isBeta:
        URL = "https://api.m1sta.xyz/betas/" + model
        print("\n[TSS BETA] Using:", URL)
    else:
        URL = "https://api.ipsw.me/v4/device/" + model + "?type=ipsw"
        print("\n[TSS] Using:", URL)

    req = requests.get(URL)
    print("-- Fetching IPSW --")
    print("[API] Response Code: [" + str(req.status_code) + "]")
    if req.status_code == 200:
        req = req.json()
        print("-- Server Response --")
        if isBeta:
            try:
                for i in range(len(req)):
                    if req[i]['buildid'] == version:
                        ipsw.append({ "version": version, "buildid": req[i]['buildid'], "url": req[i]['url']})
                        print("[TSS BETA Download] %s iOS:" %model, req[i]['version'], "buildid:", req[i]['buildid'], "URL:", req[i]['url'])
            except:
                return("No IPSW found for: %s" %model + " on: %s" %version)
        if not isBeta:
            try:
                for i in range(len(req["firmwares"])):
                    if req["firmwares"][i]["buildid"] == version:
                        ipsw.append({ "version": version, "buildid": req["firmwares"][i]['buildid'], "url": req['firmwares'][i]['url']})
                        print("[TSS Download] %s iOS:" %model, req["firmwares"][i]["version"], "buildid:", req["firmwares"][i]['buildid'], "URL:", req['firmwares'][i]['url'])
            except:
                return("No IPSW found for: %s" %model + " on: %s" %version)
    return ipsw