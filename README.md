# eltuxusb

## Supported hardware

This program only works with the following devices:

 * ELUSB-1 
 * ELUSB-2
 * ELUSB-2-LCD

Support will be extended to other Lascar products if possible (if I actually have another products in my hands).

## Installation

We need read and write access to the device. To do this as a non-root user, you need to create a udev rule:

    echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="10c4", ATTR{idProduct}=="0002", MODE:="0666"' | sudo tee /etc/udev/rules.d/10-local.rules
    sudo reboot

Under latests Ubuntu relase the udev rule doesn't work anymore, I have to figure out why but you have to add a "GROUP" key to the rule and add your user into it:

    SUBSYSTEM=="usb", ATTR{idVendor}=="10c4", ATTR{idProduct}=="0002", MODE:="0666", GROUP:="usbusers"

### Ubuntu

    sudo apt-get install python-dev gcc python-matplotlib python-pip git-core
    sudo pip install git+http://github.com/eltuxusb/eltuxusb.git#egg=eltuxusb

### Fedora

    sudo yum install python-pip gcc python-matplotlib python-devel git
    sudo pip-python install git+http://github.com/eltuxusb/eltuxusb.git#egg=eltuxusb

## Usage

Run the program, which PIP should have installed in your $PATH:

    eltuxusb
