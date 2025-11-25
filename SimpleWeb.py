import sys, os, platform, urllib.parse, json, psutil, subprocess, updater, inspect, simplewebex
import PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QWidget, QMessageBox,QVBoxLayout, QLineEdit, QTabWidget, QFileDialog,  QDialog, QLabel,  QDialogButtonBox, QComboBox, QCheckBox, QColorDialog, QPushButton)
from PyQt6.QtCore import QUrl, Qt, QSettings, QEvent, QObject, pyqtSlot, QEventLoop
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt6.QtWebChannel import QWebChannel
from pathlib import Path
from simplewebex import SimpleWeb

script_dir = os.path.dirname(os.path.abspath(__file__))
exe_path = os.path.join(script_dir, "simpleweblib")
result = subprocess.run([exe_path], capture_output=True, text=True)
print(result.stdout)

class getwebpage(QWebEnginePage):
    """Load a URL and return the rendered HTML source code."""
    def __init__(self):
        # Only create one QApplication instance globally
        self.app = QApplication.instance() or QApplication(sys.argv)
        super().__init__()

        self.html = None
        self.loadFinished.connect(self._on_load_finished)

    def fetch(self, url: str) -> str:
        self.html = None
        self._loop = QEventLoop()

        self.load(QUrl(url))
        print("Loading URL:", url)
        self._loop.exec_()  # Wait until load finishes

        return self.html

    def _on_load_finished(self, ok: bool):
        if not ok:
            self.html = ""
            self._loop.quit()
            return

        # Retrieve the rendered HTML
        self.toHtml(self._store_html)

    def _store_html(self, html: str):
        self.html = html
        self._loop.quit()

class ExtensionsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Extensions - SimpleWeb")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QLabel#heading {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 7px;
            }
            *{font-family: hack, consolas, monospace;}
            """)
        layout = QVBoxLayout()
        self.heading_label = QLabel("Extensions")
        self.heading_label.setObjectName("heading")
        layout.addWidget(self.heading_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.new_current_label = QLabel("Currently Available:")
        layout.addWidget(self.new_current_label)
        self.extension_checkboxes = {}
        self.load_extensions(layout)
        layout.addSpacing(20)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)


    def load_extensions(self, layout):
        # Path to file in same directory as this script
        base_dir = Path(__file__).resolve().parent
        extensions_file = base_dir / "extensions.json"
        if extensions_file.exists():
            try:
                with extensions_file.open("r", encoding="utf-8") as f:
                    extensions = json.load(f)
            except Exception as e:
                print(f"Failed to read {extensions_file.name}: {e}")
                extensions = {
                    "Error": True,
                }
        else:
            print("error")
        extop = QSettings("Tudify", "SimpleWeb-Extensions")

        for name, default_state in extensions.items():
            state = extop.value(name, default_state, type=bool)
            checkbox = QCheckBox(name)
            checkbox.setChecked(state)
            layout.addWidget(checkbox)
            self.extension_checkboxes[name] = checkbox

    def save_settings(self):
        extop = QSettings("Tudify", "SimpleWeb-Extensions")
        for name, checkbox in self.extension_checkboxes.items():
            extop.setValue(name, checkbox.isChecked())
        # If parent exists and has an apply_chromium_spoofer method, call it so the UA is applied immediately
        if self.parent() is not None and hasattr(self.parent(), "apply_chromium_spoofer"):
            try:
                self.parent().apply_chromium_spoofer()
            except Exception as e:
                print("Failed to apply chromium spoofer from ExtensionsWindow:", e)
        self.accept()

class SimpleWebAPI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.windows = []
        self.main_window = parent  # main browser window reference

    @pyqtSlot(str, int, int)
    def openwindow(self, url, width=800, height=600):
        window = QMainWindow()
        window.setWindowTitle("SimpleWeb Window")
        window.setGeometry(100, 100, width, height)  
        # Web view setup
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        layout.addWidget(browser)
        window.setCentralWidget(central_widget)

        window.show()
        self.windows.append(window)

    @pyqtSlot(result=str)
    def getDeviceInfo(self):
        return f"{cpuname}, {arch[0]}, {os_namereport}"

    @pyqtSlot(result=str)
    def reportAPIver(self):
        return APIver
    
    @pyqtSlot(result=str)
    def getSearchEngine(self):
        settings = QSettings("Tudify", "SimpleWeb")
        return settings.value("search_engine", "Google")

    @pyqtSlot(result=str)
    def getRamAmount(self):
        return str(mem) + " GB"

    @pyqtSlot(result=str)
    def getUserAgent(self):
        return UserAgent

    @pyqtSlot(result=str)
    def getOS(self):
        return os_name

    @pyqtSlot(result=str)
    def getUserTheme(self):
        settings = QSettings("Tudify", "SimpleWeb")
        theme = settings.value("theme", "dark")
        return theme

    @pyqtSlot(result=str)
    def GetUserTheme(self):
        print("GetUserTheme is planned to be deprecated. Please migrate to getUserTheme when possible.")
        return self.getUserTheme()
    
    @pyqtSlot(str)
    def print(self, text):
        print(text)

    @pyqtSlot(str)
    def setWindowTitle(self, title):
        """Sets title for the main browser window (if linked)."""
        if self.main_window:
            self.main_window.setWindowTitle(title)
        else:
            # fallback: rename the last opened standalone window
            if self.windows:
                self.windows[-1].setWindowTitle(title)

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QLabel#heading {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 7px;
            }
            *{font-family: hack, consolas, arial;}
            """)
        
        layout = QVBoxLayout()
        self.heading_label = QLabel("Settings")
        self.heading_label.setObjectName("heading")
        layout.addWidget(self.heading_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.new_tab_url_label = QLabel("New Tab URL:")
        layout.addWidget(self.new_tab_url_label)
        self.new_tab_url_edit = QLineEdit()
        layout.addWidget(self.new_tab_url_edit)
        self.default_new_tab_checkbox = QCheckBox("Open new tabs with default URL")
        layout.addWidget(self.default_new_tab_checkbox)
        self.theme_label = QLabel("Choose your theme:")
        layout.addWidget(self.theme_label)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        layout.addWidget(self.theme_combo)
        self.selabel = QLabel("Choose your search engine:")
        layout.addWidget(self.selabel)
        self.search_engine_combo = QComboBox()
        self.search_engine_combo.addItems(["Google", "DuckDuckGo", "Bing"])
        layout.addWidget(self.search_engine_combo)
        self.ailabel = QLabel("Choose your AI service:")
        layout.addWidget(self.ailabel)
        self.AI_combo = QComboBox()
        self.AI_combo.addItems(["Nora AI", "Claude", "Amanda AI 2", "ChatGPT", "Gemini"])
        layout.addWidget(self.AI_combo)
        self.musictitle = QLabel("Choose your Music service:")
        layout.addWidget(self.musictitle)
        self.music_combo = QComboBox()
        self.music_combo.addItems(["Spotify", "Apple Music", "Amazon Music", "YouTube Music", "Tidal"])
        layout.addWidget(self.music_combo)
        self.accent_label = QLabel("Accent Colour (Hex):")
        layout.addWidget(self.accent_label)
        accent_layout = QHBoxLayout()
        self.accent_edit = QLineEdit()
        self.accent_edit.setPlaceholderText("#0a6cff")
        self.accent_btn = QPushButton("Pick Colour")
        self.accent_btn.clicked.connect(self.pick_accent_colour)
        accent_layout.addWidget(self.accent_edit)
        accent_layout.addWidget(self.accent_btn)
        layout.addLayout(accent_layout)
        self.accent_note = QLabel("NOTE: \n Accent Colour and Music Service change \n will require restart to apply.")
        layout.addWidget(self.accent_note)
        self.load_settings()
        layout.addSpacing(20)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                      QDialogButtonBox.StandardButton.Cancel | 
                                      QDialogButtonBox.StandardButton.Reset)
        button_box.accepted.connect(self.save_settings)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        reset_button = button_box.button(QDialogButtonBox.StandardButton.Reset)
        reset_button.clicked.connect(self.reset_settings)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def pick_accent_colour(self):
        colour = QColorDialog.getColor()
        if colour.isValid():
            self.accent_edit.setText(colour.name())

    def load_settings(self):
        settings = QSettings("Tudify", "SimpleWeb")
        self.new_tab_url_edit.setText(settings.value("new_tab_url", "https://tudify.co.uk/simpleweb/newtab.htm"))
        self.theme_combo.setCurrentText(settings.value("theme", "Dark"))
        self.search_engine_combo.setCurrentText(settings.value("search_engine", "Google"))
        self.AI_combo.setCurrentText(settings.value("AI_service", "Nora AI"))
        self.AI_combo.setCurrentText(settings.value("music_service", "Spotify"))
        default_new_tab_checked = settings.value("default_new_tab_checked", False)
        self.default_new_tab_checkbox.setChecked(default_new_tab_checked == "true")
        self.accent_colour = str(settings.value("accent_colour", "#0a6cff"))
        self.accent_edit.setText(self.accent_colour)

    def reset_settings(self):
        settings = QSettings("Tudify", "SimpleWeb")
        settings.setValue("new_tab_url",  "https://tudify.co.uk/simpleweb/newtab.htm")
        settings.setValue("theme", "Dark")
        settings.setValue("search_engine","Google")
        settings.setValue("AI_service", "Nora AI")
        settings.setValue("default_new_tab_checked", "true")
        settings.setValue("accent_colour", "#0a6cff")
        settings.setValue("music_service", "Spotify")
        settings.setValue("initialsetup", "True")
        print("DEBUG: Reset Settings.")      
        settings.sync()
        QMessageBox.information(self, "Settings Reset", "SimpleWeb Will now restart to apply default settings.")
        sys.exit(69)

    def save_settings(self):
        settings = QSettings("Tudify", "SimpleWeb")
        settings.setValue("new_tab_url", self.new_tab_url_edit.text())
        settings.setValue("theme", self.theme_combo.currentText())
        settings.setValue("search_engine", self.search_engine_combo.currentText())
        settings.setValue("AI_service", self.AI_combo.currentText())
        settings.setValue("default_new_tab_checked", "true" if self.default_new_tab_checkbox.isChecked() else "false")
        settings.setValue("accent_colour", self.accent_edit.text())
        settings.setValue("music_service", self.music_combo.currentText())
        print("DEBUG: Saved accent colour:", self.accent_edit.text())        

class DebugWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DebugWindow")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QLabel#heading {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 7px;
            }
            *{font-family: hack, consolas, arial;}
            """)
        
        layout = QVBoxLayout()
        self.heading_label = QLabel("Debug info")
        self.heading_label.setObjectName("heading")
        layout.addWidget(self.heading_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.uatitle = QLabel("UserAgent")
        layout.addWidget(self.uatitle)
        self.uadisplay = QLabel(UserAgent)
        layout.addWidget(self.uadisplay)
        self.ostitle = QLabel("Versioning")
        layout.addWidget(self.ostitle)
        self.osdisplay = QLabel(f"SimpleWeb V{EngineVer} running on: {os_namereport} {arch[0]} with {mem} RAM on {cpuname}, built with {builtonIDE}")
        layout.addWidget(self.osdisplay)
        self.theme_combo = QComboBox()
        layout.addSpacing(20)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        self.setLayout(layout)

class InitialWelcome(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to SimpleWeb!")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QLabel#heading {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 7px;
            }
            *{font-family: hack, consolas, arial;}
            """)
        
        layout = QVBoxLayout()
        self.heading_label = QLabel("Hello. It's good to see you.")
        self.heading_label.setObjectName("heading")
        layout.addWidget(self.heading_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.swwelcme = QLabel("Welcome to SimpleWeb! Here's the basics so you can get going right away.")
        layout.addWidget(self.swwelcme)
        self.cntrls = QLabel("Ctrl + U is the Quick Bar. \n The Quick bar allows you to search the web, or even just go to a website. \n Ctrl + , is settings. \n you can customise almost anything about simpleweb there. \n if you open the Quick Bar and type extensions:// you can get some more useful features.")
        layout.addWidget(self.cntrls)
        layout.addSpacing(20)
        self.setLayout(layout)

    def closeEvent(self, event):
        settings = QSettings("Tudify", "SimpleWeb")
        settings.setValue("initialsetup", "False") 
        settings.sync()
        super().closeEvent(event)

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_settings()
        infofile = getinfo()
        self.setWindowTitle(infofile.get("name", "SimpleWebEngine Window"))
        self.setGeometry(300, 100, 1000, 600)
        print(f"SimpleWebAPI v{APIver}")
        self.refresh_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.refresh_shortcut.activated.connect(self.refresh_page)
        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(self.close_current_tab)
        self.shortcut_settings = QShortcut(QKeySequence("Ctrl+,"), self)
        self.shortcut_settings.activated.connect(self.open_settings_window)
        self.shortcut_new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_new_tab.activated.connect(self.open_default_new_tab)
        self.shortcut_url_popup = QShortcut(QKeySequence("Ctrl+U"), self)
        self.shortcut_url_popup.activated.connect(self.toggle_url_popup)
        self.shortcut_goback = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut_goback.activated.connect(self.go_back)
        self.set_stylesheet(self.theme)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.create_tab_widget()
        self.url_popup = QLineEdit(self)
        self.url_popup.setPlaceholderText("Enter URL or search...")
        self.url_popup.hide()
        self.url_popup.returnPressed.connect(self.handle_quick_url)
        self.url_popup.installEventFilter(self) 
        self.url_popup_width = 400
        self.url_popup_height = 40
        self.update_url_popup_position()
        self.onboardingcheck()
        self.extension_instances = {}
        self.auto_register_shortcuts(simplewebex.SimpleWeb)

        if os_name in ["Windows XP", "Windows Vista", "Windows 7", "Windows 8", "Windows 8.1"]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Insecure Operating System")
            msg.setText(
                "You are using an older version of Windows, which is no longer supported"
                "and is insecure. Please consider upgrading to a newer version of Windows."
                "tudify and the SimpleWeb team accept zero liability for any damage caused "
                "by using this software on an insecure OS."
            )
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec_()

    def initial_hello(self):
        self.initialsetup = InitialWelcome(self)
        self.initialsetup.show()

    def onboardingcheck(self):
        if self.initial_launch == "True":
            self.initial_hello()


    def auto_register_shortcuts(self, module):
        print("\n=== Starting Auto-Registration ===")
        
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if not hasattr(cls, '__module__'):
                continue
            print(f"\nChecking class: {name}")
            shortcut_value = getattr(cls, "Shortcut", None)
            print(f"Shortcut value: {shortcut_value}")
            if not shortcut_value or str(shortcut_value).lower() == "none":
                print(f"INFO: Skipping {name}: No valid shortcut")
                continue
            print(f"✓ Valid shortcut found: {shortcut_value}")

            # Try to instantiate with appropriate parameters
            instance = None
            try:
                # Special handling for different extension types
                if name == "AIsidebar":
                    instance = cls(self, ai_service=self.AI_service)
                    print(f"  ✓ Instantiated {name} with AI service: {self.AI_service}")
                elif name == "QuickNotes":
                    instance = cls(self, theme=self.theme)
                    print(f"  ✓ Instantiated {name} with theme: {self.theme}")
                else:
                    # Default: just pass parent
                    instance = cls(self)
                    print(f"  ✓ Instantiated {name} with parent")
            except TypeError as e:
                print(f"ERROR:  Failed to instantiate {name}: {e}")
                continue
            if instance is None:
                print(f"ERROR: Instance is None for {name}")
                continue
            self.extension_instances[name] = instance
            print(f"  ✓ Stored instance in extension_instances")
            toggle_method = None
            toggle_method_name = None
            print(f"Locating... One Minute...")
            for attr_name in dir(instance):
                if attr_name.startswith("toggle"):
                    attr = getattr(instance, attr_name, None)
                    if callable(attr):
                        toggle_method = attr
                        toggle_method_name = attr_name
                        print(f"Found: {attr_name}")
                        break
            if not toggle_method:
                print(f"ERROR: No toggle method found for {name}")
                continue
            print(f"  ✓ Using toggle method: {toggle_method_name}")
            try:
                shortcut = QShortcut(QKeySequence(shortcut_value), self)
                shortcut.activated.connect(toggle_method)
                print(f"  ✓✓✓ Successfully registered {shortcut_value} -> {name}.{toggle_method_name}")
            except Exception as e:
                print(f"ERROR: Failed to create shortcut: {e}")
        print("\n=== Auto-Registration Complete ===\n")

    def TrackMeNot_enabled(self):
        settings = QSettings("Tudify", "SimpleWeb-Extensions")
        # keep the same key you used when building the ExtensionsWindow
        return settings.value("TrackMeNot", False, type=bool)

    def load_settings(self):
        settings = QSettings("Tudify", "SimpleWeb")
        self.new_tab_url = settings.value("new_tab_url", "https://tudify.co.uk/simpleweb/newtab.htm")
        self.accent_colour = str(settings.value("accent_colour", "#0a6cff"))
        self.theme = settings.value("theme", "dark")
        self.default_new_tab_enabled = settings.value("default_new_tab_checked", "false") == "true"
        self.search_engine = settings.value("search_engine", "Google")
        self.AI_service = settings.value("AI_service", "Nora AI")
        self.music_service = settings.value("music_service", "Spotify")
        self.initial_launch = settings.value("initialsetup")
        print(f"DEBUG: Loaded accent colour: {self.accent_colour}")
        self.chromium_spoofer = SimpleWeb.ChromiumSpoofer(self)
        self.chromium_spoofer.apply_chromium_spoofer()

    def save_settings(self):
        settings = QSettings("Tudify", "SimpleWeb")
        settings.setValue("new_tab_url", self.new_tab_url)
        settings.setValue("theme", self.theme)
        settings.setValue("default_new_tab_checked", "true" if self.default_new_tab_enabled else "false")
        settings.setValue("search_engine", self.search_engine)
        settings.setValue("AI_service", self.AI_service)
        settings.setValue("music_service", self.music_service)
        self.music_sidebar = simplewebex.SimpleWeb.MusicSidebar(self)
        self.music_sidebar.refresh_page()
        settings.setValue("accent_colour", self.accent_colour)


    def open_default_new_tab(self):
        if self.default_new_tab_enabled:
            self.add_new_tab(QUrl(self.new_tab_url))
        else:
            self.add_new_tab(QUrl("https://tudify.co.uk/simpleweb/newtab.htm"))

    def toggle_url_popup(self):
        if self.url_popup.isVisible():
            self.url_popup.clear()
            self.url_popup.hide()
        else:
            self.url_popup.show()
            self.url_popup.raise_()
            self.url_popup.setFocus()
            
    def eventFilter(self, source, event):
        if source is self.url_popup and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self.url_popup.clear()
                self.url_popup.hide()
                return True
        return super().eventFilter(source, event)

    def handle_quick_url(self):
        text = self.url_popup.text().strip()
        if not text:
            self.url_popup.hide()
            return

        url_to_load = None

        # Handle Tudify commands
        if text.startswith(('tudify://', 'debug://', 'extensions://', '/weather')):
            if text in ('tudify://settings', 'tudify://setup', 'tudify://set', 'tudify://config'):
                self.open_settings_window()
                self.url_popup.clear()
                self.url_popup.hide()
                return
            elif text in ('debug://flags', 'debug://devflags'):
                self.debugwin = DebugWindow(self)
                self.debugwin.show()
                self.url_popup.clear()
                self.url_popup.hide()
                return
            elif text.startswith('/weather'):
                self.url_popup.clear()
                url_to_load = 'http://tudify.co.uk/weather'
            elif text.startswith('extensions://'):
                if text == 'extensions://store':
                    url_to_load = 'http://tudify.co.uk/simpleweb/extensions/store/'
                elif text == 'extensions://':
                    self.extensions_window = ExtensionsWindow(self)
                    self.extensions_window.show()
                    self.url_popup.clear()
                    self.url_popup.hide()
                else:
                    print("Error")
            elif text == 'tudify://newtab':
                url_to_load = 'https://tudify.co.uk/simpleweb/newtab.htm'
            else:
                print("Unknown tudify command:", text)
                url_to_load = 'https://tudify.co.uk/simpleweb/404/'
        
        elif text.startswith("file://"):
            url_to_load = text

        elif not text.startswith(('http://', 'https://')):
            # Use selected search engine
            
            search_eng = self.search_engine.lower()
            if '.' not in text:  # assume search
                if search_eng == "google":
                    url_to_load = f"https://www.google.com/search?q={urllib.parse.quote_plus(text)}"
                elif search_eng == "duckduckgo":
                    url_to_load = f"https://duckduckgo.com/?q={urllib.parse.quote_plus(text)}"
                elif search_eng == "bing":
                    url_to_load = f"https://www.bing.com/search?q={urllib.parse.quote_plus(text)}"
            else:
                url_to_load = 'https://' + text

        else:
            url_to_load = text  # already has https/http

        # No need to pre-check URL reachability; let the browser handle errors

        # Load the URL in the current tab
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url_to_load))
        else:
            self.add_new_tab(QUrl(url_to_load))

        # Clear and hide the popup
        self.url_popup.clear()
        self.url_popup.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_url_popup_position()

    def update_url_popup_position(self):
        x = (self.width() - self.url_popup_width) // 2
        y = 20  # distance from top
        self.url_popup.setGeometry(x, y, self.url_popup_width, self.url_popup_height)

    def set_stylesheet(self, theme):
        accent = self.accent_colour
        print(f"DEBUG: Applying {theme} Theme with accent: {accent}")

        style_dark = f"""
            *{{font-family: hack, arial;}}
            QMainWindow {{
                background-color: #202326;
                color: #ffffff;
            }}
            QPushButton {{
                background-color: #292c30;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #414346;
            }}
            QPushButton:hover {{
                background-color: #292c30;
                border: 1px solid {accent};
            }}
            QLineEdit {{
                background-color: #292c30;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid {accent};
            }}
            QLineEdit:focus {{
                background-color: #292c30;
                border: 1px solid {accent};
            }}
            QTabBar::tab {{
                background-color: #292c30;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #414346;
            }}
            QTabBar::tab:selected {{
                background-color: #292c30;
                border: 1px solid {accent};
            }}
        """

        style_light = f"""
            *{{font-family: hack;}}
            QMainWindow {{
                background-color: #f5f5f5;
                color: #000000;
            }}
            QPushButton {{
                background-color: #e0e0e0;
                color: #000000;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #cccccc;
            }}
            QPushButton:hover {{
                border: 1px solid {accent};
            }}
            QLineEdit {{
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                padding: 10px;
                border-radius: 6px;
            }}
            QLineEdit:focus {{
                border: 1px solid {accent};
            }}
            QTabBar::tab {{
                background-color: #e0e0e0;
                color: #000000;
                padding: 8px 20px;
                border-radius: 6px;
                margin-right: 4px;
            }}
            QTabBar::tab:selected {{
                border: 1px solid {accent};
            }}
        """

        if theme.lower() == "dark":
            self.setStyleSheet(style_dark)
        else:
            self.setStyleSheet(style_light)

        if hasattr(self, 'tabs') and hasattr(self, 'new_tab_button'):
            self.new_tab_button.setFixedSize(50, 50)
            self.new_tab_button.setStyleSheet(f"""
                QPushButton {{
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 16px;
                    border: 1px solid {accent};
                }}
                QPushButton:hover {{
                    background-color: {accent};
                    color: white;
                }}
            """)


    def create_tab_widget(self):
        self.tabs = QTabWidget()
        self.tabs.tabCloseRequested.connect(lambda index: self.tabs.removeTab(index))
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        tabbar = self.tabs.tabBar()
        tabbar.setExpanding(False)
        tabbar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        tabbar.setStyleSheet("QTabBar { qproperty-drawBase: 0; } QTabBar::tab { margin-right: 2px; }")
        self.central_layout.addWidget(self.tabs)
        self.add_new_tab(QUrl('https://tudify.co.uk/simpleweb/newtab.htm'))

    def add_new_tab(self, qurl):
        if qurl is None or qurl.isEmpty():
            # Use default new tab URL if the provided URL is empty
            if self.default_new_tab_enabled:
                qurl = QUrl(self.new_tab_url)
            else:
                qurl = QUrl('https://tudify.co.uk/simpleweb/newtab.htm')

        # Create a new instance of QWebEngineView
        browser = QWebEngineView()
        settings = browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setFontFamily(QWebEngineSettings.FontFamily.StandardFont, "Hack")
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(UserAgent)
        profile.setHttpCacheMaximumSize(10240)
        browser.page().titleChanged.connect(lambda title: self.update_tab_title(browser))
        browser.setUrl(qurl)
        self.tabs.addTab(browser, qurl.toString())
        self.tabs.setCurrentWidget(browser)
        if self.TrackMeNot_enabled():
            print("TrackMeNot is enabled: Applying strict privacy settings.")
            profile = QWebEngineProfile(parent=None)
            profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.NoCache)
            profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, False)
            browser.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
            profile.setHttpUserAgent("Mozilla/5.0 (X11; Linux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        else:
            print("TrackMeNot is disabled: Applying standard privacy settings.")
            profile = QWebEngineProfile.defaultProfile()
            profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
            profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
            browser.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            if self.chromium_spoofer.chromium_spoofer_enabled():
                profile.setHttpUserAgent(ChromiumUserAgent)
                print("UA: " + ChromiumUserAgent)
            else:
                profile.setHttpUserAgent(UserAgent)
                print("UA: " + UserAgent)

        if not self.TrackMeNot_enabled():
            self.channel = QWebChannel(browser.page())
            self.api = SimpleWebAPI()
            self.channel.registerObject("SimpleWeb", self.api)
            browser.page().setWebChannel(self.channel)

    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        title = browser.title()
        if title:
            self.tabs.setTabText(index, title)
        else:
            self.tabs.setTabText(index, "no title")

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        if (current_index != -1):
            self.tabs.removeTab(current_index)
            if self.tabs.count() == 0: sys.exit()

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.finished.connect(self.handle_settings_closed)
        self.settings_window.show()

    def update_ai_sidebar_url(self):
        ai_services = {
            "ChatGPT": "https://chat.openai.com/",
            "Amanda AI 2": "https://poe.com/Amanda-AI/",
            "Nora AI": "https://tudify.co.uk/Luna-AI/", # this URL would be changed if it didnt break old versions lol
            "Claude": "https://claude.ai/",
            "Gemini": "https://gemini.google.com/"
        }
        ai_url = ai_services.get(self.AI_service, "https://chat.openai.com/")
        simplewebex.AISideBar.ai_browser.setUrl(QUrl(ai_url))

    def handle_settings_closed(self, result):
        if result == QDialog.accepted:
            self.new_tab_url = self.settings_window.new_tab_url_edit.text()
            self.theme = self.settings_window.theme_combo.currentText().lower()
            self.default_new_tab_enabled = self.settings_window.default_new_tab_checkbox.isChecked()
            self.search_engine = self.settings_window.search_engine_combo.currentText()
            self.AI_service = self.settings_window.AI_combo.currentText()
            self.accent_colour = self.settings_window.accent_edit.text()
            self.update_ai_sidebar_url()
            self.set_stylesheet(self.theme)
            self.save_settings()
            current_browser = self.tabs.currentWidget()
            if current_browser:
                current_browser.reload()

    def handle_init_closed(self):
        settings = QSettings("Tudify", "SimpleWeb")
        settings.setValue("initialsetup", "False")

    def handle_download(self, download_item):
        url = download_item.url().toString()
        file_name = os.path.basename(url)
        base_name, file_extension = os.path.splitext(file_name)
        default_file_name = base_name + file_extension
        selected_filter = f"{file_extension[1:].upper()} Files (*{file_extension})"
        download_path, _ = QFileDialog.getSaveFileName(self, "Save File", default_file_name, selected_filter)  
        if download_path:
            download_item.setPath(download_path)
            download_item.accept()

    def go_back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()

    def refresh_page(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()

    def handle_copy_result(self, result):
        clipboard = QApplication.clipboard()
        clipboard.setText(result)

    def handle_fullscreen_request(self, request):
        request.accept()
        if request.toggleOn():
            self.showFullScreen()
        else:
            self.showNormal()

Search_engine = "Google"  # Default search engine
if Search_engine == "Google":
    Search_URL = "https://www.google.com/search?q="
elif Search_engine == "DuckDuckGo":
    Search_URL = "https://duckduckgo.com/?q="
elif Search_engine == "Bing":
    Search_URL = "https://www.bing.com/search?q="

cpuname = platform.processor()
os_name = platform.system()
arch = platform.architecture()

def getinfo():
    base_dir = Path(__file__).resolve().parent
    info_path = base_dir / "info.json"
    if info_path.exists():
        try:
            with info_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise TypeError("info.json is not found or is corrupted.", e)
    else:
        raise FileNotFoundError("info.json not found!")
    
name = getinfo().get("name", "unknown")
builtonIDE = getinfo().get("ide", "VS code 1.105.1")
EngineName = getinfo().get("engine", "Unknown")
EngineVer = getinfo().get("version", "Unknown")
APIver = "1.0.2" 
mem = psutil.virtual_memory().total / (1024 ** 3)

if os_name in ("Darwin", "macOS", "Mac", "Mac OS X"):
    macver = platform.mac_ver()[0].replace('.', '_')
if os_name in ("Darwin", "macOS", "Mac", "Mac OS X"):
    os_namefinal = "Macintosh; Intel Mac OS X " + macver
    os_namereport = "macOS"
if os_name == "Linux":
    os_namefinal = "X11; Linux " + arch
    os_namereport = "Linux"
if os_name.startswith("Windows"):
    os_namefinal = "Windows NT 10.0; Win64; x64"
    os_namereport = "Windows"

print(f"SimpleWeb V{EngineVer} running on: {os_namereport} {arch[0]} with {mem} GB RAM, built with {builtonIDE}")

if cpuname == "arm" and os_namereport == "macOS":
    cpunamefinal = "Apple Silicon"
else:
    cpunamefinal = "Intel"

if os_namereport == "macOS":
    print(f"SimpleWeb on {os_namereport} ({cpunamefinal})")
else:
    print(f"SimpleWeb on {os_namereport}")

UserAgent = (
    f"Mozilla/5.0 ({os_namefinal}) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    f"{EngineName}/{EngineVer} Safari/605.1.15"
)

ChromiumUserAgent = (
    f"Mozilla/5.0 ({os_namefinal}) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    f"Chromium/141.0 Safari/605.1.15"
)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    updater.check_for_update()
    window.show()
    sys.exit(app.exec())