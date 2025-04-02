<p align="center"> <img src="src/prime_number_finder/resources/images/prime_number_finder-256.png" /> </p>

## Table of Contents

[Donations](#donations)  
[Stars](#stars)
[Purpose](#purpose)  
[Install on Linux](#linux)  
[Install on Windows](#windows)  
[Build Source Code](#build-source-code)  
[Visual App Showcase](#app-showcase)  
[Other useful information](#useful-information)

## Donations

[Buy Me A Coffee](https://buymeacoffee.com/KingKairos)  
[GitHub Sponsors](https://github.com/sponsors/melvinquick)

## Stars

If you like this project, please consider giving it a star on [Codeberg](https://codeberg.org/melvinquick/prime_number_finder) or [GitHub](https://github.com/melvinquick/prime_number_finder)!

## Purpose

The purpose of this project is to make a simple app to look for Prime Numbers and to check and see if any particular number you desire is prime.

## Install/Uninstall

**Note**: Your system needs to have Python 3.12 or higher installed to run this!

### Linux

Install: `curl -s https://codeberg.org/melvinquick/prime_number_finder/raw/branch/main/install.py | python3 -`  
Uninstall: `curl -s https://codeberg.org/melvinquick/prime_number_finder/raw/branch/main/uninstall.py | python3 -`

### Windows

I will be updating my install and uninstall scripts in upcoming days/weeks/months to allow this. For now, please follow the instructions in [Build Source Code](#build-source-code)

### Build Source Code

If you're not on Linux, or if you want to build this from source, you'll need to do the following.

1. Make sure Python 3.12 or higher is installed.
2. Make sure [UV](https://docs.astral.sh/uv/) is installed.
3. Within a terminal:
   1. `cd` into whatever directory you'd like.
   2. Run the command `git clone https://codeberg.org/melvinquick/prime_number_finder.git`.
   3. `cd` into `prime_number_finder`
4. Run the command `uv sync`
5. Run the command `uv run prime-number-finder`

## App Showcase

![app-showcase.gif](src/prime_number_finder/resources/gifs/app_showcase.gif)

## Useful Information

[Project Goals](https://codeberg.org/melvinquick/prime_number_finder/projects/14092)  
[Latest Releases](https://pypi.org/project/prime_number_finder/)
