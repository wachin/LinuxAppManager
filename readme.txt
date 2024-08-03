interfaz gráfica de usuario (GUI) en Python utilizando Tkinter que permite:

1. Ingresar una extensión de archivo para consultar qué aplicaciones pueden abrirla.
2. Mostrar una lista de aplicaciones que pueden abrir la extensión.
3. Permitir seleccionar una aplicación para establecerla como predeterminada.


### Instrucciones

1. **Instalación de Tkinter**: Asegúrate de tener Tkinter instalado en tu sistema. En la mayoría de las distribuciones de Linux, viene preinstalado, pero puedes instalarlo con:
   ```sh
   sudo apt-get install python3-tk
   ```

2. **Ejecutar el script**: Guarda el código en un archivo, por ejemplo, `app_manager.py`, y ejecuta el script con:
   ```sh
   python3 app_manager.py
   ```

3. **Uso de la aplicación**:
   - **Extensión de archivo**: Ingresa la extensión del archivo (por ejemplo, `md`) y presiona el botón "Buscar Aplicaciones".
   - **Lista de aplicaciones**: Selecciona una aplicación de la lista para establecerla como predeterminada.
   - **Establecer por defecto**: Haz clic en "Establecer como Predeterminada" para hacer que la aplicación seleccionada sea la predeterminada para esa extensión.

### Notas

- El código utiliza `subprocess.getoutput` para ejecutar comandos en la línea de comandos y obtener resultados.
- El archivo temporal creado (`temp.{extension}`) se utiliza para determinar el tipo MIME del archivo.
- Puedes mejorar la GUI añadiendo más funcionalidades o refinando la interfaz.


