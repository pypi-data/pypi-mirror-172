# Command line Interface in Python

In this package I build an example of a command line interface(CLI)
based on CLI from linux bash commands. The main proposal of this
package is to workaround how to create a package in python.


## How to install

```bash
pip install cli-python
```

## Usage

```bash
$ python                                                                                                
Python 3.9.10 (main, Jul 10 2022, 21:54:43) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from clisrc import CommandLine
>>> cmd = CommandLine(cmdline='')
/usr/bin/zsh
>>> cmd.ls()
total 32K
4,0K drwxrwxr-x 5 andsilva andsilva 4,0K out 16 20:20 .
4,0K drwxrwxr-x 6 andsilva andsilva 4,0K out 16 20:20 ..
4,0K drwxrwxr-x 2 andsilva andsilva 4,0K out 16 20:20 cli_python.egg-info
4,0K drwxrwxr-x 3 andsilva andsilva 4,0K out 16 20:20 clisrc
4,0K drwxrwxr-x 2 andsilva andsilva 4,0K out 16 20:20 dist
4,0K -rw-rw-r-- 1 andsilva andsilva 1,1K out 16 20:20 license.txt
4,0K -rw-rw-r-- 1 andsilva andsilva 1,3K out 16 20:20 README.md
4,0K -rw-rw-r-- 1 andsilva andsilva  674 out 16 20:20 setup.py
>>> cmd.pwd()
The path where you are right now!
~/repo/Data-Science-bootcamp/buildpip
```

## Directory structure

```bash
$ tree                                                                                                 
.
├── cli_python.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── clisrc
│   ├── clipython.py
│   ├── commandLineInterface.py
│   ├── __init__.py
│   └── __pycache__
│       ├── clipython.cpython-39.pyc
│       ├── commandLineInterface.cpython-39.pyc
│       └── __init__.cpython-39.pyc
├── dist
│   └── cli_python-0.0.1.tar.gz
├── license.txt
├── README.md
└── setup.py

4 directories, 14 files
```

## License
This project is licensed under the MIT License

## Author

[Andre Vieira Silva](https://andsilvadrcc.gitlab.io/my-web-page-andre-vieira/).

## Useful link

[Create your own Python package and publish it into PyPI](https://towardsdatascience.com/create-your-own-python-package-and-publish-it-into-pypi-9306a29bc116)