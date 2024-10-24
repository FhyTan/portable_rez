# Portable Rez build by PyInstaller

This is an unofficial portable build of Rez, created using PyInstaller. It is intended to be used as a standalone executable, which can be run on any Windows machine without the need to install Python or Rez.

The behavior of this build should be identical to the official Rez build.

The only difference between this repository and the official Rez repository is the addition of the pyinstaller folder, which contains the build script and the necessary files to create the portable build.

Original Rez repository: [AcademySoftwareFoundation/rez](https://github.com/AcademySoftwareFoundation/rez)

Rez documentation: [rez.readthedocs.io](https://rez.readthedocs.io/en/stable/index.html)

## Usage

1. Download the latest release from the [Latest Releases](https://github.com/FhyTan/portable_rez/releases/download/Latest/portable_rez-3.2.0-x86_64-windows-py311.zip)
2. Extract the contents of the zip file to a folder of your choice
3. Add the folder to your PATH environment variable

now you can run `rez` from the command line as you would with the official build.

## Build

Currently just provides a Windows build, but it should be possible to build for other platforms or other python versions as well.

The build script is located in the `pyinstaller` folder. Just installer pyinstaller and run the command with your desired python version and platform:

```bash
pip install pyinstaller
python ./pyinstaller/build.py
```
