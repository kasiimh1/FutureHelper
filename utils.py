import os, csv

def createSavePath(ecid, savePath, version):
    if not os.path.isdir(os.path.expanduser(savePath + '/SaveMe-Tickets/' + ecid + '/')):
        try:
            os.mkdir(os.path.expanduser(savePath + '/SaveMe-Tickets/' + ecid + '/'))
        except FileExistsError:
            print('[*] Skipping creating ECID folder as %s it already exists' %ecid)
    if not os.path.isdir(os.path.expanduser(savePath + '/SaveMe-Tickets/' + ecid + '/') + version):
        try:
            os.mkdir(os.path.expanduser(savePath + '/SaveMe-Tickets/' + ecid + '/' + version))
        except FileExistsError:
            print('[*] Skipping creating iOS version folder as %s it already exists' %ecid)

def openFolder(savePath):
    print('[*] File should be in:', savePath)
    os.system('open ' + savePath)
    #subprocess.run(['explorer', os.path.realpath(args.path + 'SaveMe-Tickets/' + i['ecid'] + '/' + version + '/' )])

def writeDevicesToOutput(data, path):
    f = open(path + "/SaveMe-Devices", "a")
    f.write(data)
    f.close()

def printCachedDevices(savePath):
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
        print("------------------------------------------------------------------------")