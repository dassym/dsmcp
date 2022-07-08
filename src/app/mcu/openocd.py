'''

:author:  F. Voillat
:date: 2022-06-24 Creation
:copyright: Dassym SA 2021
'''

import subprocess
from .base import BaseExternalMcuInterface  


    


class OpenocdExternalMcuInterface(BaseExternalMcuInterface):
    
    EXEC = 'openocd'
    TRANSPORT = 'echo "Default transport"'
    PROTECT_CLEARING='flash protect 0 0 last off'
    UNPROTECT_CLEARING='echo "Protection not cleared"'
    FLASH_ERASE='flash erase_sector 0 0 last'
    FLASH_KEEP='echo "Flash Erase disabled"'
    
    
    def __init__(self):
        super().__init__()
        
    def setUp(self):
        pass
    
    
    def execute(self, *commands):
        args = (f"-c{cmd!s}" for cmd in commands)
        ret = subprocess.run((self.EXEC,*args))
        

    def tearDown(self):
        pass
    
    
    def program(self, fpath):
        pass
        
        
class OlimexJTAG(OpenocdExternalMcuInterface):
    
    INTERFACE = 'script interface/ftdi/olimex-arm-usb-tiny-h.cfg'
    
    
    def program(self, fpath, target):
        
        self.execute((
            self.INTERFACE,
            self.TRANSPORT,
            target.OPENOCD,
            "init",
            "reset halt",
            
            ))
    
    
    
            
        