# Pioneer600
Python project for creating a headless Raspberry Pi server and easily outputting information and executing simple commands

## Installing required libraries

`sudo apt-get install python-dev python-smbus python-imaging python-serial`

You must enable i2c, SPI, and Serial with `sudo raspi-config`

You can run the module in boot by typing `sudo crontab -e` to the terminal and adding `@reboot /path/to/Pioneer600.py`

## Functions

*Left and Right changes the Main Menus, Up and Right changes the Submenus*

**1. Information on the Server**

1.1. Up Status and IP

1.2. Network Status

1.3. SSH (Secure Socket Shell) Server Status

**2. Device Information**

2.1. Information on Disk Usage

2.2. Free RAM

2.3. CPU Usage

2.4. CPU Temperature

**3. Power Menu**

3.1. Halt System

3.2. Reboot

3.3. Exit Module

**4. Interfaces**

4.1. Wlan0

4.2. Eth0




## Feel free to make requests and ask for support
