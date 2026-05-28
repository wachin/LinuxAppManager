# LinuxAppManager

LinuxAppManager is a small graphical utility for Linux desktops that helps you
manage default applications and file associations without editing MIME files by
hand.

It is useful when you want to see which installed programs can open a specific
file extension and choose one of them as the default application. It can also
manage common system defaults from a simple interface.

![App Preview](vx_images/403303311-AppManager.webp)

---

## What LinuxAppManager Does

LinuxAppManager can:

- Search compatible applications by file extension, for example `pdf`, `txt`,
  `jpg`, `mp4`, or any other extension recognized by your system.
- Detect the MIME type for that extension using `xdg-mime`.
- List installed `.desktop` launchers that declare support for that MIME type.
- Set the selected application as the default handler for that file type.
- Show and change common default applications:
  - File Manager
  - Web Browser
  - Text Editor
  - Email Client
  - PDF Viewer
  - Image Viewer
  - Video Player
  - Audio Player
  - Terminal Emulator
- Show the current default application for supported categories.
- Change the default terminal emulator through `update-alternatives`
  (`pkexec` may ask for administrator authentication).
- Load translations automatically according to your system language.

The application is designed around standard Linux desktop tools such as
`xdg-mime`, `xdg-settings`, `.desktop` files, and `update-alternatives`.

---

## Available Languages

LinuxAppManager is available in **17 languages/locales**:

- English
- Arabic
- Chinese, Simplified
- Chinese, Traditional
- Dutch
- French
- German
- Italian
- Japanese
- Korean
- Polish
- Portuguese, Brazil
- Russian
- Spanish
- Swedish
- Turkish
- Ukrainian

The program automatically tries to use the language configured in your system.
If a translation is not available, it falls back to English.

---

## Run in a Specific Language

LinuxAppManager can load a specific Qt translation file from the terminal. The
runtime translation files are the `.qm` files inside the `translations/`
directory.

No extra package is needed to launch the program with an existing `.qm` file
beyond the normal runtime dependencies (`python3`, `python3-pyqt6`, and
`xdg-utils`).

For example, to launch the program in Spanish from the source directory:

```bash
python3 app_manager.py --qm translations/app_manager_es.qm
```

To launch it in English for a screenshot, do not load any translation. English
is the original interface language and does not need a `.qm` file:

```bash
python3 app_manager.py --no-translation
```

You can also use the bundled language-code shortcut:

```bash
python3 app_manager.py --lang fr
python3 app_manager.py --lang pt_BR
python3 app_manager.py --lang zh_CN
```

If you use the installed launcher command, replace `python3 app_manager.py`
with `linux-app-manager` and point `--qm` to the installed translation file:

```bash
linux-app-manager --qm /usr/share/linux-app-manager/translations/app_manager_fr.qm
```

Common launch commands from the source directory:

| Language | Command |
| --- | --- |
| English | `python3 app_manager.py --no-translation` |
| Arabic | `python3 app_manager.py --qm translations/app_manager_ar.qm` |
| Chinese, Simplified | `python3 app_manager.py --qm translations/app_manager_zh_CN.qm` |
| Chinese, Traditional | `python3 app_manager.py --qm translations/app_manager_zh_TW.qm` |
| Dutch | `python3 app_manager.py --qm translations/app_manager_nl.qm` |
| French | `python3 app_manager.py --qm translations/app_manager_fr.qm` |
| German | `python3 app_manager.py --qm translations/app_manager_de.qm` |
| Italian | `python3 app_manager.py --qm translations/app_manager_it.qm` |
| Japanese | `python3 app_manager.py --qm translations/app_manager_ja.qm` |
| Korean | `python3 app_manager.py --qm translations/app_manager_ko.qm` |
| Polish | `python3 app_manager.py --qm translations/app_manager_pl.qm` |
| Portuguese, Brazil | `python3 app_manager.py --qm translations/app_manager_pt_BR.qm` |
| Russian | `python3 app_manager.py --qm translations/app_manager_ru.qm` |
| Spanish | `python3 app_manager.py --qm translations/app_manager_es.qm` |
| Swedish | `python3 app_manager.py --qm translations/app_manager_sv.qm` |
| Turkish | `python3 app_manager.py --qm translations/app_manager_tr.qm` |
| Ukrainian | `python3 app_manager.py --qm translations/app_manager_uk.qm` |

The `.ts` files are editable translation sources. They are not loaded directly
when the program starts. If you edit a `.ts` file, compile it to `.qm` first.
For that compilation step only, install the Qt 6 translation tools on
Debian-based systems with:

```bash
sudo apt install qt6-l10n-tools
```

Then compile a `.ts` file like this:

```bash
/usr/lib/qt6/bin/lrelease translations/app_manager_fr.ts -qm translations/app_manager_fr.qm
```

After that, launch the program with the generated `.qm` file.

---

## Requirements

On Debian 12 or Debian-based systems, install the runtime dependencies with APT:

```bash
sudo apt install python3 python3-pyqt6 xdg-utils git
```

`pip` is **not required** to run LinuxAppManager if PyQt6 is installed from your
distribution packages.

Using `pip` is optional. It is only needed if you prefer to install the Python
dependency from `requirements.txt` instead of using your system package manager.

Optional `pip` method:

```bash
python3 -m pip install -r requirements.txt
```

---

## Run From Source

Clone the repository:

```bash
git clone https://github.com/wachin/LinuxAppManager
cd LinuxAppManager
```

Run the program:

```bash
python3 app_manager.py
```

---

## Optional Icon Setup

The program can use the icon directly from the repository. If you want to
install the icon into your local icon directory, run:

```bash
mkdir -p ~/.local/share/icons/
cp assets/appmanager.svg ~/.local/share/icons/appmanager.svg
```

---

## Optional Python Package Installation

If you prefer to install the project as a Python package, you can do it with
`pip`. This is optional and is not required for normal execution from source.

```bash
python3 -m pip install .
linux-app-manager
```

---

## User Guide

### Search Applications by Extension

1. Open the **By Extension** tab.
2. Enter a file extension without the dot, for example `pdf` or `txt`.
3. Click **Search Applications**.
4. Select an application from the list.
5. Click **Set as Default**.

### Manage Default Applications

1. Open the **Default Applications** tab.
2. Select a category, such as Web Browser, File Manager, or PDF Viewer.
3. Review the current default shown by the program.
4. Select the preferred application.
5. Click **Set as Default**.

For the Terminal Emulator category, LinuxAppManager uses the system
`x-terminal-emulator` alternative. Changing it may require administrator
authentication.

---

## License

LinuxAppManager is released under the GPL3 license.
