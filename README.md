# tudify SimpleWeb 3.0.2
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
You will need ``` Python 3.11 or later ```, ```Command Prompt``` and an ```administrator account```
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

``` pyinstaller --noconsole --onefile --add-data "extensions.json:." simpleweb.py ```

on Windows 

``` pyinstaller --noconsole --onefile --add-data "extensions.json;." simpleweb.py ```

you have now built simpleweb, look inside the folder simpleweb.py is, and look for a new folder called 'Dist'

your new binary is there.

# API documentation
**the SimpleWeb API allows for extra communication between the SimpleWeb browser and the website its running on.**
## examples and info
## Getting Started

### 1. Include the Qt WebChannel script
Place the following inside your <head>:`` <script src="qrc:///qtwebchannel/qwebchannel.js"></script> ``

### 2. Initialize the API

Place the following in your <script> tag:
```
document.addEventListener("DOMContentLoaded", function() {
    if (typeof qt === "undefined") return;

    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.SimpleWeb = channel.objects.SimpleWeb;
        // Your code using the API goes here
    });    
});
```

### Available functions

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getDeviceInfo()` | None | String | Returns CPU, architecture, and OS info. Example: `"Intel i5, x64, Windows"` |
| `reportAPIver()` | None | String | Returns the API version, e.g., `"1.0.1"` |
| `getRamAmount()` | None | String | Returns system RAM amount, e.g., `"16 GB"` |
| `getUserAgent()` | None | String | Returns the browser User-Agent string |
| `getOS()` | None | String | Returns the OS name (`Windows`, `Linux`, `macOS`) |
| `GetUserTheme()` | None | String | Returns the current user theme: `"dark"` or `"light"` |
| `openwindow(url, width, height)` | `url` (string), `width` (int, default 800), `height` (int, default 600) | None | Opens a new SimpleWeb window with the specified URL and dimensions |
| `setWindowTitle(title)` | `title` (string) | None | Changes the title of the main browser window (or the last opened window if no main window) |
| `print(text)` | `text` (string) | None | Prints a message to the Python console |

### Example Usage
**Getting device information**
```
SimpleWeb.getDeviceInfo().then(info => {
    SimpleWeb.print("Device info:", info);
});
```
**Opening a new window**
```
SimpleWeb.openwindow("https://tudify.co.uk", 1024, 768);
SimpleWeb.setWindowTitle("My Cool App");
```
**Detecting the user's theme**
```
SimpleWeb.GetUserTheme().then(theme => {
    if (theme === "dark") {
        document.body.style.backgroundColor = "#202326";
    } else {
        document.body.style.backgroundColor = "#ffffff";
    }
});
```
## extra notes:
- The API only works in SimpleWeb. Standard browsers will ignore it.
-	Some features may require user interaction (e.g., openwindow).
-	Future releases may expand API capabilities with extra extensions and AI integrations.
  
## thank you for choosing SimpleWeb.
