# dsmcp
## installation
```
pip install dsmcp
```
## run the application
by passing a config file
```
python3 -m dsmcp -c [config file].ini basic
```
or by passing params in command line
```
python3 -m dsmcp 
```
replace host by the host url and port by the host port
## config file structure
```
[GLOBAL]
loglevel=info
host=host:port
```

The *PyDapi2* library offers a Python implementation of the Dassym API version 2.

Dassym API version 2 aka **DAPI2** is the application programming interface (API) used to
control Dassym electronic boards.

This library was created to meet internal needs in Dassym. 

Version : 0.0.3 (2021-05-17)