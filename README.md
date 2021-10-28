# FutureHelper 

### Supports macOS and Windows

Downloads SEP, Baseband and BuildManifest automatically for signed iOS version's (including beta firmwares) for connected iDevice

```
FutureHelper: FutureRestore SEP, Basband and BuildManifest.plist Downloader by Kasiimh1
optional arguments:
  -h, --help  show this help message and exit
  -s S        Set Custom Save Path for Downloaded Files
  -b          Download files for signed Beta iOS versions
  -d          Download SEP, Baseband and BuildManifest.plist files
  -i          Install brew.sh and libimobiledevice deps on macOS
```

### Uses ideviceinfo from: https://github.com/libimobiledevice/libimobiledevice

### Downloads files to folder named after iPhone, iPad or iPod model e.g. (iPad7,3, iPhone11,2)

The tool performs BuildManifest lookup for the matching SEP firmware and Baseband that is specific for the connected device!

### all users need to run 

- ``` pip install -r requirements.txt ```

### macOS users need to install brew and libimobiledevice 

#### Automatically:

- ``` python3 main.py -i ```

#### Manually install brew.sh:

- ``` /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" ```

#### Manually install libimobiledevice:

- ``` brew install libimobiledevice ```

#### RestoreMe will be incorporated into this soon, allowing automatically downloading of files and automating futurerestore, device updates and restores outside of signing windows (if baseband and SEP are compatible)

### Troubleshoot

- Make sure device is connected and trusted both on the device and via iTunes or Finder

- Does not currently support linux
