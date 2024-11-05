# Portable Rez build by PyInstaller

This is an unofficial portable build of Rez, created using PyInstaller.

Original Rez repository: [AcademySoftwareFoundation/rez](https://github.com/AcademySoftwareFoundation/rez)

Rez documentation: [rez.readthedocs.io](https://rez.readthedocs.io/en/stable/index.html)

## Introduction

The official Rez project does not provide a standalone executable, and installing Rez can be complex, especially for users who are not familiar with Python, such as CG artists. This repository offers a portable build of Rez that can be run on any Windows machine without needing to install Python or Rez.

The behavior of this build should be identical to the official Rez build.

The only difference between this repository and the official Rez repository is the addition of the pyinstaller folder, which contains the build script and the necessary files to create the portable build.

## Usage

1. Download the latest release from the [Releases Page](https://github.com/FhyTan/portable_rez/releases)
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
