# Development Roadmap

This document outlines the progress and future plans for **LinuxAppManager**.

## **Achieved Goals**
- [x] Port application from Tkinter to **PyQt6**.
- [x] Implement **Default Applications** tab for system categories (Web Browser, File Manager, etc.).
- [x] Full **Internationalization (i18n)** support with Qt Linguist.
- [x] Support for **17 languages** (English, Spanish, Portuguese, Italian, Polish, Arabic, Turkish, Korean, German, French, Russian, Ukrainian, Dutch, Japanese, Simplified/Traditional Chinese, Swedish).
- [x] Project restructuring for **Debian guidelines** compliance.
- [x] Added `setup.py` and `.desktop` entry for system integration.
- [x] Updated documentation (README) in English.

## **Short-Term Goals (v1.1.0)**
- [ ] Complete **Debian packaging** (`debian/` directory with control, rules, etc.).
- [ ] Add support for more system categories (Terminal Emulator, Archive Manager).
- [ ] Improve UI with custom themes or dark mode support.
- [ ] Add "Open With" test functionality to verify defaults within the app.

## **Long-Term Goals (v2.0.0)**
- [ ] Support for Flatpak and Snap application detection.
- [ ] Integration with more Desktop Environments (beyond XDG standards if necessary).
- [ ] Submission to official **Debian repositories**.
