import os, requests, sys
from remotezip import RemoteZip

def downloadFileFromIPSW(URL, filenames, savepath):
    with RemoteZip(URL) as zip:
        try:
            for i in filenames:
                zip.extract(i, savepath)
                print("Downloaded %s successfully" %i)
        except:
            print("File not found!")

def listZip(URL):
    with RemoteZip(URL) as zip:
        try:
            for i in zip.namelist():
                print(i)
        except:
            print("File not found!")

def downloadIPSW(url, path, version, product):
    file = os.path.expanduser(path)
    if os.path.isdir(file) is False:
        try:
            os.mkdir(path)
            print("\nSuccessfully created the directory %s " % path)
        except FileExistsError:
                print("\nCreation of the directory %s failed (might already exist)" % path)
    ipsw = path + "/" + product + "_" + version + ".ipsw"
    if not os.path.isfile(ipsw):
        with open(path + "/" + product + "_" + version + ".ipsw", "wb") as f:
            response = requests.get(url, stream=True)
            total = response.headers.get("content-length")
            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write("\r[{}{}]".format("█" * done, "." * (50 - done)))
                    sys.stdout.flush()
        sys.stdout.write("\n")
    else:
        print("\n[*] IPSW already exists for " + product + " on iOS " + version + " at path: %s" % ipsw)