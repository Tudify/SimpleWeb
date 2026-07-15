<img width="50" height="50" alt="simpleweb logo" src="https://github.com/user-attachments/assets/c88ec103-c9cc-4663-89b0-6e8908121889"/> 

# SimpleWeb NIGHTLY

### this version of simpleweb is in beta or sometimes alpha. expect lots of bugs, broken features and more.

## Build Instructions
You will need ``` Python 3.11 or later ```, ``` gcc or clang ```, ```Command Prompt``` and an ```administrator account```
### Step One:
#### Install dependencies
run the following command:

On Windows:
``` pip install pyqt6 pyqtwebengine psutil pyinstaller ```

On Linux or macOS:
``` pip3 install pyqt6 pyqtwebengine psutil pyinstaller ```

### Step two:
#### Create binary

locate your folder path that simpleweb.py and extensions.json are in, then cd to it like this

``` cd /users/you/folder/ ``` 

<small> this is not an actual command for your system, you need to find your folder path to replace /users/you/folder </small>

when you are in your folder in your command prompt, type the following

on Linux and macOS:

```
g++ -std=c++17 -o simpleweblib startupinfo.cpp
g++ -std=c++17 -o infoloaderbin infoloader.cpp
pyinstaller --onefile --windowed --add-data "extensions.json:." --add-data "info.json:." --add-binary "simpleweblib:." --add-binary "infoloaderbin:." SimpleWeb.py
```

on Windows 

```
g++ -std=c++17 -o simpleweblib startupinfo.cpp
g++ -std=c++17 -o infoloaderbin infoloader.cpp
pyinstaller --onefile --windowed --add-data "extensions.json;." --add-data "info.json;." --add-binary "simpleweblib;." SimpleWeb.py
```

## API Documentation
[View API Documentation](API.md)

## thank you for choosing SimpleWeb.
