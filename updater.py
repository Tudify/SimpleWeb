# Copyright (c) 2025 tudify
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

"""Fuckin updater bro"""
import json, sys, webbrowser, ssl
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMessageBox, QPushButton)
from urllib.request import urlopen

UPDATE_URL = "https://tudify.co.uk/update/simpleweb.txt"
RELEASES_URL = "https://github.com/tudify/simpleweb/releases"

def load_local_version_numeric():
    info_path = Path.home() / ".SimpleWeb/info.json"
    print(info_path)
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
        ctx = ssl._create_unverified_context()
        with urlopen(UPDATE_URL, context=ctx) as response:
            remote_text = response.read().decode().strip()
            remote_version = int(remote_text.replace(".", ""))
            print(f"Latest Version Available: {remote_text}")
            print(f"Parsed As: {remote_version}")
    except Exception as e:
        print(f"Failed to fetch remote version: {e}")
        return

    if remote_version > local_version:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.icon.Information)
        msg.setWindowTitle("Update Available")
        msg.setText(f"A new version is available!\n"
                    f"Would you like to download it?")
        # Download Update button
        update_button = QPushButton("Download Update")
        update_button.clicked.connect(lambda: webbrowser.open(RELEASES_URL))
        msg.addButton(update_button, QMessageBox.ActionRole)
        later_button = QPushButton("Later")
        msg.addButton(later_button, QMessageBox.RejectRole)
        
        msg.exec()
    else:
        print("No update available.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    check_for_update()
    sys.exit(0)