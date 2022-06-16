dsmcp applications
******************

The `dsmcp` package provides a family of human-machine interface applications for Dassym electronic boards.

These interfaces can be command line (CLI) or graphical user interface (GUI).

These applications can connect to the electronic board in 2 ways:

- **direct** through a serial interface (RS-232)
- **remotely** via a *proxi* and the *dsm-scp* client application.

Version: |release|


Licence
=======

Copyright ® 2021  |DASSYM| SA

This program is free software: you can redistribute it and/or modify
it under the terms of the **GNU General Public License** as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can consult the GNU General Public License on http://www.gnu.org/licenses/gpl-3.0.html.

:doc:`app-overview`

    
Package
-------
    
The package itself is able to launch an application with the following command:

.. code:: bash

   python3 -m dsmcp 
   
Command line usage
..................

.. literalinclude:: __main__.clu  
    
    

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   app-overview
   app
   