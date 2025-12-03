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

| Method | Parameters | Returns | Description | Added in API ver |
|--------|------------|---------|-------------|------------------|
| `getDeviceInfo()` | None | String | Returns CPU, architecture, and OS info. Example: `"Intel i5, x64, Windows"` | 1.0 |
| `macVersion()` | None | String | Returns `null` if not a mac, or eg. `26_2` for Tahoe 26.2 | 1.0.3 |
| `reportAPIver()` | None | String | Returns the API version, e.g., `"1.0.1"` | 1.0 |
| `getRamAmount()` | None | String | Returns system RAM amount, e.g., `"16 GB"` | 1.0.1 |
| `getUserAgent()` | None | String | Returns the browser User-Agent string | 1.0 |
| `getOS()` | None | String | Returns the OS name (`Windows`, `Linux`, `macOS`) | 1.0 |
| `getUserTheme()` | None | String | Returns the current user theme: `"dark"` or `"light"` | 1.0 for GetUserTheme, or 1.0.2 for getUserTheme |
| `getSearchEngine()` | None | String | Returns the current user Search Engine: `"Google"`, `Bing` or `"DuckDuckGo"` | 1.0.2 |
| `openwindow(url, width, height)` | `url` (string), `width` (int, default 800), `height` (int, default 600) | None | Opens a new SimpleWeb window with the specified URL and dimensions | 1.0 |
| `setWindowTitle(title)` | `title` (string) | None | Changes the title of the main browser window (or the last opened window if no main window) | 1.0 |
| `print(text)` | `text` (string) | None | Prints a message to the Python console | 1.0 |

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
  
