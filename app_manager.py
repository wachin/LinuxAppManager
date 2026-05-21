import sys
import subprocess
import tempfile
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QVariant

def get_mime_type(extension):
    # Crear un archivo temporal en la carpeta del sistema
    with tempfile.NamedTemporaryFile(suffix=f".{extension}", delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write(b"temporal content")  # Escribir contenido al archivo temporal

    try:
        # Obtener el tipo MIME
        mime_type = subprocess.getoutput(f'xdg-mime query filetype {temp_filename}')
    finally:
        # Eliminar el archivo temporal
        os.remove(temp_filename)

    return mime_type

def get_applications(mime_type):
    # Buscar las aplicaciones que pueden abrir el tipo MIME
    output = subprocess.getoutput(f'grep "{mime_type}" /usr/share/applications/*.desktop | cut -d":" -f1')
    applications = output.splitlines()
    return applications

def set_default_application(mime_type, app):
    # Establecer la aplicación por defecto para el tipo MIME
    subprocess.run(f'xdg-mime default {app} {mime_type}', shell=True)

class AppManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Aplicaciones por Extensión de Archivo")
        self.setMinimumSize(400, 450)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Icon
        icon_path = os.path.expanduser("~/.local/share/icons/appmanager.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Fallback to local assets if ~/.local doesn't have it
            local_icon = os.path.join(os.path.dirname(__file__), "assets", "appmanager.svg")
            if os.path.exists(local_icon):
                self.setWindowIcon(QIcon(local_icon))

        # Extension input
        layout.addWidget(QLabel("Extensión de archivo:"))
        self.entry_extension = QLineEdit()
        self.entry_extension.setPlaceholderText("ej: pdf, txt, html")
        layout.addWidget(self.entry_extension)

        # Search button
        self.button_search = QPushButton("Buscar Aplicaciones")
        self.button_search.clicked.connect(self.search_apps)
        layout.addWidget(self.button_search)

        # Applications list
        self.listbox_apps = QListWidget()
        layout.addWidget(self.listbox_apps)

        # Set default button
        self.button_set_default = QPushButton("Establecer como Predeterminada")
        self.button_set_default.clicked.connect(self.set_default)
        layout.addWidget(self.button_set_default)

    def search_apps(self):
        extension = self.entry_extension.text().strip()
        if not extension:
            QMessageBox.critical(self, "Error", "Por favor, ingrese una extensión de archivo.")
            return

        # Ensure extension starts with a dot if needed by get_mime_type logic, 
        # though current logic adds it if missing or assumes it's just the extension name.
        # The original code used f".{extension}", so if user enters "pdf", it becomes ".pdf".
        
        mime_type = get_mime_type(extension)
        if not mime_type or "not found" in mime_type.lower():
            QMessageBox.critical(self, "Error", f"No se encontró el tipo MIME para .{extension}")
            return

        apps = get_applications(mime_type)
        self.listbox_apps.clear()
        if apps:
            for app_path in apps:
                app_name = os.path.basename(app_path)
                item = QListWidgetItem(app_name)
                item.setData(Qt.ItemDataRole.UserRole, app_path)
                self.listbox_apps.addItem(item)
        else:
            self.listbox_apps.addItem("No se encontraron aplicaciones.")

    def set_default(self):
        selected_items = self.listbox_apps.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, "Error", "Por favor, seleccione una aplicación.")
            return

        item = selected_items[0]
        selected_app_path = item.data(Qt.ItemDataRole.UserRole)
        
        if not selected_app_path: # Case where "No se encontraron aplicaciones" is selected
            return

        # xdg-mime default usually expects the .desktop filename, not the full path.
        # However, we will use the basename to be safe as per xdg-mime specs for desktop-file-id.
        selected_app = os.path.basename(selected_app_path)
        
        extension = self.entry_extension.text().strip()
        mime_type = get_mime_type(extension)
        
        try:
            set_default_application(mime_type, selected_app)
            QMessageBox.information(self, "Éxito", f"Aplicación predeterminada establecida a: {selected_app}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo establecer la aplicación: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppManager()
    window.show()
    sys.exit(app.exec())
