# Dassym DSM-CP installation tutorial

This document is an installation guide for Dassym dsmcp application. It explained all the step to have a functionnal dsmcp application.

## Requirement 

You must have at least python 3.8 installed on your computer.

## Windows

### Installation 

1. Download the installer `dsmcp-setup.exe` from **[Dassym DSM-CP repository](https://cloud.dassym.com/index.php/s/SronqwT56Ce6n77)**
2. Double-click to execute the installer 
3. Follow the installer's instructions 

## Debian

### Pre-installation

1. Update your package source : `sudo apt-get update`
2. Install pip on your computer : `sudo apt-get install python3-pip`
3. Add your user to the serial port group : `sudo usermod -aG dialout $USER`
4. Reboot your computer to applied the changes : `reboot`
5. Installation of dependencies
	- Installation of main dependencies : `python3 -m pip install pyserial lxml chardet PyDapi2`
	- Installation of a PyQt5 dependence : `sudo apt-get install --reinstall libxcb-xinerama0` 
	- Installation of PyQt5 : `python3 -m pip install pyqt5` (can be very long on a Raspberry Pi)


### Installation 

1. Download the deb package from **[here](https://github.com/dassym/)**
2. Execute the deb package installer : `sudo dpkg -i dsmcp_x.x-x_amd64.deb` (change the `x` with your version)

### Post-installation

1. If you are using a computer with embedded serial port or you use a VM 
	- Change the default serial port in the `$HOME/dassym/dsmcp.ini` in *line 42* from `default_serial=/dev/ttyUSB0` to `default_serial=/dev/ttyS0` (you have to run the dcp programm at least one time to let it create the config file)

### Start the apps 

- dcpbasic without gui : `dcpbasic --cli -S` 
- dcpbasic with gui : `dcpbasic -S`
- dcpdev with gui : `dcpdev -S`

### For help with the command line 

Execute the command `dcpbasic --help` or  `dcpdev --help`

