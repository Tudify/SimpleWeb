<img width="50" height="50" alt="simpleweb logo" src="https://github.com/user-attachments/assets/c88ec103-c9cc-4663-89b0-6e8908121889"/> 

# SimpleWeb 3.0 

### an all-new reimagination of SimpleWeb, with all-new controls, incredible stability & efficiency improvements and reimagined UI.
<img width="1822" height="1118" alt="Screenshot 2025-11-11 at 18 21 17" src="https://github.com/user-attachments/assets/6b711711-b7de-46a6-92a8-6f553107edd6" />

### note: macOS builds will appear to crash on start. give it ~15 seconds and it will open.

## controls
### Smart Bar
⌘ + U / ctrl + U
### New tab
⌘ + T / ctrl + T
### Close Tab
⌘ + W / ctrl + W
### Refresh page
⌘ + R / ctrl + R
### Settings page
⌘ + U / ctrl + U, then type tudify://settings.
### Extensions page
⌘ + U / ctrl + U, then type extensions://
## Note 2: some features may be broken, buggy or messy. 

# Note on Windows:
<b> SimpleWeb team does not offer prebuilt Windows Binaries. </b>
You can build SimpleWeb from source with no issue, as it is officially supported.
## Build Instructions
You will need ``` Python 3.11 or later ```, ``` gcc or clang ```, ```Command Prompt``` and an ```administrator account```
### Step One:
#### Install dependencies
run the following command:

On Windows:
``` pip install pyqt5 pyqtwebengine psutil pyinstaller ```

On Linux or macOS:
``` pip3 install pyqt5 pyqtwebengine psutil pyinstaller ```

### Step two:
#### Create binary

locate your folder path that simpleweb.py and extensions.json are in, then cd to it like this

``` cd /users/you/folder/ ``` 

<small> this is not an actual command for your system, you need to find your folder path to replace /users/you/folder </small>

when you are in your folder in your command prompt, type the following

on Linux and macOS:

```
g++ -std=c++17 -o simpleweblib startupinfo.cpp
pyinstaller --onefile --add-data "extensions.json:." --add-data "info.json:." --add-binary "simpleweblib:." SimpleWeb.py
```

on Windows 

```
g++ -std=c++17 -o simpleweblib startupinfo.cpp
pyinstaller --onefile --add-data "extensions.json;." --add-data "info.json;." --add-binary "simpleweblib;." SimpleWeb.py
```

you have now built simpleweb, look inside the folder simpleweb.py is, and look for a new folder called 'Dist'

your new binary is there.

## API Documentation
[View API Documentation](API.md)

## thank you for choosing SimpleWeb.
