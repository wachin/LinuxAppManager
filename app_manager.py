import sys
import subprocess
import tempfile
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
    QMessageBox, QTabWidget, QComboBox, QDialog
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QTranslator, QLocale, QLibraryInfo

class AboutDialog(QDialog):
    def __init__(self, parent=None, icon_pixmap=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("About Linux App Manager"))
        self.setFixedSize(450, 250)
        
        layout = QHBoxLayout(self)
        
        # Left side: Icon
        icon_label = QLabel()
        if icon_pixmap and not icon_pixmap.isNull():
            scaled_pixmap = icon_pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Right side: Text info
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        
        title = QLabel("Linux App Manager")
        title.setStyleSheet("font-size: 18pt; font-weight: bold;")
        
        description = QLabel(self.tr("A simple utility to manage default applications and file associations on Linux systems."))
        description.setWordWrap(True)
        
        info = QLabel(
            f"<b>{self.tr('Developer')}:</b> Washington Indacochea Delgado<br>"
            f"<b>{self.tr('Email')}:</b> <a href='mailto:linuxfrontier@proton.me'>linuxfrontier@proton.me</a><br>"
            f"<b>{self.tr('License')}:</b> GPL3<br>"
            f"<b>{self.tr('Technologies')}:</b> Python, PyQt6, XDG Utils"
        )
        info.setOpenExternalLinks(True)
        info.setWordWrap(True)
        
        text_layout.addWidget(title)
        text_layout.addWidget(description)
        text_layout.addWidget(info)
        text_layout.addStretch()
        
        layout.addWidget(text_widget, 1)

class AppManager(QMainWindow):
    def __init__(self):
        super().__init__()
        # Mapping of common categories (English keys for i18n)
        self.COMMON_CATEGORIES = {
            self.tr("File Manager"): {"type": "mime", "value": "inode/directory"},
            self.tr("Web Browser"): {"type": "setting", "value": "default-web-browser"},
            self.tr("Text Editor"): {"type": "mime", "value": "text/plain"},
            self.tr("Email Client"): {"type": "setting", "value": "default-url-scheme-handler", "sub": "mailto"},
            self.tr("PDF Viewer"): {"type": "mime", "value": "application/pdf"},
            self.tr("Image Viewer"): {"type": "mime", "value": "image/jpeg"},
            self.tr("Video Player"): {"type": "mime", "value": "video/mp4"},
            self.tr("Audio Player"): {"type": "mime", "value": "audio/mpeg"},
        }

        self.setWindowTitle(self.tr("Linux App Manager"))
        self.setMinimumSize(600, 500)

        # Main layout
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1: Extension Search
        self.tab_extension = QWidget()
        self.setup_extension_tab()
        self.tabs.addTab(self.tab_extension, self.tr("By Extension"))

        # Tab 2: Common Apps
        self.tab_common = QWidget()
        self.setup_common_tab()
        self.tabs.addTab(self.tab_common, self.tr("Default Applications"))

        # Icon
        self.load_icon()

    def load_icon(self):
        icon_path = os.path.expanduser("~/.local/share/icons/appmanager.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            local_icon = os.path.join(os.path.dirname(__file__), "assets", "appmanager.svg")
            if os.path.exists(local_icon):
                self.setWindowIcon(QIcon(local_icon))

    def setup_extension_tab(self):
        layout = QVBoxLayout(self.tab_extension)
        
        # Header with About button
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel(self.tr("Enter file extension (e.g. pdf, txt):")))
        header_layout.addStretch()
        self.button_about = QPushButton()
        self.button_about.setIcon(self.windowIcon())
        self.button_about.setFixedSize(30, 30)
        self.button_about.setToolTip(self.tr("About"))
        self.button_about.clicked.connect(self.show_about)
        header_layout.addWidget(self.button_about)
        layout.addLayout(header_layout)

        self.entry_extension = QLineEdit()
        self.entry_extension.setPlaceholderText(self.tr("e.g. pdf"))
        self.entry_extension.returnPressed.connect(self.search_apps_extension)
        layout.addWidget(self.entry_extension)

        self.button_search = QPushButton(self.tr("Search Applications"))
        self.button_search.clicked.connect(self.search_apps_extension)
        layout.addWidget(self.button_search)

        self.list_apps_ext = QListWidget()
        layout.addWidget(self.list_apps_ext)

        self.button_set_ext = QPushButton(self.tr("Set as Default"))
        self.button_set_ext.clicked.connect(self.set_default_extension)
        layout.addWidget(self.button_set_ext)

    def setup_common_tab(self):
        layout = QVBoxLayout(self.tab_common)

        # Category selection
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel(self.tr("Category:")))
        self.combo_categories = QComboBox()
        self.combo_categories.addItems(self.COMMON_CATEGORIES.keys())
        self.combo_categories.currentTextChanged.connect(self.load_category_apps)
        h_layout.addWidget(self.combo_categories, 1)
        layout.addLayout(h_layout)

        # Current default display
        self.label_current_default = QLabel(self.tr("Current: Loading..."))
        self.label_current_default.setStyleSheet("font-weight: bold; color: #555;")
        layout.addWidget(self.label_current_default)

        # List of available apps
        layout.addWidget(QLabel(self.tr("Available Applications:")))
        self.list_apps_common = QListWidget()
        layout.addWidget(self.list_apps_common)

        # Set default button
        self.button_set_common = QPushButton(self.tr("Set as Default"))
        self.button_set_common.clicked.connect(self.set_default_common)
        layout.addWidget(self.button_set_common)

        # Initial load
        self.load_category_apps(self.combo_categories.currentText())

    def get_mime_type(self, extension):
        with tempfile.NamedTemporaryFile(suffix=f".{extension}", delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.write(b"temporal content")

        try:
            mime_type = subprocess.getoutput(f'xdg-mime query filetype {temp_filename}')
        finally:
            os.remove(temp_filename)

        return mime_type

    def get_applications(self, mime_type):
        dirs = [
            "/usr/share/applications/*.desktop",
            os.path.expanduser("~/.local/share/applications/*.desktop")
        ]
        applications = set()
        for d in dirs:
            output = subprocess.getoutput(f'grep -l "{mime_type}" {d} 2>/dev/null')
            if output:
                applications.update(output.splitlines())
        return sorted(list(applications))

    def set_default_application(self, mime_type, app):
        subprocess.run(f'xdg-mime default {app} {mime_type}', shell=True)

    def get_xdg_setting(self, property_name, subproperty=None):
        cmd = f'xdg-settings get {property_name}'
        if subproperty:
            cmd += f' {subproperty}'
        return subprocess.getoutput(cmd).strip()

    def set_xdg_setting(self, property_name, value, subproperty=None):
        cmd = f'xdg-settings set {property_name}'
        if subproperty:
            cmd += f' {subproperty}'
        cmd += f' {value}'
        subprocess.run(cmd, shell=True)

    def show_about(self):
        icon_path = os.path.expanduser("~/.local/share/icons/appmanager.png")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "appmanager.svg")
        
        pixmap = QPixmap(icon_path)
        dialog = AboutDialog(self, pixmap)
        dialog.exec()

    def search_apps_extension(self):
        extension = self.entry_extension.text().strip()
        if not extension:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Please enter an extension."))
            return

        mime_type = self.get_mime_type(extension)
        if not mime_type or "not found" in mime_type.lower():
            QMessageBox.critical(self, self.tr("Error"), self.tr("MIME type not found for .{0}").format(extension))
            return

        apps = self.get_applications(mime_type)
        self.list_apps_ext.clear()
        if apps:
            for app_path in apps:
                app_name = os.path.basename(app_path)
                item = QListWidgetItem(app_name)
                item.setData(Qt.ItemDataRole.UserRole, app_path)
                self.list_apps_ext.addItem(item)
        else:
            self.list_apps_ext.addItem(self.tr("No applications found."))

    def set_default_extension(self):
        selected_items = self.list_apps_ext.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Please select an application."))
            return

        item = selected_items[0]
        app_path = item.data(Qt.ItemDataRole.UserRole)
        if not app_path:
            return

        app_name = os.path.basename(app_path)
        extension = self.entry_extension.text().strip()
        mime_type = self.get_mime_type(extension)
        
        try:
            self.set_default_application(mime_type, app_name)
            QMessageBox.information(self, self.tr("Success"), self.tr("Default application for .{0} set to: {1}").format(extension, app_name))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Could not set default: {0}").format(str(e)))

    def load_category_apps(self, category_name):
        if not category_name: return
        config = self.COMMON_CATEGORIES[category_name]
        self.list_apps_common.clear()
        
        # Get current default
        current = ""
        if config["type"] == "mime":
            current = subprocess.getoutput(f'xdg-mime query default {config["value"]}')
            mime_type = config["value"]
        else:
            current = self.get_xdg_setting(config["value"], config.get("sub"))
            mime_map = {
                "default-web-browser": "text/html",
                "default-url-scheme-handler": "x-scheme-handler/mailto"
            }
            mime_type = mime_map.get(config["value"], "text/plain")

        self.label_current_default.setText(self.tr("Current: {0}").format(current if current else self.tr("Not defined")))

        # Load available apps
        apps = self.get_applications(mime_type)
        if apps:
            for app_path in apps:
                app_name = os.path.basename(app_path)
                item = QListWidgetItem(app_name)
                item.setData(Qt.ItemDataRole.UserRole, app_path)
                if app_name == current:
                    item.setSelected(True)
                    item.setBackground(Qt.GlobalColor.lightGray)
                self.list_apps_common.addItem(item)
        else:
            self.list_apps_common.addItem(self.tr("No compatible applications found."))

    def set_default_common(self):
        category_name = self.combo_categories.currentText()
        config = self.COMMON_CATEGORIES[category_name]
        
        selected_items = self.list_apps_common.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Please select an application."))
            return

        item = selected_items[0]
        app_path = item.data(Qt.ItemDataRole.UserRole)
        if not app_path:
            return

        app_name = os.path.basename(app_path)
        
        try:
            if config["type"] == "mime":
                self.set_default_application(config["value"], app_name)
            else:
                self.set_xdg_setting(config["value"], app_name, config.get("sub"))
            
            QMessageBox.information(self, self.tr("Success"), self.tr("Default for {0} changed to: {1}").format(category_name, app_name))
            self.load_category_apps(category_name)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Error setting default: {0}").format(str(e)))

def main():
    app = QApplication(sys.argv)
    
    # Translation setup
    translator = QTranslator()
    # Try multiple paths for translation files (local dev and system-wide)
    search_paths = [
        os.path.join(os.path.dirname(__file__), "translations"),
        "/usr/share/linux-app-manager/translations"
    ]
    for path in search_paths:
        if translator.load(QLocale(), "app_manager", "_", path):
            app.installTranslator(translator)
            break
    
    window = AppManager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
