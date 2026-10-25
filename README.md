This is a clicker game inspired by cookie clicker,
Just click, upgrade and click!

# Download

**Linux, Android (Termux)**

Download the latest file from Releases named "main-os-architecture", 
Navigate to the directory you downloaded the file and 
run this
```bash
chmod +x main-os-architecture
./main-os-architecture
```

**Windows, MacOS, android x86_64 and all 32 bit machines**


## Windows, MacOS
Because neither i have a Windows nor a MacOS only android, i couldn't make it for Windows or MacOS, but you still can use it like this assuming you have python3 and git installed

Note: These are not tested so please don't ask me if it fails

**Windows, MacOS**

```bash
git clone https://github.com/Arnav-unix/Mewo-clicker.git
cd Mewo-clicker
python3 main.py
```

If you want a .exe or a MacOS executable file do this

```bash
# Installing pyinstaller
pip3 install pyinstaller

# Assuming you have cloned the repo and are inside it
python3 -m PyInstaller \
  --noconfirm --clean --onedir \
  --noconsole \
  --add-data "Assets:Assets" \
  main.py
```

Now to run it
**Windows**
```bash
.\dist\main\main.exe
```

**MacOS**
```bash
#first run this
chmod +x dist/main/main

# then this
./dist/main/main
```
