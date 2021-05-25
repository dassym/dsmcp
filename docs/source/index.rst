dsmcp applications
******************

The `dsmcp` package provides a family of human-machine interface applications for Dassym electronic boards.

These interfaces can be command line (CLI) or graphical user interface (GUI).

These applications can connect to the electronic board in 2 ways:

- **direct** through a serial interface (RS-232)
- **remotely** via a *proxi* and the *dsm-scp* client application.


Applications
============

*Basic Control Panel* application
---------------------------------

The *Basic Control Panel* application provides the essential functions to control a Dassym electronic card.


Command line usage
..................

.. code-block:: none

    usage: dcpbasic.py [-h] [-c CONFIG] [--no-gui] [--qt5-options QT5_OPTIONS]
                  [--lang LANG] [-l {error,warning,debug,info,noset}]
                  [--log-file LOGFILE] [--log-max-size LOG_MAXBYTES]
                  [--log-backup-count LOG_BACKUPCOUNT] [-t] [-S SERIAL] [-H HOST]
                  [-C] [-R] [-b BAUDRATE] [-v] [--registers REGFILE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Configuration file (.ini)
      --no-gui              If present start no GUI application
      --qt5-options QT5_OPTIONS
                            Qt5 options
      --lang LANG           ISO name of language to use.
      -l {error,warning,debug,info,noset}, --log-level {error,warning,debug,info,noset}
                            Log level. (default = info)
      --log-file LOGFILE    LOG file (default = stderr)
      --log-max-size LOG_MAXBYTES
                            Maximum LOG file size in bytes (default=100000).
      --log-backup-count LOG_BACKUPCOUNT
                            Number of LOG files retained (default=10).
      -t, --trace           If present, trace API message exchanges (default = not)
      -S SERIAL, --serial SERIAL
                            Serial port for direct control.
      -H HOST, --host HOST  Host name and port for remote control. (host:port)
      -C, --command-mode    Sets the preferred DAPI2 mode to 'command'. (Default=command)
      -R, --register-mode   Sets the preferred DAPI2 mode to 'register'. (Default=command)
      -b BAUDRATE, --baudrate BAUDRATE
                            Baud rate. (default : 115200)
      -v, --version         Show software version
      --registers REGFILE   The XML registers definition file



.. automodule:: dcpbasic
    :members:
    :undoc-members:
    :show-inheritance:

*Development Control Panel* application
---------------------------------------

The *Development Control Panel* application provides a wide range of functions to facilitate
the development of firmware for Dassym electronic boards.


.. code-block:: none

    usage: dcpdev.py [-h] [-c CONFIG] [--no-gui] [--qt5-options QT5_OPTIONS]
                  [--lang LANG] [-l {error,warning,debug,info,noset}]
                  [--log-file LOGFILE] [--log-max-size LOG_MAXBYTES]
                  [--log-backup-count LOG_BACKUPCOUNT] [-t] [-S SERIAL] [-H HOST]
                  [-C] [-R] [-b BAUDRATE] [-v] [--registers REGFILE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Configuration file (.ini)
      --no-gui              If present start no GUI application
      --qt5-options QT5_OPTIONS
                            Qt5 options
      --lang LANG           ISO name of language to use.
      -l {error,warning,debug,info,noset}, --log-level {error,warning,debug,info,noset}
                            Log level. (default = info)
      --log-file LOGFILE    LOG file (default = stderr)
      --log-max-size LOG_MAXBYTES
                            Maximum LOG file size in bytes (default=100000).
      --log-backup-count LOG_BACKUPCOUNT
                            Number of LOG files retained (default=10).
      -t, --trace           If present, trace API message exchanges (default = not)
      -S SERIAL, --serial SERIAL
                            Serial port for direct control.
      -H HOST, --host HOST  Host name and port for remote control. (host:port)
      -C, --command-mode    Sets the preferred DAPI2 mode to 'command'. (Default=command)
      -R, --register-mode   Sets the preferred DAPI2 mode to 'register'. (Default=command)
      -b BAUDRATE, --baudrate BAUDRATE
                            Baud rate. (default : 115200)
      -v, --version         Show software version
      --registers REGFILE   The XML registers definition file


.. automodule:: dcpdev
    :members:
    :undoc-members:
    :show-inheritance:
    

    
    
app package
-----------

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   app
   