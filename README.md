# LinuxAppManager
I needed a program that would only show me the programs that can open a file extension and allow me to select one of them and set it as the default application to open, this is my creation.

### **LinuxAppManager Installation and Usage Manual**

This document will guide you through the installation and use of the **LinuxAppManager** program, which you can find in its GitHub repository:  
[LinuxAppManager](https://github.com/wachin/LinuxAppManager)

---

## **Prerequisites**

To run the program, you need to have the following packages installed on a Debian 12 system (or Debian-based):

1. **Python 3**  
   Python must be installed. If not, you can install it by running:  
   ```bash
   sudo apt install python3
   ```

2. **PyQt6 and Git**  
   PyQt6 is required for the graphical interface, and git to clone the repository:  
   ```bash
   pip install PyQt6
   sudo apt install git
   ```

---

## **Installation**

1. **Clone the repository**  
   Download the source code from GitHub:  
   ```bash
   git clone https://github.com/wachin/LinuxAppManager
   ```

2. **Access the project directory**  
   Navigate to the project directory:  
   
   ```bash
   cd LinuxAppManager
   ```
   
3. **(Optional) Install the icon for `app_manager.py`**  
   If you want to use the icon, you need to copy the icon file to the system's standard location:  
   
   ```bash
   mkdir -p ~/.local/share/icons/
   cp assets/appmanager.svg ~/.local/share/icons/appmanager.png
   ```
   You can also copy it manually using a file manager.

---

## **Using the Program**

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the program**:  
   ```bash
   python3 app_manager.py
   ```

The program will automatically detect your system language (English and Spanish supported).

---

## **User Guide**

The program has two main functionalities: 

### **1. Search Applications by Extension**
- Enter the file extension (without the dot, e.g., `txt` or `pdf`).
- Click **"Search Applications"**.
- Select an app from the list and click **"Set as Default"**.

### **2. Default Applications (System Categories)**
- Go to the **"Default Applications"** tab.
- Select a category (e.g., Web Browser, File Manager).
- Choose your preferred application and set it as the system default.

![App Preview](vx_images/403303311-AppManager.webp)
---
