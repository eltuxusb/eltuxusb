# eltuxusb

## Supported hardware

This program only works with the following devices:

 * ELUSB-1 
 * ELUSB-2
 * ELUSB-2-LCD

Support will be extended to other Lascar products if possible (if we actually have another products in our hands).

## Installation

We need read and write access to the device. To do this as a non-root user, the PIP installer should automatically create the following udev rule: /etc/udev/rules.d/10-local.rules

    SUBSYSTEM=="usb", ATTR{idVendor}=="10c4", ATTR{idProduct}=="0002", MODE:="0666", GROUP:="usbusers"

If not create it by hand.

With latest udev release the device must also be part of a group, we used here the group "usbusers". You need to create this group in your system and add the desired user(s) into it.

### Ubuntu

    sudo apt-get install python-dev gcc python-matplotlib python-pip git-core
    sudo pip install git+http://github.com/eltuxusb/eltuxusb.git#egg=eltuxusb
    udevadm control --reload-rules (OR sudo reboot)

### Fedora

    sudo yum install python-pip gcc python-matplotlib python-devel git
    sudo pip-python install git+http://github.com/eltuxusb/eltuxusb.git#egg=eltuxusb
    sudo reboot

## Usage

Run the program, which PIP should have installed in your $PATH:

    eltuxusb
    
## Remove

To remove the program:

    sudo pip uninstall eltuxusb
