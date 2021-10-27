import os, plistlib, time, sys, subprocess, argparse, tssUtils, fetch

frozen = "not"
if getattr(sys, "frozen", False):
    frozen = "ever so"
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

def checkManifest(fileLocation, device, boardconfig, version, element, savePath):
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
                    fetch.downloadFileFromIPSW(element, [i['Manifest']['SEP']['Info']['Path']], savePath + "%s/" %device + "%s/" %version + "/" + i['Info']['BuildNumber'])
                    if 'iPhone' in device:
                        print("[Found] Baseband at path:[%s] in BuildManifest" %i['Manifest']['BasebandFirmware']['Info']['Path'])
                        fetch.downloadFileFromIPSW(element, [i['Manifest']['BasebandFirmware']['Info']['Path']], savePath + "%s/" %device + "%s/" %version + "/" + i['Info']['BuildNumber'])
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

def main():
    parser = argparse.ArgumentParser(description="FutureHelper: FutureRestore SEP, Basband and BuildManifest.plist Downloader by Kasiimh1")
    if sys.platform == "darwin":
        parser.add_argument("-s",help="Set Custom Save Path for Downloaded Files",default=os.path.expanduser("~/Desktop/"))
    if sys.platform == "win32":
        parser.add_argument("-s",  help="Set Custom Save Path for Downloaded Files",default=os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop/" ))
    # parser.add_argument("-b", help="Download files for signed Beta iOS versions", action="store_true")
    parser.add_argument("-d", help="Download SEP, Basband and BuildManifest.plist files", action="store_true")
    args = parser.parse_args()

    if args.d:
        input("[*] Press ENTER when Device is connected > ")
        time.sleep(1)
        try:
            if sys.platform == "darwin":
                #os.chdir(bundle_dir + "/darwin/")
                udid = deviceExtractionTool("ideviceinfo", 16, "UniqueDeviceID: ", False)
                ecid = deviceExtractionTool("ideviceinfo", 13, "UniqueChipID: ", True)
                platform = deviceExtractionTool("ideviceinfo", 18, "HardwarePlatform: ", False)
                product = deviceExtractionTool("ideviceinfo", 13, "ProductType: ", False)
                user = deviceExtractionTool("ideviceinfo", 12, "DeviceName: ", False)
                boardid = deviceExtractionTool("ideviceinfo", 15, "HardwareModel: ", False)
            if sys.platform == "win32":
                os.chdir(bundle_dir + "/win32/")
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

            for i in tssUtils.signedVersionChecker(product, args.b):
                for index, element in enumerate(tssUtils.ipswGrabber(product, i, False)):
                    fetch.downloadFileFromIPSW(element['url'], ["BuildManifest.plist"], args.s + "%s/" %product + "/%s/" %i + element['buildid'])
                    print("-- Performing BuildManifest Lookup for %s --" %product)
                    checkManifest(args.s + "%s/" %product + "/%s/" %i + element['buildid'] + "/BuildManifest.plist", product, boardid.lower() , i, element['url'], args.s)
        except:
            print("Something went wrong, Connect Device again and run script again!")
            sys.exit(-1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()