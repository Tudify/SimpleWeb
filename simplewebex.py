from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDockWidget, QTextEdit
from PyQt6.QtCore import Qt, QSettings, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
import platform, json
from pathlib import Path

class SimpleWeb:
    class AIsidebar:
        Shortcut = "ctrl+I"
        
        def __init__(self, parent, ai_service="ChatGPT"):
            self.parent = parent
            self.AI_service = ai_service
            self.ai_sidebar = None
            self.ai_browser = None
            
        def toggle_ai_sidebar(self):
            if not self.is_ai_sidebar_enabled():
                return
            
            if self.ai_sidebar is None:
                self.create_ai_sidebar()
            
            if self.ai_sidebar.isVisible():
                self.ai_sidebar.hide()
            else:
                self.ai_sidebar.show()

        def is_ai_sidebar_enabled(self):
            settings = QSettings("Tudify", "SimpleWeb-Extensions")
            return settings.value("AI sidebar [beta] (ctrl + I)", False, type=bool)

        def create_ai_sidebar(self):
            if self.ai_sidebar is not None:
                return

            self.ai_sidebar = QDockWidget(self.parent)
            self.ai_sidebar.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)

            self.ai_browser = QWebEngineView()
            ai_services = {
                "Nora AI": "https://tudify.co.uk/Luna-AI/",
                "ChatGPT": "https://chat.openai.com/",
                "Amanda AI 2": "https://poe.com/Amanda-AI/",
                "Claude": "https://claude.ai/",
                "Gemini": "https://gemini.google.com/"
            }

            ai_url = ai_services.get(self.AI_service, "https://chat.openai.com/")
            self.ai_browser.setUrl(QUrl(ai_url))
            self.ai_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            self.ai_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            self.ai_sidebar.setWidget(self.ai_browser)

            self.parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.ai_sidebar)
            self.ai_sidebar.hide()

            title_widget = QWidget()
            layout = QHBoxLayout(title_widget)
            layout.setContentsMargins(5, 0, 5, 0)
            layout.addWidget(QLabel("AI Sidebar"))
            layout.addStretch()
            title_widget.setStyleSheet("""
                background-color: #292c30;
                color: #ffffff;
                font-weight: bold;
                padding: 4px;
            """)
            self.ai_sidebar.setTitleBarWidget(title_widget)

    class QuickNotes:
        Shortcut = "ctrl+N"
        
        def __init__(self, parent, theme="light"):
            self.parent = parent
            self.theme = theme
            self.quick_notes_sidebar = None
            self.notes_editor = None

        def toggle_quick_notes_sidebar(self):
            if not self.is_quick_notes_enabled():
                return

            if self.quick_notes_sidebar is None:
                self.create_quick_notes_sidebar()

            if self.quick_notes_sidebar.isVisible():
                self.quick_notes_sidebar.hide()
            else:
                self.quick_notes_sidebar.show()

        def is_quick_notes_enabled(self):
            settings = QSettings("Tudify", "SimpleWeb-Extensions")
            return settings.value("Quick Notes (ctrl + N)", False, type=bool)
            
        def create_quick_notes_sidebar(self):
            self.quick_notes_sidebar = QDockWidget(self.parent)
            self.quick_notes_sidebar.setAllowedAreas(
                Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea
            )

            self.notes_editor = QTextEdit()
            self.notes_editor.setPlaceholderText("Type your notes here...")
            self.notes_editor.setStyleSheet(self.get_quick_notes_stylesheet())

            self.quick_notes_sidebar.setWidget(self.notes_editor)
            self.parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.quick_notes_sidebar)
            self.quick_notes_sidebar.hide()

            title_widget = QWidget()
            layout = QHBoxLayout(title_widget)
            layout.setContentsMargins(5, 0, 5, 0)
            layout.addWidget(QLabel("Quick Notes"))
            layout.addStretch()

            if self.theme.lower() == "dark":
                title_widget.setStyleSheet("""
                    background-color: #292c30;
                    color: #ffffff;
                    font-weight: bold;
                    padding: 4px;
                """)
            else:
                title_widget.setStyleSheet("""
                    background-color: #f0f0f0;
                    color: #000000;
                    font-weight: bold;
                    padding: 4px;
                """)

            self.quick_notes_sidebar.setTitleBarWidget(title_widget)

        def get_quick_notes_stylesheet(self):
            if self.theme.lower() == "dark":
                return """
                    QTextEdit {
                        background-color: #292c30;
                        color: #ffffff;
                        font-family: hack, consolas, monospace;
                        font-size: 14px;
                        padding: 10px;
                    }
                """
            else:
                return """
                    QTextEdit {
                        background-color: #f0f0f0;
                        color: #000000;
                        font-family: hack, consolas, monospace;
                        font-size: 14px;
                        padding: 10px;
                    }
                """

    class QuickResearch:
        Shortcut = "ctrl+O"
        
        def __init__(self, parent):
            self.parent = parent
            self.quick_research_sidebar = None
            
        def is_quick_research_enabled(self):
            settings = QSettings("Tudify", "SimpleWeb-Extensions")
            return settings.value("Quick Research (ctrl + O)", False, type=bool)
        
        def create_quick_research_sidebar(self):
            self.quick_research_sidebar = QDockWidget(self.parent)
            self.quick_research_sidebar.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)
            self.quick_research_browser = QWebEngineView()
            self.quick_research_browser.setUrl(QUrl("https://tudify.co.uk/Luna-AI/research/"))
            self.quick_research_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            self.quick_research_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            self.quick_research_sidebar.setWidget(self.quick_research_browser)
            self.parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.quick_research_sidebar)
            self.quick_research_sidebar.hide()
            
            title_widget = QWidget()
            layout = QHBoxLayout(title_widget)
            layout.setContentsMargins(5, 0, 5, 0)
            title_label = QLabel("[AI] Quick Research")
            layout.addWidget(title_label)
            layout.addStretch()
            title_widget.setStyleSheet("""
                background-color: #292c30;
                color: #ffffff;
                font-weight: bold;
                padding: 4px;
            """)
            self.quick_research_sidebar.setTitleBarWidget(title_widget)

        def toggle_quick_research_sidebar(self):
            if not self.is_quick_research_enabled():
                return

            if self.quick_research_sidebar is None:
                self.create_quick_research_sidebar()

            if self.quick_research_sidebar.isVisible():
                self.quick_research_sidebar.hide()
            else:
                self.quick_research_sidebar.show()

    class ChromiumSpoofer:
        Shortcut = "none"
        
        def __init__(self, parent):
            self.parent = parent
            
        def chromium_spoofer_enabled(self):
            settings = QSettings("Tudify", "SimpleWeb-Extensions")
            return settings.value("Chromium Spoofer [alpha]", False, type=bool)

        def apply_chromium_spoofer(self):
            try:
                from PyQt6.QtWebEngineCore import QWebEngineProfile
                profile = QWebEngineProfile.defaultProfile()
                if self.chromium_spoofer_enabled():
                    profile.setHttpUserAgent(ChromiumUserAgent)
                    print("Chromium Spoofer enabled")
                else:
                    profile.setHttpUserAgent(UserAgent)
            except Exception as e:
                print("apply_chromium_spoofer error:", e)

    class MusicSidebar:
        Shortcut = "ctrl+M"
        def __init__(self, parent):
            self.app_settings = QSettings("Tudify", "SimpleWeb")
            self.music_service = self.app_settings.value("music_service", "Spotify") 
            self.parent = parent
            self.music_sidebar = None
            self.music_browser = None

        def toggle_ai_sidebar(self):
            if not self.is_music_sidebar_enabled():
                return
            
            if self.music_sidebar is None:
                self.create_music_sidebar()
            
            if self.music_sidebar.isVisible():
                self.music_sidebar.hide()
            else:
                self.music_sidebar.show()

        def is_music_sidebar_enabled(self):
            settings = QSettings("Tudify", "SimpleWeb-Extensions")
            return settings.value("Music sidebar (ctrl + M)", False, type=bool)

        def create_music_sidebar(self):
            if self.music_sidebar is not None:
                return

            self.music_sidebar = QDockWidget(self.parent)
            self.music_sidebar.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)

            self.music_browser = QWebEngineView()

            music_services = {
                "Spotify": "https://open.spotify.com",
                "Apple Music": "https://music.apple.com/",
                "Amazon Music": "https://music.amazon.com/",
                "Youtube Music": "https://music.youtube.com/",
                "Tidal": "https://tidal.com"
            }

            ai_url = music_services.get(self.music_service, "https://open.spotify.com/")
            self.music_browser.setUrl(QUrl(ai_url))
            self.music_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            self.music_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            self.music_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
            self.music_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
            self.music_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
            self.music_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
            self.music_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            self.music_sidebar.setWidget(self.music_browser)

            self.parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.music_sidebar)
            self.music_sidebar.hide()

            title_widget = QWidget()
            layout = QHBoxLayout(title_widget)
            layout.setContentsMargins(5, 0, 5, 0)
            layout.addWidget(QLabel("Music Sidebar"))
            layout.addStretch()
            title_widget.setStyleSheet("""
                background-color: #292c30;
                color: #ffffff;
                font-weight: bold;
                padding: 4px;
            """)
            self.music_sidebar.setTitleBarWidget(title_widget)

        def refresh_page(self):
            if self.music_sidebar is None:
                self.create_music_sidebar()
            else:
                print("Ok vro")

            music_services = {
                "Spotify": "https://open.spotify.com",
                "Apple Music": "https://music.apple.com/",
                "Amazon Music": "https://music.amazon.com/",
                "Youtube Music": "https://music.youtube.com/",
                "Tidal": "https://tidal.com"
            }

            ai_url = music_services.get(self.music_service, "https://open.spotify.com/")
            self.music_browser.setUrl(QUrl(ai_url))




# Keep backward compatibility
AISideBar = SimpleWeb.AIsidebar
QuickNotes = SimpleWeb.QuickNotes
QuickResearch = SimpleWeb.QuickResearch
ChromiumSpoofer = SimpleWeb.ChromiumSpoofer



@staticmethod
def getinfo():
    base_dir = Path(__file__).resolve().parent
    info_path = base_dir / "info.json"
    if info_path.exists():
        try:
            with info_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to read {info_path.name}: {e}")
            return {}
    else:
        print("info.json not found!")
        return {}
    
name = getinfo().get("name", "unknown") # SimpleCode Internal 1.0 hits harder
EngineName = getinfo().get("engine", "Unknown")
EngineVer = getinfo().get("version", "Unknown")
cpuname = platform.processor()
os_name = platform.system()
arch = platform.architecture()

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

UserAgent = (
    f"Mozilla/5.0 ({os_namefinal}) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    f"{EngineName}/{EngineVer} Safari/605.1.15"
)

ChromiumUserAgent = (
    f"Mozilla/5.0 ({os_namefinal}) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    f"Chromium/141.0 Safari/605.1.15"
)