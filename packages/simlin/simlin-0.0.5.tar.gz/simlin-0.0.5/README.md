# SIMLIN - Simple Image Manipulator for Linux

Version 0.0.5b

![Simlin Demo](https://www.linuxnorth.org/simlin/output.gif)

This project is simply for learning.  Do not use it for anything important as it could have unintended consequences.

SIMLIN is a Simple Image Manipulator for Linux.  This utility does only one thing at the moment.  It takes images in the current working folder and resizes them in the 'resized' subfolder.

The end goal is to have a fully functional command line utility that will do various scriptable batch image manipulations.

## Usage

Resize can be completed in batch or interactive mode

    batch mode
    simlin -r <int> -q <int>

Where -r is the new horizontal size and -q is the image quality (0-95)

    interactive mode. go to directory and type

    simlin


## Install

sudo pip3 install simlin.


## Requires

* Python3
* Pillow (latest version)
