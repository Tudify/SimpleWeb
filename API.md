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

**Printing a Debug string**
```
SimpleWeb.print("hello world")
```

**Getting system RAM amount**
```
SimpleWeb.getRamAmount()
```
output:
```
16.0 GB
```

**Fetching API ver**
```
SimpleWeb.reportAPIver()
```
this line is insannely useful for making sure your code works with the users version of SimpleWeb.

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
- Arvitrary code will not run.
-	Some features may require user interaction (e.g., openwindow).
-	Future releases may expand API capabilities with extra extensions and AI integrations.
  
