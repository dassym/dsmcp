# dsmcp

The **DSMCP** program is a Python implementation of a control panel for Dassym engines.
**DSMCP** can be used to control motors by connecting a Dassym electronic card (MB-x) to the PC via an RS-232 link.
**DSMCP** is based on the PyDapi2 library.

**DSMCP** can work with a graphical user interface (GUI) or simply with the command line (CLI).

It is possible to trace all the messages exchanged with the card.

This program was created for the internal needs of Dassym.
It is distributed to help our partners in their projects to integrate our products into their own solutions.

This program is free software: you can redistribute it and/or modify
it under the terms of the **GNU General Public License** as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can consult the GNU General Public License on <http://www.gnu.org/licenses/gpl-3.0.html>.

Version: 0.5.18 (2023-06-26)

## Installation

After the first launch of the application. The `dassym` directory will be created with the default dsmcp.ini configuration file.
The configuration file allows, among other things, to specify the serial port to use.

### Prerequisite

- Python 3.8 or later
- Libraries : *lxml*, *pyserial* and *PyDapi2* (all available on [PyPI](https://pypi.org/))

### GNU/Linux installation
1. Get the dsmcp-v.v-v_amd64.deb archive on [GitHub](https://www.dassym.com/files/debs/dsmcp)
2. Use dpkg to install it (`sudo dpkg -i dsmcp-v.v-v_amd64.deb archive`)
3. Modify the dsmcp.ini file for your configuration

### Windows installation


## Run the application

The *DSMCP* includes several applications such as:

- dcpbasic: a basic control panel implementation
- dcpdev : an implementation for development
- dcpsrv: an implementation for service support

### Run on GNU/Linux



### Run on Windows



