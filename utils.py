import os, plistlib, sys, subprocess, fetch, os.path

def openFolder(savePath):
    print('[*] File should be in:', savePath)
    os.system('open ' + savePath)
    #subprocess.run(['explorer', os.path.realpath(args.path + 'SaveMe-Tickets/' + i['ecid'] + '/' + version + '/' )])

def checkManifest(fileLocation, device, boardconfig, element, savePath):
    fileName = os.path.expanduser(fileLocation)
    if os.path.exists(fileName):
        with open(fileName, 'rb') as f:
            pl = plistlib.load(f)
        if device in pl['SupportedProductTypes']:
            print("[Found] %s in " % device + "BuildManifest")
            for i in pl['BuildIdentities']:
                if boardconfig in i['Info']['DeviceClass']:
                    print("[Found] %s version in BuildManifest" %i['ProductMarketingVersion'])
                    print("[Found] %s boardconfig entry in BuildManifest" %i['Info']['DeviceClass'])
                    print("[Found] SEP at path:[%s] in BuildManifest" %i['Manifest']['SEP']['Info']['Path'])
                    fetch.downloadFileFromIPSW(element, [i['Manifest']['SEP']['Info']['Path']], savePath)
                    if 'iPhone' in device:
                        print("[Found] Baseband at path:[%s] in BuildManifest" %i['Manifest']['BasebandFirmware']['Info']['Path'])
                        fetch.downloadFileFromIPSW(element, [i['Manifest']['BasebandFirmware']['Info']['Path']], savePath)
                    else:
                        print("[Warning] %s does not use Baseband for restores!" %device)
                    return
            else:
                print("[Error] BoardConfig: [%s] does not match entry in BuildManifest, check again!"%boardconfig)
        else:
            print("[Error] Counldn't match %s to entry in BuildManifest" %device)
    else:
        print('[Error] %s does not exist, so can\'t be read' % fileName)
    return

def deviceExtractionTool(binaryName, stripValue, grepValue, replace):
    if sys.platform == "darwin":
        command = binaryName + " | grep " + grepValue
    if sys.platform == "win32":
        command = binaryName + " | findstr " + grepValue
    command = binaryName + " | grep " + grepValue
    process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf8")
    output = process.communicate()
    stdOutput, stdErrValue = output
    stdOutput = stdOutput.strip()
    stdOutput = stdOutput[stripValue:]
    if replace == True:
        stdOutput = stdOutput.replace(" ", "")
    return dataReturn(stdOutput, stdErrValue)

def dataReturn(output, error):
    ret = None
    if error != None:
        ret = error
    if output != None:
        ret = output
    return ret