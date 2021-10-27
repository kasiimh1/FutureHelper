import os, plistlib, time, sys, subprocess
from support_files import tssUtils, fetch

savePath = desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop/") 

def checkManifest(fileLocation, device, boardconfig, version):
    fileName = os.path.expanduser(fileLocation)
    if os.path.exists(fileName):
        with open(fileName, 'rb') as f:
            pl = plistlib.load(f)
        if device in pl['SupportedProductTypes']:
            print("[Found] %s in " % device + "BuildManifest")
            for i in pl['BuildIdentities']:
                if boardconfig in i['Info']['DeviceClass']: # and version in i['ProductMarketingVersion'] 
                    print("[Found] %s version in BuildManifest" %i['ProductMarketingVersion'])
                    print("[Found] %s boardconfig entry in BuildManifest" %i['Info']['DeviceClass'])
                    print("[Found] SEP at path:[%s] in BuildManifest" %i['Manifest']['SEP']['Info']['Path'])
                    if 'iPhone' in device:
                        print("[Found] Baseband at path:[%s] in BuildManifest" %i['Manifest']['BasebandFirmware']['Info']['Path'])
                    else:
                        print("[Error] %s does not use Baseband for restores!" %device)
                    return
            else:
                print("[Error] BoardConfig: [%s] does not match entry in BuildManifest, check again!"%boardconfig)
        else:
            print("[Error] Counldn't match %s to entry in BuildManifest" %device)
    else:
        print('[Error] %s does not exist, so can\'t be read' % fileName)

    return

def deviceExtractionTool(binaryName, stripValue, grepValue, replace):
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

def main():

    input("[*] Press ENTER when Device is connected > ")
    time.sleep(1)
    try:
        udid = deviceExtractionTool("ideviceinfo", 16, "UniqueDeviceID: ", False)
        ecid = deviceExtractionTool("ideviceinfo", 13, "UniqueChipID: ", True)
        platform = deviceExtractionTool("ideviceinfo", 18, "HardwarePlatform: ", False)
        product = deviceExtractionTool("ideviceinfo", 13, "ProductType: ", False)
        user = deviceExtractionTool("ideviceinfo", 12, "DeviceName: ", False)
        boardid = deviceExtractionTool("ideviceinfo", 15, "HardwareModel: ", False)

        print("[*] Fetching Infromation From Device")
        print("-- Device Information --")
        print("[D] Found " + user)
        print("[D] Device is:", product)
        print("[D] BoardID is:", boardid)
        print("[D] Found Device: UDID:", udid)
        print("[D] ECID:", ecid)
        print("[D] Device Platform:", platform)

        for i in tssUtils.signedVersionChecker(product, False):
            for index, element in enumerate(tssUtils.ipswGrabber(product, i, False)):
                dl = fetch.downloadFileFromIPSW(element['url'], ["BuildManifest.plist"], savePath + "%s/" %product + "/%s/" %i)
                print("-- Performing BuildManifest Lookup for %s --" %product)
                checkManifest(savePath + "%s/" %product + "/%s/" %i + "BuildManifest.plist", product, boardid.lower() , i)
    except:
        print("Unabled to query device info, Connect Device again and run script again!")
        sys.exit(-1)

if __name__ == '__main__':
    main()