import sys, subprocess ,time, os, urllib.request, urllib.error, platform #AHHH
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QAction, QMenu, QMenuBar,QFileDialog, QShortcut, QMessageBox, QDialog, QLabel, QPlainTextEdit, QDialogButtonBox, QComboBox, QCheckBox, QSplashScreen)
os_name = platform.system()
from PyQt5.QtCore import QUrl, Qt, QSettings, QTimer, QEvent
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile

EngineName = "SWE-Multiplatform"
EngineVer = "3.0"
UserAgent = EngineName + " " + EngineVer + " / " + os_name


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
            *{font-family: hack, arial;}
            """)
        
        layout = QVBoxLayout()

        # Big heading
        self.heading_label = QLabel("Settings")
        self.heading_label.setObjectName("heading")
        layout.addWidget(self.heading_label, alignment=Qt.AlignLeft)

        # New tab URL
        self.new_tab_url_label = QLabel("New Tab URL:")
        layout.addWidget(self.new_tab_url_label)

        self.new_tab_url_edit = QLineEdit()
        layout.addWidget(self.new_tab_url_edit)

        # Default new tab checkbox
        self.default_new_tab_checkbox = QCheckBox("Open new tabs with default URL")
        layout.addWidget(self.default_new_tab_checkbox)

        # Theme selection
        self.theme_label = QLabel("Choose your theme:")
        layout.addWidget(self.theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        layout.addWidget(self.theme_combo)

        self.load_settings()

        # Add some space before buttons
        layout.addSpacing(20)

        # Buttons
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
        self.setWindowTitle("Tudify SimpleWeb")
        self.setGeometry(300, 100, 1000, 600)
        self.setWindowIcon(QIcon("ICO.png"))
        self.refresh_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.refresh_shortcut.activated.connect(self.refresh_page)
        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(self.close_current_tab)
        self.shortcut_new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_new_tab.activated.connect(self.open_default_new_tab)
        self.shortcut_url_popup = QShortcut(QKeySequence("Ctrl+U"), self)
        self.shortcut_url_popup.activated.connect(self.toggle_url_popup)
        self.load_settings()
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
        print("Setup saved")

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
        if source is self.url_popup and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.url_popup.clear()
                self.url_popup.hide()
                return True
        return super().eventFilter(source, event)

    def handle_quick_url(self, *args):
        text = self.url_popup.text().strip()
        if not text:
            self.url_popup.hide()
            return

        url_to_load = None

        # Handle Tudify commands
        if text.startswith('tudify://'):
            if text in ('tudify://settings', 'tudify://setup', 'tudify://set', 'tudify://config'):
                self.open_settings_window()
                self.url_popup.clear()
                self.url_popup.hide()
                return
            elif text == 'tudify://newtab':
                url_to_load = 'https://tudify.co.uk/simpleweb/newtab.htm'
            else:
                print("Unknown tudify command:", text)
                url_to_load = 'https://tudify.co.uk/simpleweb/404/'

        # Handle search / incomplete URL
        elif not text.startswith(('http://', 'https://')):
            if '.' not in text:  # assume search
                url_to_load = f'https://www.google.com/search?q={text}'
            else:
                url_to_load = 'https://' + text  # let QWebEngineView handle unreachable URLs

        else:  # treat as HTTPS URL
            url_to_load = 'https://' + text
            try:
                urllib.request.urlopen(url_to_load, timeout=5)
            except Exception:
                url_to_load = 'https://tudify.co.uk/simpleweb/404/'


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
        style_dark = """
            *{font-family: hack, arial;}
            QMainWindow {
                background-color: #202326;
                color: #ffffff;
            }
            QPushButton {
                background-color: #292c30;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #414346;
            }
            QPushButton:hover {
                background-color: #292c30;
                border: 1px solid #0a6cff;
            }
            QLineEdit {
                background-color: #292c30;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #414346;
            }
            QLineEdit:focus {
                background-color: #292c30;
                border: 1px solid #0a6cff;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #292c30;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #414346;
            }
            QTabBar::tab:selected {
                background-color: #292c30;
                border: 1px solid #0a6cff;
            }
        """

        style_light = """
            *{font-family: hack;}
            QMainWindow {
                background-color: #f5f5f5;
                color: #000000;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                padding: 10px 16px;
                border-radius: 6px;
                border: 1px solid #cccccc;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
                padding: 10px;
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #000000;
                padding: 8px 20px;
                border-radius: 6px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background-color: #c0c0c0;
            }
        """

        theme = theme.lower()
        if theme == "dark":
            self.setStyleSheet(style_dark)
        elif theme == "light":
            self.setStyleSheet(style_light)
        else:
            self.setStyleSheet(style_light)
    
        # Fix + button in the corner
        if hasattr(self, 'tabs') and hasattr(self, 'new_tab_button'):
            self.new_tab_button.setFixedSize(50, 50)
            self.new_tab_button.setStyleSheet("""
                QPushButton {
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 16px
                }
            """)


    def error(self, parent):
        print("not finished")
        sys.exit()

    def create_tab_widget(self):
        self.tabs = QTabWidget()
        self.tabs.tabCloseRequested.connect(lambda index: self.tabs.removeTab(index))

        # Create buttons
        self.back_button = QPushButton('⏴')
        self.back_button.setFixedSize(40, 35)
        self.back_button.clicked.connect(self.go_back)

        self.new_tab_button = QPushButton('+')
        self.new_tab_button.setFixedSize(40, 35)
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab(QUrl(self.new_tab_url)))

        # Make a small container for both buttons
        corner_widget = QWidget()
        corner_layout = QHBoxLayout(corner_widget)
        corner_layout.setContentsMargins(0, 0, 0, 0)
        corner_layout.setSpacing(4)
        corner_layout.addWidget(self.back_button)
        corner_layout.addWidget(self.new_tab_button)

        # Put the container in the top-right corner of the tab bar
        self.tabs.setCornerWidget(corner_widget, Qt.TopRightCorner)

        self.central_layout.addWidget(self.tabs)

        # Add the first tab
        self.add_new_tab(QUrl('https://tudify.co.uk/SimpleWeb/newtab.htm'))


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
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, False)

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(UserAgent)
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

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
    def create_main_window(self, splash):
        print("main window was created.")
        main_window = BrowserWindow()
        main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())