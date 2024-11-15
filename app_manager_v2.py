import subprocess
import tempfile
import os
import tkinter as tk
from tkinter import messagebox

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

def search_apps():
    extension = entry_extension.get().strip()
    if not extension:
        messagebox.showerror("Error", "Por favor, ingrese una extensión de archivo.")
        return

    mime_type = get_mime_type(extension)
    if not mime_type:
        messagebox.showerror("Error", f"No se encontró el tipo MIME para .{extension}")
        return

    apps = get_applications(mime_type)
    listbox_apps.delete(0, tk.END)
    if apps:
        for app in apps:
            listbox_apps.insert(tk.END, app)
    else:
        listbox_apps.insert(tk.END, "No se encontraron aplicaciones.")

def set_default():
    selection = listbox_apps.curselection()
    if not selection:
        messagebox.showerror("Error", "Por favor, seleccione una aplicación.")
        return

    selected_app = listbox_apps.get(selection[0])
    extension = entry_extension.get().strip()
    mime_type = get_mime_type(extension)
    set_default_application(mime_type, selected_app)
    messagebox.showinfo("Éxito", f"Aplicación predeterminada establecida a: {selected_app}")

# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Aplicaciones por Extensión de Archivo")

# Etiqueta y entrada para la extensión del archivo
label_extension = tk.Label(root, text="Extensión de archivo:")
label_extension.pack(pady=5)
entry_extension = tk.Entry(root)
entry_extension.pack(pady=5)

# Botón para buscar aplicaciones
button_search = tk.Button(root, text="Buscar Aplicaciones", command=search_apps)
button_search.pack(pady=5)

# Lista para mostrar las aplicaciones
listbox_apps = tk.Listbox(root, height=10, width=50)
listbox_apps.pack(pady=5)

# Botón para establecer la aplicación predeterminada
button_set_default = tk.Button(root, text="Establecer como Predeterminada", command=set_default)
button_set_default.pack(pady=5)

# Ejecutar la aplicación
root.mainloop()

