import os, time, sys, argparse, tssUtils, fetch, os.path, utils
from os import path

def main():
    parser = argparse.ArgumentParser(description="FutureHelper: FutureRestore SEP, Basband and BuildManifest.plist Downloader by Kasiimh1")
    if sys.platform == "darwin":
        parser.add_argument("-s",help="Set Custom Save Path for Downloaded Files",default=os.path.expanduser("~/Desktop/"))
    if sys.platform == "win32":
        parser.add_argument("-s",  help="Set Custom Save Path for Downloaded Files", default=os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop/" ))
    parser.add_argument("-b", help="Download files for signed Beta iOS versions", action="store_true")
    parser.add_argument("-d", help="Download SEP, Basband and BuildManifest.plist files", action="store_true")
    parser.add_argument("-i", help="Install brew.sh and libimobiledevice deps on macOS", action="store_true")
    args = parser.parse_args()

    if args.i:
        if sys.platform == "darwin":
            try:
                if not path.exists("/usr/local/bin/brew"): 
                    print("Enter password to contiune installation when requested!")
                    os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
                else: 
                    print("brew.sh is already installed skipping....")
                if not path.exists("/usr/local/bin/ideviceinfo"):
                    os.system("brew install libimobiledevice")
                else:
                    print("libimobiledevice is already installed skipping....")
            except:
                print("Error occured when installing brew.sh and libimobiledevice")
        else:
            print("macOS is only supported for deps install!")

    if args.d:
        input("[*] Press ENTER when Device is connected > ")
        time.sleep(1)
        try:
            if sys.platform == "darwin":
                udid = utils.deviceExtractionTool("ideviceinfo", 16, "UniqueDeviceID: ", False)
                ecid = utils.deviceExtractionTool("ideviceinfo", 13, "UniqueChipID: ", True)
                platform = utils.deviceExtractionTool("ideviceinfo", 18, "HardwarePlatform: ", False)
                product = utils.deviceExtractionTool("ideviceinfo", 13, "ProductType: ", False)
                user = utils.deviceExtractionTool("ideviceinfo", 12, "DeviceName: ", False)
                boardid = utils.deviceExtractionTool("ideviceinfo", 15, "HardwareModel: ", False)
            if sys.platform == "win32":
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/win32/")
                udid = utils.deviceExtractionTool("ideviceinfo", 16, "UniqueDeviceID: ", False)
                ecid = utils.deviceExtractionTool("ideviceinfo", 13, "UniqueChipID: ", True)
                platform = utils.deviceExtractionTool("ideviceinfo", 18, "HardwarePlatform: ", False)
                product = utils.deviceExtractionTool("ideviceinfo", 13, "ProductType: ", False)
                user = utils.deviceExtractionTool("ideviceinfo", 12, "DeviceName: ", False)
                boardid = utils.deviceExtractionTool("ideviceinfo", 15, "HardwareModel: ", False)

            print("[*] Fetching Infromation From Device")
            print("-- Device Information --")
            print("[D] Found " + user)
            print("[D] Device is:", product)
            print("[D] BoardID is:", boardid)
            print("[D] Found Device: UDID:", udid)
            print("[D] ECID:", ecid)
            print("[D] Device Platform:", platform)

            for i in tssUtils.signedVersionChecker(product, args.b):
                for index, element in enumerate(tssUtils.ipswGrabber(product, i, args.b)):
                    fetch.downloadFileFromIPSW(element['url'], ["BuildManifest.plist"], args.s + "%s/" %product + "%s/" %i)
                    print("-- Performing BuildManifest Lookup for %s --" %product)
                    utils.checkManifest(args.s + "%s/" %product + "%s/" %i + "BuildManifest.plist", product, boardid.lower(), element['url'], args.s + "%s/" %product + "%s/" %i)
        except:
            print("Something went wrong, Connect Device again and run script again!")
            sys.exit(-1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()