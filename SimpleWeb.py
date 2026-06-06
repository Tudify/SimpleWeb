# Copyright (c) 2026 tudify
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file. The requirements
# of the GNU General Public License version 3.0 can be found here:
# http://www.gnu.org/copyleft/gpl.html.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

import sys, os, platform, urllib.parse, json, psutil, subprocess, updater, inspect, simplewebex, darkdetect
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar,QMenu, QHBoxLayout, QWidget, QMessageBox,QVBoxLayout, QLineEdit, QTabWidget, QFileDialog,  QDialog, QLabel,  QDialogButtonBox, QComboBox, QCheckBox, QColorDialog, QPushButton)
from PyQt6.QtCore import QUrl, Qt, QSettings, QEvent, QObject, pyqtSlot, QEventLoop
from PyQt6.QtGui import QKeySequence, QAction, QShortcut
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage, QWebEngineDownloadRequest, QWebEngineFullScreenRequest, QWebEnginePermission, QWebEngineFileSystemAccessRequest
from PyQt6.QtWebChannel import QWebChannel
from pathlib import Path
from simplewebex import SimpleWeb # this file's ln count needs saving.

script_dir = os.path.dirname(os.path.abspath(__file__))
exe_path = os.path.join(script_dir, "simpleweblib")
result = subprocess.run([exe_path], capture_output=True, text=True)
print(result.stdout)
#MARK: GetWebPage
class getwebpage(QWebEnginePage):
    """Load a URL and return the rendered HTML source code."""
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        super().__init__()

        self.html = None
        self.loadFinished.connect(self._on_load_finished)

    def fetch(self, url: str) -> str:
        self.html = None
        self._loop = QEventLoop()

        self.load(QUrl(url))
        print("Loading URL:", url)
        self._loop.exec_()
        return self.html

    def _on_load_finished(self, ok: bool):
        if not ok:
            self.html = ""
            self._loop.quit()
            return
        self.toHtml(self._store_html)
    def _store_html(self, html: str):
        self.html = html
        self._loop.quit()

#MARK: ExtensionsWindow

class ExtensionsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Extensions - SimpleWeb")
        self.setGeometry(100, 100, 400, 300)
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
        base_dir = Path(__file__).resolve().parent
        extensions_file = base_dir / "extensions.json"
        if extensions_file.exists():
            try:
                with extensions_file.open("r", encoding="utf-8") as f:
                    extensions = json.load(f)
            except Exception as e:
                print(f"Failed to read {extensions_file.name}: {e}")
                msg = QMessageBox()
                msg.setText("Fatal Error\n\nSimpleWeb could not read from its internal files. \n extensions.json not readable (3)")
                msg.exec()
                raise TypeError(f"simplewebex is malformed or corrupted. {e}")
        else:
            msg = QMessageBox()
            msg.setText("Fatal Error\n\nSimpleWeb could not read from its internal files. \n extensions.json not found (0)")
            msg.exec()
            raise FileNotFoundError("extensions.json is missing.")
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
        if self.parent() is not None and hasattr(self.parent(), "apply_chromium_spoofer"):
            try:
                self.parent().apply_chromium_spoofer()
            except Exception as e:
                msg = QMessageBox()
                msg.setText(f"Fatal Error\n\nCould not save settings to simpleweb-extensions \n {e} (2)")
                raise TypeError(f"info.json is malformed or corrupted. {e}")
        self.accept()

#MARK: SimpleWebEngine About

class AboutSWE(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About SimpleWebEngine")
        self.setGeometry(100, 100, 467, 120)
        layout = QVBoxLayout()
        versions = EngineVer
        self.heading_label = QLabel(f"This Program Uses SimpleWebEngine {versions}")
        layout.addWidget(self.heading_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.new_current_label = QLabel(f"An open-source project by tudify & its users. \n SimpleWebEngine is liscenced under the GPL v3 Lisence.\n Uses Qt and Chromium.")
        layout.addWidget(self.new_current_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

#MARK: SimpleWeb About

class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About SimpleWeb")
        self.setGeometry(100, 100, 200, 100)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        layout = QVBoxLayout()
        versions = EngineVer
        print(versions)
        self.heading_label = QLabel("SimpleWeb")
        self.heading_label.setObjectName("heading")
        layout.addWidget(self.heading_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.new_current_label = QLabel(f"An open-source project by tudify. \n")
        layout.addWidget(self.new_current_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.verlabel = QLabel(f"version: {versions}")
        layout.addWidget(self.verlabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

#MARK: SimpleWebAPI

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
    def checkver(self):
        # Return the SimpleWeb application version for runtime compatibility checks.
        return getinfo().get("version", "0.0.0")
    
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
        if theme.lower() == "auto":
            if current_theme.lower() == "dark":
                return "dark"
            else:
                return "light"
        else:
            return theme

    @pyqtSlot(result=str)
    def GetUserTheme(self):
        return self.getUserTheme()
    
    @pyqtSlot(result=str)
    def macVersion(self):
        if os_namereport == "macOS":
            return macver
        else:
            return "null"
    
    @pyqtSlot(str)
    def print(self, text):
        print(text)

    @pyqtSlot(str)
    def setWindowTitle(self, title):
        """Sets title for the main browser window (if linked)."""
        if self.main_window:
            self.main_window.setWindowTitle(title)
        else:
            if self.windows:
                self.windows[-1].setWindowTitle(title)

    def _account_file_path(self):
        account_dir = Path.home() / ".tudifyID"
        account_dir.mkdir(parents=True, exist_ok=True)
        return account_dir / "Details.json"

    def _load_accounts(self):
        account_file = self._account_file_path()
        if account_file.exists():
            try:
                with account_file.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_accounts(self, data):
        account_file = self._account_file_path()
        with account_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @pyqtSlot(str, str, result=str)
    def CreateAccount(self, username, password):
        if not username or not password:
            return "error"
        data = self._load_accounts()
        accounts = data.get("accounts", {})
        if username in accounts:
            return "exists"
        accounts[username] = {"password": password}
        data["accounts"] = accounts
        self._save_accounts(data)
        return "success"

    @pyqtSlot(str, str, result=str)
    def EditAccount(self, username, password):
        if not username or not password:
            return "error"
        data = self._load_accounts()
        accounts = data.get("accounts", {})
        if username not in accounts:
            return "not_found"
        accounts[username]["password"] = password
        data["accounts"] = accounts
        self._save_accounts(data)
        return "success"

    @pyqtSlot(str, str, result=str)
    def VerifyAccount(self, username, password):
        if not username or not password:
            return "false"
        data = self._load_accounts()
        accounts = data.get("accounts", {})
        if username not in accounts:
            return "false"
        return "true" if accounts[username].get("password") == password else "false"

#MARK: SettingsWindow

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 300)
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
        self.theme_combo.addItems(["Auto", "Dark", "Light"])
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
        self.accent_note = QLabel("NOTE: \n All settings changes \n will require a restart to apply.")
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
        self.theme_combo.setCurrentText(settings.value("theme", "auto"))
        self.search_engine_combo.setCurrentText(settings.value("search_engine", "Google"))
        self.AI_combo.setCurrentText(settings.value("AI_service", "Nora AI"))
        self.music_combo.setCurrentText(settings.value("music_service", "Spotify"))
        default_new_tab_checked = settings.value("default_new_tab_checked", False, type=bool)
        self.default_new_tab_checkbox.setChecked(default_new_tab_checked)
        self.accent_colour = str(settings.value("accent_colour", "#0a6cff"))
        self.accent_edit.setText(self.accent_colour)

    def reset_settings(self):
        settings = QSettings("Tudify", "SimpleWeb")
        settings.setValue("new_tab_url",  "https://tudify.co.uk/simpleweb/newtab.htm")
        settings.setValue("theme", "auto")
        settings.setValue("search_engine","Google")
        settings.setValue("AI_service", "Nora AI")
        settings.setValue("default_new_tab_checked", True)
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
        settings.setValue("default_new_tab_checked", self.default_new_tab_checkbox.isChecked())
        settings.setValue("accent_colour", self.accent_edit.text())
        settings.setValue("music_service", self.music_combo.currentText())
        print("DEBUG: Saved accent colour:", self.accent_edit.text())        

#MARK: Debug Window

class DebugWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DebugWindow")
        self.setGeometry(100, 100, 400, 300)

        self.json_path = os.path.join(os.path.dirname(__file__), "info.json")
        self.info = self.load_json()
        chromium_spoofer = None
        if parent is not None and hasattr(parent, "chromium_spoofer"):
            chromium_spoofer = parent.chromium_spoofer
        else:
            try:
                chromium_spoofer = SimpleWeb.ChromiumSpoofer(parent or self)
            except Exception:
                chromium_spoofer = None
        try:
            currentchromiumstate = chromium_spoofer.chromium_spoofer_enabled() if chromium_spoofer else False
        except Exception:
            currentchromiumstate = False
        if currentchromiumstate:
            CurrentUA = ChromiumUserAgent
        else:
            CurrentUA = UserAgent
        layout = QVBoxLayout()
        self.heading_label = QLabel("Debug Flags")
        self.heading_label.setObjectName("heading")
        layout.addWidget(self.heading_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.ostitle = QLabel("Versioning")
        layout.addWidget(self.ostitle)
        self.osdisplay = QLabel(f"SimpleWeb {EngineVer} on {os_namereport} ({cpunamefinal})")
        layout.addWidget(self.osdisplay)
        self.cbn = QLabel("Set a Custom Browser Name:")
        layout.addWidget(self.cbn)
        self.CustomBrowserName = QLineEdit()
        self.CustomBrowserName.setText(self.info.get("name", ""))
        layout.addWidget(self.CustomBrowserName)
        self.ua_label = QLabel("Edit UserAgent:")
        layout.addWidget(self.ua_label)
        self.ua_edit = QLineEdit()
        self.ua_edit.setText(CurrentUA)
        layout.addWidget(self.ua_edit)
        self.font_label = QLabel("Set Custom Font Name:")
        layout.addWidget(self.font_label)
        self.font_edit = QLineEdit()
        self.font_edit.setText(self.info.get("font", "Hack"))
        layout.addWidget(self.font_edit)
        layout.addSpacing(20)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.save_and_close)
        layout.addWidget(button_box)
        self.setLayout(layout)
    def load_json(self):
        if not os.path.exists(self.json_path):
            raise FileNotFoundError("info.json must be in the same directory!")
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            raise FileNotFoundError("info.json must be in the same directory!")
    def save_json(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.info, f, indent=4)
    def save_and_close(self):
        global UserAgent
        self.info["name"] = self.CustomBrowserName.text().strip()
        self.info["font"] = self.font_edit.text().strip()  # save the font
        UserAgent = self.ua_edit.text().strip()
        self.save_json()
        self.accept()

#MARK: InitialWelcome

class InitialWelcome(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to SimpleWeb!")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.heading_label = QLabel("Hello. It's good to see you.")
        self.heading_label.setObjectName("heading")
        layout.addWidget(self.heading_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.swwelcme = QLabel("Welcome to SimpleWeb! Here's the basics so you can get going right away.")
        self.swwelcme.setObjectName("welcome")
        layout.addWidget(self.swwelcme)

        self.cntrls = QLabel("""
        <b>Keyboard Shortcuts:</b><br><br>
        • <b>Ctrl + U</b> — Quick Bar<br>
        • <b>Ctrl + ,</b> — Settings<br>
        • <b>extensions:// (type inside of Quick Bar)</b> — Extensions Panel<br>
        • <b>Ctrl + Z</b> — Back<br>
        • <b>Ctrl + R</b> — Refresh
        """)

        layout.addWidget(self.cntrls)

        layout.addSpacing(20)

        self.settings_btn = QPushButton("Open Settings")
        self.settings_btn.clicked.connect(self.openSettings)
        layout.addWidget(self.settings_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)
    
    def openSettings(self):
        BrowserWindow.settings_window = SettingsWindow(self)
        BrowserWindow.settings_window.show()

    def closeEvent(self, event):
        settings = QSettings("Tudify", "SimpleWeb")
        settings.setValue("initialsetup", "False") 
        settings.sync()
        super().closeEvent(event)

#MARK: Main - BrowserWindow

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_settings()
        self.checkwintitle()
        self.setWindowTitle(name)
        self.setGeometry(225, 150, 1270, 760)
        print(f"SimpleWebAPI v{APIver}")

        self.refresh_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.refresh_shortcut.activated.connect(self.refresh_page)
        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(self.close_current_tab)
        self.shortcut_settings = QShortcut(QKeySequence("Ctrl+,"), self)
        self.shortcut_settings.activated.connect(self.open_settings_window)
        self.shortcut_new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_new_tab.activated.connect(self.open_default_new_tab)
        self.shortcut_toggle_tabbar = QShortcut(QKeySequence("F11"), self)
        self.shortcut_toggle_tabbar.activated.connect(self.toggle_tab_bar)
        self.shortcut_url_popup = QShortcut(QKeySequence("Ctrl+U"), self)
        self.shortcut_url_popup.activated.connect(self.toggle_url_popup)
        self.shortcut_find_popup = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_find_popup.activated.connect(self.toggle_find_popup)
        self.shortcut_goback = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut_goback.activated.connect(self.go_back)

        self.set_stylesheet(self.theme)
        menubar(self)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.create_tab_widget()
        self.url_popup = QLineEdit(self)
        self.url_popup.setPlaceholderText("Enter URL or search...")
        self.url_popup.hide()
        self.url_popup.returnPressed.connect(self.handle_quick_url)
        self.url_popup.installEventFilter(self) 
        self.find_popup = QLineEdit(self)
        self.find_popup.setPlaceholderText("Search this Webpage...")
        self.find_popup.hide()
        self.find_popup.installEventFilter(self) 
        self.popups_width = 400
        self.popups_height = 40
        self.update_url_popup_position()
        self.update_find_pos()
        self.onboardingcheck()
        self.extension_instances = {}
        self.auto_register_shortcuts(simplewebex.SimpleWeb)
        self.debugwin = DebugWindow(self)
        self.versioncheck()
# MARK: Support Check
    def versioncheck(self):
        if os_namereport.startswith("Windows"):
            if winver in ["XP", "Vista", "7", "8", "8.1"]:
                self.supportissuewindow()
                print("version check failed!")
            else:
                print("version check passed: Windows 10/11")
        if os_namereport.startswith("macOS"):
            if not macver.startswith("26_"):
                self.supportissuewindow()
                print("version check failed!")
            else:
                print("version check passed: macOS 26")
        #if you imagine it supports linux, it supports linux!
    
    def supportissuewindow(self):
        msg = QMessageBox()
        msg.setWindowTitle("Insecure Operating System")
        msg.setText(
            f"""You are using an older version of {os_namereport}, which is no longer supported 
            and is insecure. Please consider upgrading to a newer version of {os_namereport}. 
            tudify and the SimpleWeb team accept zero liability for any damage caused 
            by using this software on an insecure OS.""")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def checkwintitle(self):
        if name == "null":
            winnullmsg = QMessageBox()
            winnullmsg.setText("Fatal Error \n Window title cannot be null. \n null_err (1)")
            winnullmsg.exec()

    def initial_hello(self):
        self.initialsetup = InitialWelcome(self)
        self.initialsetup.show()

    def onboardingcheck(self):
        if self.initial_launch == "True":
            self.initial_hello()

    def findonpage(self, browser: QWebEngineView, text: str):
        current_browser = self.tabs.currentWidget()
        if not text:
            current_browser.page().findText("", QWebEnginePage.FindFlag(0))
            return

        current_browser.page().findText(text, QWebEnginePage.FindFlag(0),
            lambda result: print(f"Found {result.numberOfMatches()} matches, active match {result.activeMatch()}"))

    def toggle_find_popup(self):
        if self.find_popup.isVisible():
            self.find_popup.clear()
            self.find_popup.hide()
        else:
            self.find_popup.show()
            self.find_popup.raise_()
            self.find_popup.setFocus()

    def toggle_tab_bar(self):
        tabbar = self.tabs.tabBar()
        if tabbar.isVisible():
            tabbar.hide()
        else:
            tabbar.show()
# MARK: Shortcut handler
    def auto_register_shortcuts(self, module):        
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if not hasattr(cls, '__module__'):
                continue
            shortcut_value = getattr(cls, "Shortcut", None)
            if not shortcut_value or str(shortcut_value).lower() == "none":
                continue
            instance = None
            try:
                if name == "AIsidebar":
                    instance = cls(self, ai_service=self.AI_service)
                else:
                    instance = cls(self)
            except TypeError as e:
                continue
            if instance is None:
                continue
            self.extension_instances[name] = instance
            toggle_method = None
            toggle_method_name = None
            for attr_name in dir(instance):
                if attr_name.startswith("toggle"):
                    attr = getattr(instance, attr_name, None)
                    if callable(attr):
                        toggle_method = attr
                        toggle_method_name = attr_name
                        break
            if not toggle_method:
                continue
            try:
                shortcut = QShortcut(QKeySequence(shortcut_value), self)
                shortcut.activated.connect(toggle_method)
            except Exception as e:
                extmsg = QMessageBox()
                extmsg.setWindowTitle("Non-Fatal Error")
                extmsg.setText(
                    "Non-Fatal Error\nSimpleWeb failed to initialise extensions."
                    "SimpleWeb will continue."
                    "simplewebex_not_found (4)")
                extmsg.exec()
# MARK: Settings Checker
    def TrackMeNot_enabled(self):
        settings = QSettings("Tudify", "SimpleWeb-Extensions")
        return settings.value("TrackMeNot", False, type=bool)

    def load_settings(self):
        settings = QSettings("Tudify", "SimpleWeb")
        self.new_tab_url = settings.value("new_tab_url", "https://tudify.co.uk/simpleweb/newtab.htm")
        self.accent_colour = str(settings.value("accent_colour", "#0a6cff"))
        self.theme = settings.value("theme", "auto")
        self.default_new_tab_enabled = settings.value("default_new_tab_checked", False, type=bool)
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
        settings.setValue("default_new_tab_checked", self.default_new_tab_enabled)
        settings.setValue("search_engine", self.search_engine)
        settings.setValue("AI_service", self.AI_service)
        settings.setValue("music_service", self.music_service)
        self.music_sidebar = simplewebex.SimpleWeb.MusicSidebar(self)
        self.music_sidebar.refresh_page()
        settings.setValue("accent_colour", self.accent_colour)
# MARK: Default New Tab
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
        elif source is self.find_popup and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.findonpage(self.tabs.currentWidget(), self.find_popup.text())
                return True 
            return False
        return super().eventFilter(source, event)
# MARK: URL handler
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
                    return
                else:
                    print("Error")
                    url_to_load = 'https://tudify.co.uk/simpleweb/404/'
            elif text == 'tudify://newtab':
                url_to_load = 'https://tudify.co.uk/simpleweb/newtab.htm'
            else:
                print("Unknown tudify command:", text)
                url_to_load = 'https://tudify.co.uk/simpleweb/404/'
        
        elif text.startswith("file://"):
            url_to_load = text

        elif not text.startswith(('http://', 'https://')):
            
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

        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url_to_load))
        else:
            self.add_new_tab(QUrl(url_to_load))

        self.url_popup.clear()
        self.url_popup.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_url_popup_position()
        self.update_find_pos()

    def update_find_pos(self):
        x = (self.width() - self.popups_width) // 2
        y = 20  # distance from top
        self.find_popup.setGeometry(x, y, self.popups_width, self.popups_height)

    def update_url_popup_position(self):
        x = (self.width() - self.popups_width) // 2
        y = 20  # distance from top
        self.url_popup.setGeometry(x, y, self.popups_width, self.popups_height)
# MARK: Stylesheet
    def set_stylesheet(self, theme):
        accent = self.accent_colour
        print(f"DEBUG: Applying {theme} Theme with accent: {accent}")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        style_dark = f"""
            *{{
                font-family:{font_name}, hack, arial;
                color: #ffffff;
            }}
            QMainWindow {{
                background-color: #202326;
                color: #ffffff;
                border: none;
            }}
            QLabel#heading {{
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 7px;
            }}
            QLabel#welcome {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 7px;
            }}
            QWebEngineView {{
                border: none;
                outline: none;
                background: transparent;
            }}
            QMenu {{
                background-color: #2b2b2b;
                color: white;
                border-radius: 8px;
                border: 1px solid #444;
                padding: 6px;
            }}
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}
            QMenu::item {{
                padding: 6px 20px;
                background-color: transparent;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: #3c3c3c;
                border-radius: 4px;
            }}
            QComboBox{{
                background-color: #292c30;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #414346;
                padding: 10px 16px 10px 16px;
            }}
            QComboBox:focus {{
                background-color: #292c30;
                border: 1px solid {accent};
            }}
            QDialog{{
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
                border: 1px solid #414346;
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
            *{{
                font-family:{font_name}, hack, arial;
                color: #000000;
                }}
            QMainWindow {{
                background-color: #f5f5f5;
            }}
            QDialog {{
                background-color: #f5f5f5;
                text-color: #000000;
            }}
            QWebEngineView {{
                border: none;
                outline: none;
                background: transparent;
            }}
            QLabel#heading {{
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 7px;
            }}
            QLabel#welcome {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 7px;
            }}
            QMenu {{
                background-color: #e3e3e3;
                color: black;
                border-radius: 8px;
                border: 1px solid #ccc;
                padding: 6px;
            }}
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}
            QMenu::item {{
                padding: 6px 20px;
                background-color: transparent;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: #ffffff;
                border-radius: 4px;
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
        elif theme.lower() == "light":
            self.setStyleSheet(style_light)
        elif theme.lower() == "auto":
            if os_namereport != "Linux":
                if current_theme.lower() == "dark":
                    self.setStyleSheet(style_dark)
                else:
                    self.setStyleSheet(style_light)
            else:
                self.setStyleSheet(style_dark)
        else:
            thmemsg = QMessageBox()
            thmemsg.setWindowTitle("Settings Error")
            thmemsg.setText(
                "Settings Error\nSimpleWeb failed to initialise due"
                "to an unknown setting."
                "themenotfound error (5)"
            )
            thmemsg.exec()
            sys.exit()

# MARK: Browsing Experiences

    def docs(self, url):
        current_browser = self.tabs.currentWidget()
        if current_browser is not None:
            current_browser.setUrl(QUrl(url))

    def create_tab_widget(self):
        self.tabs = QTabWidget()
        self.tabs.tabCloseRequested.connect(lambda index: self.tabs.removeTab(index))
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        tabbar = self.tabs.tabBar()
        tabbar.setExpanding(False)
        tabbar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        tabbar.setStyleSheet("QTabBar { qproperty-drawBase: 0;} QTabBar::tab { margin-right: 5px; }")
        self.central_layout.addWidget(self.tabs)
        self.add_new_tab(QUrl('https://tudify.co.uk/simpleweb/newtab.htm'))

    def sw_context_menu(self, pos):
        self.find_popup.hide()
        self.url_popup.hide()
        browser = self.sender()
        page = browser.page()
        menu = QMenu(self)
        act_copy = page.action(QWebEnginePage.WebAction.Copy)
        act_copy.setText("⧉ Copy")
        act_cut = page.action(QWebEnginePage.WebAction.Cut)
        act_cut.setText("✂ Cut")
        act_paste = page.action(QWebEnginePage.WebAction.Paste)
        act_paste.setText("| Paste")
        menu.addAction(act_copy)
        menu.addAction(act_paste)
        menu.addAction(act_cut)
        menu.addSeparator() 
        back_action = menu.addAction("← Back")
        find_action = menu.addAction("⌕ Find")
        reload_action = menu.addAction("↻ Reload")
        selected = menu.exec(browser.mapToGlobal(pos))
        if selected == back_action:
            self.go_back()
        elif selected == find_action:
            self.toggle_find_popup()
        elif selected == reload_action:
            self.refresh_page()

    def handle_fs(self, request: QWebEngineFileSystemAccessRequest):
        request.deny()

    def add_new_tab(self, qurl):
        if not isinstance(qurl, QUrl):
            if self.default_new_tab_enabled:
                qurl = QUrl(self.new_tab_url)
            else:
                qurl = QUrl('https://tudify.co.uk/simpleweb/newtab.htm')

        browser = QWebEngineView()
        trackme_not_active = self.TrackMeNot_enabled()
        if trackme_not_active:
            profile = QWebEngineProfile(parent=browser)
        else:
            profile = QWebEngineProfile.defaultProfile()
        page = QWebEnginePage(profile, browser)
        browser.setPage(page)
        page.fullScreenRequested.connect(self.handle_fullscreen_request)
        page.certificateError.connect(self.handle_cert_error)
        page.permissionRequested.connect(self.handle_permission)
        page.fileSystemAccessRequested.connect(self.handle_fs)
        browser.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        browser.customContextMenuRequested.connect(self.sw_context_menu)
        settings = browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setFontFamily(QWebEngineSettings.FontFamily.StandardFont, font_name)    
        profile.setHttpUserAgent(UserAgent)
        profile.setHttpCacheMaximumSize(10240)
        browser.page().titleChanged.connect(lambda title: self.update_tab_title(browser))
        browser.setUrl(qurl)
        self.tabs.addTab(browser, qurl.toString())
        self.tabs.setCurrentWidget(browser)
        # MARK: Attribute Setter
        if trackme_not_active:
            print("TrackMeNot is enabled: Applying strict privacy settings.")
            profile.downloadRequested.connect(self.on_downloadRequested)
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
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        else:
            print("TrackMeNot is disabled: Applying standard privacy settings.")
            profile.downloadRequested.connect(self.on_downloadRequested)
            profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
            profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            try:
                if self.chromium_spoofer.chromium_spoofer_enabled():
                    profile.setHttpUserAgent(ChromiumUserAgent)
                    print("UA: " + ChromiumUserAgent)
                else:
                    profile.setHttpUserAgent(UserAgent)
                    print("UA: " + UserAgent)
            except Exception as e:
                profile.setHttpUserAgent(UserAgent)
                print("UA: " + UserAgent)
                print(f"error in chromiumspoofer, falling back! {e}")

        if not trackme_not_active:
            self.channel = QWebChannel(browser.page())
            # Expose the API object to JavaScript pages. Pass `self` so the API
            # has a reference to the main window (used by setWindowTitle etc.).
            self.api = SimpleWebAPI(self)
            # Register under several common names so pages can find it reliably.
            self.channel.registerObject("SimpleWeb", self.api)
            self.channel.registerObject("SimpleWebAPI", self.api)
            self.channel.registerObject("simpleweb", self.api)
            self.channel.registerObject("simplewebapi", self.api)
            browser.page().setWebChannel(self.channel)

    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        title = browser.title()
        if title:
            self.tabs.setTabText(index, title)
        else:
            self.tabs.setTabText(index, "no title")
    # MARK: Permission handler
    def handle_permission(self, permission: QWebEnginePermission):
        interactive_permissions = {
            QWebEnginePermission.PermissionType.MediaAudioCapture,
            QWebEnginePermission.PermissionType.MediaVideoCapture,
            QWebEnginePermission.PermissionType.MediaAudioVideoCapture,
            QWebEnginePermission.PermissionType.Geolocation,
            QWebEnginePermission.PermissionType.DesktopAudioVideoCapture,
            QWebEnginePermission.PermissionType.DesktopVideoCapture,
        }
        perm_type = permission.permissionType()
        if perm_type not in interactive_permissions:
            permission.deny()
            return

        reply = QMessageBox.question(
            self,
            "Permission Request",
            "This website is requesting access to microphone/camera, screen sharing, or location data. Allow?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            permission.grant()
        else:
            permission.deny()


# MARK: Other Misc. Handling

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        if (current_index != -1):
            self.tabs.removeTab(current_index)
            print(f"EXIT: Reason - Tab count is ({self.tabs.count()})")
            if self.tabs.count() == 0: sys.exit()

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.finished.connect(self.handle_settings_closed)
        self.settings_window.show()

    def update_ai_sidebar_url(self):
        ai_services = {
            "ChatGPT": "https://chat.openai.com/",
            "Amanda AI 2": "https://poe.com/Amanda-AI/",
            "Nora AI": "https://tudify.co.uk/Luna-AI/",
            "Claude": "https://claude.ai/",
            "Gemini": "https://gemini.google.com/"
        }
        ai_url = ai_services.get(self.AI_service, "https://chat.openai.com/")
        ai_instance = self.extension_instances.get("AIsidebar")
        if ai_instance and ai_instance.ai_browser:
            ai_instance.ai_browser.setUrl(QUrl(ai_url))

    def handle_settings_closed(self, result):
        if result == QDialog.DialogCode.Accepted:
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

    def on_downloadRequested(self, download: QWebEngineDownloadRequest):
        suggested = download.suggestedFileName() or download.downloadFileName()
        default_name = suggested or "download.zip"
        path, _ = QFileDialog.getSaveFileName(self, "Save File", default_name,
                                             "All Files (*)")
        if not path:
            download.cancel()
            return
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        download.setDownloadDirectory(directory)
        download.setDownloadFileName(filename)
        download.accept()

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

    def handle_cert_error(self, error):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl("https://tudify.co.uk/simpleweb/cert.htm"))
        else:
            pass

    def handle_fullscreen_request(self, request: QWebEngineFullScreenRequest):
        if request.toggleOn():
            self.toggle_tab_bar()
            self.showFullScreen()
            request.accept()
        else:
            self.toggle_tab_bar()
            self.showNormal()
            request.accept()

settings = QSettings("Tudify", "SimpleWeb")
Search_engine = settings.value("search_engine", "Google")
if Search_engine == "Google": Search_URL = "https://www.google.com/search?q="
elif Search_engine == "DuckDuckGo": Search_URL = "https://duckduckgo.com/?q="
elif Search_engine == "Bing": Search_URL = "https://www.bing.com/search?q="
else: Search_URL = Search_engine = "Google"

cpuname = platform.processor()
os_name = platform.system()
arch = platform.architecture()

def menubar(parent: BrowserWindow):
    if os_namereport == "macOS":
        menu_bar = QMenuBar(parent)
        app_menu = menu_bar.addMenu("SimpleWeb")
        about_action = QAction("About SimpleWeb", parent)
        about_action.triggered.connect(lambda: About(parent).exec())
        about_qtaction = QAction("About Qt", parent)
        about_qtaction.triggered.connect(lambda: app.aboutQt())
        quit_action = QAction("Quit SimpleWeb", parent)
        quit_action.triggered.connect(parent.close)
        Settings_action = QAction("Settings", parent)
        Settings_action.setShortcut("Ctrl+,")
        Settings_action.triggered.connect(parent.open_settings_window) 
        app_menu.addAction(Settings_action)
        app_menu.addAction(about_action)
        app_menu.addAction(about_qtaction)
        app_menu.addAction(quit_action)
#-----> TABS MENU
        file_menu = menu_bar.addMenu("Tabs")
        new_tab_action = QAction("New Tab", parent)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(lambda: parent.add_new_tab(None))
        file_menu.addAction(new_tab_action)
        close_tab_action = QAction("Close Tab", parent)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(parent.close_current_tab)
        file_menu.addAction(close_tab_action)
#-----> VIEW MENU
        view_menu = menu_bar.addMenu("View")
        tabbar_action = QAction("Toggle Tab Bar", parent)
        tabbar_action.setShortcut("F11")
        tabbar_action.triggered.connect(parent.toggle_tab_bar)
        view_menu.addAction(tabbar_action)
        Debug_action = QAction("Debug", parent)
        Debug_action.triggered.connect(lambda: parent.debugwin.show()) 
        view_menu.addAction(Debug_action)
        about_SWEaction = QAction("SW Engine Info", parent)
        about_SWEaction.triggered.connect(lambda: AboutSWE(parent).exec())
        view_menu.addAction(about_SWEaction)
#-----> HELP MENU
        help_menu = menu_bar.addMenu("Help")
        doc_action = QAction("View Documentation", parent)
        doc_action.triggered.connect(lambda: parent.docs("https://github.com/Tudify/SimpleWeb/blob/main/README.md"))
        help_menu.addAction(doc_action)

        parent.setMenuBar(menu_bar)

def getinfo():
    base_dir = Path(__file__).resolve().parent
    info_path = base_dir / "info.json"
    if info_path.exists():
        try:
            with info_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            app = QApplication(sys.argv)
            msg = QMessageBox()
            msg.setWindowTitle("Fatal Error")
            msg.setText(
                "Fatal Error\n\n"
                "SimpleWeb's internal files are damaged and cannot be used. \n"
                "Please Reinstall SimpleWeb. (7)"
            )
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            raise TypeError(f"info.json is malformed or corrupted. {e}")
    else:
        app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setWindowTitle("Fatal Error")
        msg.setText(
            "SimpleWeb is missing one or more critical components." # noob mistake
            "info.json (6)"
        )
        msg.exec()
        raise FileNotFoundError("info.json must be in the same directory!")
    
_info = getinfo()
name = _info.get("name", "null")
builtonIDE = _info.get("ide", "null")
EngineName = _info.get("engine", "null")
EngineVer = _info.get("version", "null")
APIver = "1.0.4" 
mem = round(psutil.virtual_memory().total / (1024 ** 3), 1)

if os_name in ("Darwin", "macOS", "Mac", "Mac OS X"):
    macver = platform.mac_ver()[0].replace('.', '_')
    if cpuname == "arm":
        os_namefinal = "Macintosh; Apple Silicon Mac OS X " + macver
    else:
         os_namefinal = "Macintosh; Intel Mac OS X " + macver
    os_namereport = "macOS"
if os_name == "Linux":
    os_namefinal = "X11; Linux " + arch[0]
    os_namereport = "Linux"
if os_name.startswith("Windows"):
    winver = platform.win32_ver()[0]
    if winver == 'XP':
        WinNT = "5.1"
    elif winver == 'Vista':
        WinNT = "6.0"
    elif winver == '7':
        WinNT = "6.1"
    elif winver == '8':
        WinNT = "6.2"
    elif winver == '8.1':
        WinNT = "6.3"
    elif winver == '10':
        WinNT = "10.0"
    os_namefinal = f"Windows NT {WinNT}; Win64; x64"
    os_namereport = f"Windows {winver}"

print(f"SimpleWeb V{EngineVer} running on: {os_namereport} {arch[0]} with {mem} GB RAM, built with {builtonIDE}")

if cpuname == "arm" and os_namereport == "macOS":
    cpunamefinal = "Apple Silicon"
elif cpuname != "arm" and os_namereport == "macOS":
    cpunamefinal = "Intel"
else:
    cpunamefinal = "x86_64"
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
    f"Chromium/142.0 Safari/605.1.15"
)

font_name = getinfo().get("font", "Hack")
current_theme = darkdetect.theme()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("SimpleWeb")
    app.setApplicationVersion(getinfo().get("version"))
    app.setApplicationDisplayName("SimpleWeb")
    app.setOrganizationName("Tudify")
    if os_namereport == "macOS":
        app.setStyle("Aqua")
    else:
        pass
    window = BrowserWindow()
    updater.check_for_update()
    window.show()
    sys.exit(app.exec())
