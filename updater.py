import json, sys, webbrowser
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox, QApplication, QPushButton
from urllib.request import urlopen

UPDATE_URL = "http://tudify.co.uk/update/simpleweb.txt"
RELEASES_URL = "https://github.com/tudify/simpleweb/releases"

def load_local_version_numeric():
    info_path = Path(__file__).resolve().parent / "info.json"
    if not info_path.exists():
        return 0
    try:
        with info_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("version", "0").replace(".", ""))
    except:
        return 0

def check_for_update():
    local_version = load_local_version_numeric()
    try:
        with urlopen(UPDATE_URL) as response:
            remote_text = response.read().decode().strip()
            remote_version = int(remote_text.replace(".", ""))
    except Exception as e:
        print(f"Failed to fetch remote version: {e}")
        return

    if remote_version > local_version:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Update Available")
        msg.setText(f"A new version is available!\n"
                    f"Would you like to download it?")
        # Download Update button
        update_button = QPushButton("Download Update")
        update_button.clicked.connect(lambda: webbrowser.open(RELEASES_URL))
        msg.addButton(update_button, QMessageBox.ActionRole)
        later_button = QPushButton("Later")
        msg.addButton(later_button, QMessageBox.RejectRole)
        
        msg.exec_()
    else:
        print("No update available.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(0)