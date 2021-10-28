# FutureHelper 

### Supports macOS and Windows

Downloads SEP, Baseband and BuildManifest automatically for signed iOS version's

```
FutureHelper: FutureRestore SEP, Basband and BuildManifest.plist Downloader by Kasiimh1
optional arguments:
  -h, --help  show this help message and exit
  -s S        Set Custom Save Path for Downloaded Files
  -b          Download files for signed Beta iOS versions
  -d          Download SEP, Basband and BuildManifest.plist files
  -p          Install brew.sh and libimobiledevice deps on macOS
```

### Uses ideviceinfo from: https://github.com/libimobiledevice/libimobiledevice

### Downloads files to folder named after iPhone, iPad or iPod model e.g. (iPad7,3, iPhone11,2)

### all users need to run 

- ``` pip install -r requirements.txt ```

### macOS users need to install brew and libimobiledevice 

#### Install brew:

- ``` /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" ```

#### Install libimobiledevice:

- ``` brew install libimobiledvice ```

#### RestoreMe will be incorporated into this soon, allowing automatically downloading of files and automating futurerestore, device updates and restores outside of signing windows (if baseband and SEP are compatiable)

### Troubleshoot

- Make sure device is connected and trusted both on the device and via iTunes or Finder

- Does not currently support linux
