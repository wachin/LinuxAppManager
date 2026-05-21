from setuptools import setup, find_packages

setup(
    name="linux-app-manager",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["app_manager"],
    install_requires=[
        "PyQt6",
    ],
    entry_points={
        "console_scripts": [
            "linux-app-manager=app_manager:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "translations/*.qm"],
    },
    author="Washington Indacochea Delgado",
    author_email="linuxfrontier@proton.me",
    description="A simple application to manage default file handlers in Linux",
    license="GPL3",
    keywords="linux xdg mime application manager",
    url="https://github.com/wachin/LinuxAppManager",
)
