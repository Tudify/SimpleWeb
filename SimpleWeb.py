import sys, subprocess ,time, os, urllib.request, urllib.error,platform #AHHH
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTabWidget, QAction, QMenu, QMenuBar,QFileDialog, QShortcut, QMessageBox,
    QDialog, QLabel, QPlainTextEdit, QDialogButtonBox, QComboBox, QCheckBox, QSplashScreen
)
from PyQt5.QtCore import QUrl, Qt, QSettings, QTimer
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        SettingsWindow.set_stylesheet(self.theme)
        self.setWindowTitle("Settings - SimpleWeb")
        self.setGeometry(300, 100, 300, 200)

        layout = QVBoxLayout()
        self.set_stylesheet(self.theme)

        self.new_tab_url_label = QLabel("New Tab URL:")
        layout.addWidget(self.new_tab_url_label)

        self.new_tab_url_edit = QLineEdit()
        layout.addWidget(self.new_tab_url_edit)

        self.default_new_tab_checkbox = QCheckBox("Open new tabs with default URL")
        layout.addWidget(self.default_new_tab_checkbox)

        self.theme_label = QLabel("Make SimpleWeb yours:")
        layout.addWidget(self.theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Midnight", "Luxe"])
        layout.addWidget(self.theme_combo)

        self.load_settings()
          
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def load_settings(self):
        settings = QSettings("Tudify", "Simpleweb")
        self.new_tab_url_edit.setText(settings.value("new_tab_url", "https://tudify.co.uk/simpleweb/newtab.htm"))
        self.theme_combo.setCurrentText(settings.value("theme", "Dark"))

        default_new_tab_checked = settings.value("default_new_tab_checked", False)
        self.default_new_tab_checkbox.setChecked(default_new_tab_checked == "true")

    def save_settings(self):
        settings = QSettings("Tudify", "Simpleweb")
        settings.setValue("new_tab_url", self.new_tab_url_edit.text())
        settings.setValue("theme", self.theme_combo.currentText())
        settings.setValue("default_new_tab_checked", "true" if self.default_new_tab_checkbox.isChecked() else "false")

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("theme_dark")
        self.setWindowTitle("Settings - SimpleWeb")
        self.setGeometry(300, 100, 300, 200)

        layout = QVBoxLayout()

        self.new_tab_url_label = QLabel("New Tab URL:")
        layout.addWidget(self.new_tab_url_label)

        self.new_tab_url_edit = QLineEdit()
        layout.addWidget(self.new_tab_url_edit)

        self.default_new_tab_checkbox = QCheckBox("Open new tabs with default URL")
        layout.addWidget(self.default_new_tab_checkbox)

        self.theme_label = QLabel("Make SimpleWeb yours:")
        layout.addWidget(self.theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Midnight", "Luxe"])
        layout.addWidget(self.theme_combo)

        self.load_settings()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def load_settings(self):
        settings = QSettings("Tudify", "Simpleweb")
        self.new_tab_url_edit.setText(settings.value("new_tab_url", "https://tudify.co.uk/simpleweb/newtab.htm"))
        self.theme_combo.setCurrentText(settings.value("theme", "Dark"))

        default_new_tab_checked = settings.value("default_new_tab_checked", False)
        self.default_new_tab_checkbox.setChecked(default_new_tab_checked == "true")

    def save_settings(self):
        settings = QSettings("Tudify", "Simpleweb")
        settings.setValue("new_tab_url", self.new_tab_url_edit.text())
        settings.setValue("theme", self.theme_combo.currentText())
        settings.setValue("default_new_tab_checked", "true" if self.default_new_tab_checkbox.isChecked() else "false")

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tudify SimpleWeb") # 2017- to change soon #2024- soon my ass
        self.setGeometry(300, 100, 1000, 600)
        self.TDFMENU()  # Call the method to set up the menu

        print("Tudify Simpleweb")
        print("Version 2.0")
        print("UserAgent= Tudify SimpleWebEngine 2.0")
        print("No data in the console is transmitted to, or saves to any online services or servers.")

        self.setWindowIcon(QIcon("ICO.png"))  # Set window icon to ICO.png
        print("icon loaded")

        self.splash = QSplashScreen(QPixmap("splash.png"))  # Replace "splash.png" with your splash screen image
        print("splash screen loaded")

        self.load_settings()
        self.set_stylesheet(self.theme)
        print("Theme loaded")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)

        self.create_top_bar()
        self.create_tab_widget()

        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(self.close_current_tab)

        self.shortcut_new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_new_tab.activated.connect(self.open_default_new_tab)

        self.load_favorites()

        QTimer.singleShot(0, self.show_splash)  # Show splash screen immediately
        print("splash screen displayed")
        QTimer.singleShot(3200, self.hide_splash)  # Hide splash screen after 2 seconds (adjust as needed)
        print("splash screen closed")

    def show_splash(self):
        self.splash.show()

    def hide_splash(self):
        self.splash.finish(self)

    def open_default_new_tab(self):
        if self.default_new_tab_enabled:
            self.add_new_tab(QUrl(self.new_tab_url))
        else:
            self.add_new_tab(QUrl('https://tudify.co.uk/SimpleWeb/newtab.htm'))

    def load_settings(self):
        settings = QSettings("MyCompany", "MyApp")
        self.new_tab_url = settings.value("new_tab_url", "https://tudify.co.uk/simpleweb/newtab.htm")
        self.theme = settings.value("theme", "dark")
        self.default_new_tab_enabled = settings.value("default_new_tab_checked", False)

    def save_settings(self):
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("new_tab_url", self.new_tab_url)
        settings.setValue("theme", self.theme)
        settings.setValue("default_new_tab_checked", self.default_new_tab_enabled)
        print("setup saved")


    def set_stylesheet(self, theme):
        style_dark = """
            QMainWindow {
                background-color: #222;
                color: white;
            }
            QPushButton, QLineEdit {
                background-color: #555;
                color: white;
                padding: 12px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QLineEdit {
                background-color: #444;
                border: 1px solid #666;
                padding: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #00BFFF;
            }
        """
        style_light = """
            QMainWindow {
                background-color: #f0f0f0;
                color: black;
            }
            QPushButton, QLineEdit {
                background-color: #ddd;
                color: black;
                padding: 12px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ccc;
            }
            QLineEdit {
                background-color: #eee;
                border: 1px solid #ccc;
                padding: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #00BFFF;
            }
        """
        style_midnight = """
            QMainWindow {
                background-color: #000;
                color: white;
            }
            QPushButton, QLineEdit {
                background-color: #333;
                color: white;
                padding: 12px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QLineEdit {
                background-color: #222;
                border: 1px solid #444;
                padding: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #00BFFF;
            }
        """
        style_Luxe = """
            QMainWindow {
                background-color: #202;
                color: white;
            }
            QPushButton, QLineEdit {
                background-color: #101;
                color: white;
                padding: 12px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #001;
            }
            QLineEdit {
                background-color: #000;
                border: 1px solid #001;
                padding: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #003;
            }
        """

        
        if theme == "luxe":
            self.setStyleSheet(style_Luxe)
            print("stylesheet set to", theme)
        if theme == "dark":
            self.setStyleSheet(style_dark)
            print("stylesheet set to", theme)
        elif theme == "light":
            self.setStyleSheet(style_light)
            print("stylesheet set to", theme)
        elif theme == "midnight":
            self.setStyleSheet(style_midnight)
            print("stylesheet set to", theme)
        else:
            self.setstylesheet(style_dark)

    

    def TDFMENU(self):
        # Create the menu bar

        menubar = self.menuBar()

        # Create "Webpage" menu
        webpage_menu = menubar.addMenu('Webpage')
        
        # Add actions to the "Webpage" menu
        back_webpage_action = QAction('view page source', self)
        back_webpage_action.triggered.connect(self.error)

        webpage_menu.addAction(back_webpage_action)

        # Add actions to the "Webpage" menu
        src_webpage_action = QAction('Back\t⌘b', self)
        src_webpage_action.triggered.connect(self.go_back)
        src_webpage_action.setShortcut(QKeySequence("Command+B") if platform.system() == 'Darwin' else QKeySequence("Ctrl+B"))

        webpage_menu.addAction(src_webpage_action)

        # Create "File" menu
        file_menu = menubar.addMenu('File')
        

        # Add actions to the "File" menu
        add_action = QAction('Refresh\t⌘R', self)
        add_action.triggered.connect(self.refresh_page)
        file_menu.addAction(add_action) 

        # Add actions to the "File" menu
        open_action = QAction('Split screen', self)
        open_action.triggered.connect(self.create_tab_widget)
        file_menu.addAction(open_action)

        save_action = QAction('Close tab\t⌘W' , self)
        save_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(save_action)


    def error(self, parent):
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2934 in TDF_pid_924")
        print("error, bool expected at ln 2932 in TDF_pid_921")
        sys.exit()


    def create_top_bar(self):
        top_bar_layout = QHBoxLayout()

        self.back_button = QPushButton('←')
        self.back_button.clicked.connect(self.go_back)
        top_bar_layout.addWidget(self.back_button)

        self.refresh_button = QPushButton('↻')
        self.refresh_button.clicked.connect(self.refresh_page)
        top_bar_layout.addWidget(self.refresh_button)

        self.favorites_menu = QMenu("Favorites", self)
        self.favorite_actions = []

        self.add_favorite_action = QAction("Favorite this", self)
        self.add_favorite_action.triggered.connect(self.add_to_favorites)
        self.favorites_menu.addAction(self.add_favorite_action)

        self.remove_favorite_action = QAction("Remove this", self)
        self.remove_favorite_action.triggered.connect(self.remove_favorite)
        self.favorites_menu.addAction(self.remove_favorite_action)
        self.favorites_button = QPushButton('★')
        self.favorites_button.setMenu(self.favorites_menu)
        self.favorites_button.setStyleSheet(
            "QPushButton::menu-indicator { image: none; }"
        )
        top_bar_layout.addWidget(self.favorites_button)

        self.url_input = QLineEdit(self)
        self.url_input.setStyleSheet("QLineEdit { padding: 12px; }")
        self.url_input.returnPressed.connect(self.load_url_or_search)
        self.url_input.setMinimumHeight(40)
        top_bar_layout.addWidget(self.url_input)

        self.new_tab_button = QPushButton('+')
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab(QUrl(self.new_tab_url)))
        top_bar_layout.addWidget(self.new_tab_button)

        self.central_layout.addLayout(top_bar_layout)

    def create_tab_widget(self):
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab-bar { alignment: left; }
            QTabBar::tab {
                background-color: #333;
                color: white;
                border-radius: 5px;
                padding: 8px;
                margin-right: 4px;
                margin-bottom: 5px;
            }
            QTabBar::tab:selected { background-color: #555; }
        """)
        self.central_layout.addWidget(self.tabs)

        self.add_new_tab(QUrl('https://tudify.co.uk/SimpleWeb/newtab.htm'))
    def add_new_tab(self, qurl):
        if qurl is None or qurl.isEmpty():
            # Use default new tab URL if the provided URL is empty
            if self.default_new_tab_enabled:
                qurl = QUrl(self.new_tab_url)
            else:
                qurl = QUrl('https://tudify.co.uk/SimpleWeb/newtab.htm')

        # Create a new instance of QWebEngineView
        browser = QWebEngineView()
        settings = browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, False)

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent("Tudify SimpleWebEngine 2.0")
        profile.setHttpCacheMaximumSize(10240)
       

        # Connect signals for updating tab title
        browser.page().titleChanged.connect(lambda title: self.update_tab_title(browser))

        browser.setUrl(qurl)
        self.tabs.addTab(browser, qurl.toString())

        # Ensure the new tab is set as the current widget
        self.tabs.setCurrentWidget(browser)

    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        title = browser.title()
        if title:
            self.tabs.setTabText(index, title)
        else:
            self.tabs.setTabText(index, "New Tab")


    def load_url_or_search(self):
        input_text = self.url_input.text().strip()

        url_to_load = TudifyUrlHandler.handle_url(input_text)
        if not url_to_load:
            self.show_error_message("Invalid Input", "Please enter a valid URL or search term.")
            return

        if url_to_load == 'settings':
            self.open_settings_window()
        else:
            url = QUrl(url_to_load)
            current_browser = self.tabs.currentWidget()
            if current_browser:
                current_browser.setUrl(url)

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        print("Tab closed")
        if (current_index != -1):
            self.tabs.removeTab(current_index)
            if self.tabs.count() == 0:
                print("default tab closed")
                print("tab count is equal to or below 0.")
                sys.exit()


    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.finished.connect(self.handle_settings_closed)
        self.settings_window.show()

    def handle_settings_closed(self, result):
        if result == QDialog.Accepted:
            self.new_tab_url = self.settings_window.new_tab_url_edit.text()
            self.theme = self.settings_window.theme_combo.currentText().lower()
            self.default_new_tab_enabled = self.settings_window.default_new_tab_checkbox.isChecked()
            self.set_stylesheet(self.theme)
            self.save_settings()
            print("settings terminated")

            current_browser = self.tabs.currentWidget()
            if current_browser:
                current_browser.reload()

    def handle_download(self, download_item):
        url = download_item.url().toString()
        print("downloading file class was called")
        file_name = os.path.basename(url)  # Extract file name from URL
        base_name, file_extension = os.path.splitext(file_name)  # Split into base name and extension
        
        # Combine base name and extension
        default_file_name = base_name + file_extension
        
        # Append the file extension to the suggested file name
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

    def add_to_favorites(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            url = current_browser.url().toString()
            title = current_browser.title()

            favorite = {"title": title, "url": url}
            self.favorite_actions.append(favorite)
            self.save_favorites()

            action = QAction(QIcon(), title, self)
            action.setData(url)
            action.triggered.connect(lambda: self.load_url_from_favorite(url))
            self.favorites_menu.addAction(action)

    def load_favorites(self):
        settings = QSettings("MyCompany", "MyApp")
        favorites = settings.value("favorites", [])

        for favorite in favorites:
            action = QAction(QIcon(), favorite["title"], self)
            action.setData(favorite["url"])
            action.triggered.connect(lambda url=favorite["url"]: self.load_url_from_favorite(url))
            self.favorite_actions.append(favorite)
            self.favorites_menu.addAction(action)

    def save_favorites(self):
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("favorites", self.favorite_actions)

    def load_url_from_favorite(self, url):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))

    def remove_favorite(self):
        active_action = self.favorites_menu.activeAction()
        if active_action:
            url_to_remove = active_action.data()
            self.favorite_actions = [fav for fav in self.favorite_actions if fav["url"] != url_to_remove]
            self.favorites_menu.removeAction(active_action)
            self.save_favorites()

            QMessageBox.information(self, "Remove Favorite", "Favorite removed successfully.")

    def view_page_source(self, browser):
        if not hasattr(browser, 'page'):
            print(f"Error: Expected a browser object. Got {type(browser).__name__} instead.")
            raise TypeError("Expected a browser object with a 'page' attribute.")
        browser.page().toHtml(self.handle_page_source)

    def handle_page_source(self, html):
        source_dialog = QDialog(self)
        source_dialog.setWindowTitle("Page Source Viewer")
        layout = QVBoxLayout()
        text_edit = QPlainTextEdit()
        text_edit.setPlainText(html)
        text_edit.setReadOnly(True)  # Make the text edit read-only
        layout.addWidget(text_edit)
        source_dialog.setLayout(layout)
        source_dialog.resize(800, 600)  # Set initial size of the dialog
        source_dialog.exec_()

    def handle_copy_result(self, result):
        clipboard = QApplication.clipboard()
        clipboard.setText(result)

    def handle_fullscreen_request(self, request):
        request.accept()
        if request.toggleOn():
            self.showFullScreen()
        else:
            self.showNormal()

    def show_error_message(self, title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.exec_()

import time
import sys

class TudifyUrlHandler:
    def tdferr(self):
        self.show_warning_message("Invalid Input", "Please enter a valid URL or search term.")
        print('error at ln 529, in TudifyUrlHandler')

    @staticmethod
    def check_url_reachability(url):
        # Function to check if a URL is reachable
        try:
            urllib.request.urlopen(url, timeout=5)
            return True
        except urllib.error.URLError:
            return False

    @staticmethod
    def handle_url(input_text):
        if input_text.startswith('tudify://'):
            if input_text == 'tudify://settings' or \
               input_text == 'tudify://setup' or \
               input_text == 'tudify://set' or \
               input_text == 'tudify://config' or \
               input_text == 'tudify://configuration':
                print("Settings was opened at", time.localtime())
                return 'settings'
            elif input_text == 'tudify://newtab':
                print("Newtab accessed at", time.localtime())
                return 'https://tudify.co.uk/simpleweb/newtab.htm'
            elif input_text == 'tudify://incognito':
                print("unknown exception, last found linecall: ln 546, TudifyURLhandler was told to ignore request and close app.")
                time.sleep(4)
                print("SERIOUS EXCEPTION: APP MUST CLOSE!")
                sys.exit()
            else:
                print("Unknown tudify command:", input_text)
                return 'https://tudify.co.uk/simpleweb/404/'

        if not input_text.startswith(('http://', 'https://')):
            if '.' not in input_text:
                print("went to url", input_text, "at", time.localtime())
                return f'https://www.google.com/search?q={input_text}'
            else:
                url = 'https://' + input_text
                if TudifyUrlHandler.check_url_reachability(url):
                    print("went to url", input_text, "at", time.localtime())
                    return url
                else:
                    print("failed to return", input_text, "at", time.localtime())
                    return 'https://tudify.co.uk/SimpleWseb/404/'

        url = input_text
        if TudifyUrlHandler.check_url_reachability(url):
            print("went to url", input_text, "at", time.localtime())
            return url
        else:
            print("failed to return", input_text, "at", time.localtime())
            return 'https://tudify.co.uk/SimpleWeb/404/'

# Example usage:
handler = TudifyUrlHandler()
url = handler.handle_url('https://tudify.co.uk/simpleweb/404/')  # Replace with your URL or input
print("Redirecting to:", url)
    
#extra spaceee   
#extra spaceee   
#extra spaceee   
#extra spaceee   
#extra spaceee   
#extra spaceee   
#extra spaceee   
#extra spaceee   
#extra spaceee           

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

    def run(self):
        splash_pix = QPixmap("splash.png")
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.show()
        self.processEvents()

        # Create and show the main window after a delay
        QTimer.singleShot(2000, lambda: self.create_main_window(splash))

    def create_main_window(self, splash):
        print("main window was created.")
        main_window = BrowserWindow()
        main_window.show()
        splash.finish(main_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())

#Alfie - is it finished
#butch - fuck no
#ethan - oh ffs NOOOOOOOO!!!