'''

:author: fv
:date: Created on 24 juin 2022
'''



class BaseMcuTarget(object):
    NAME = None
    
    
class Stm32f1xx(object):
    NAME = "STM32F1xx"
    OPENOCD = 'script target/stm32f1x.cfg'
     



class McuProgrammer(object):
    
    def __init__(self, interface, target):
        self._interface = interface
        self._target = target

        
        
    def writeFirmware(self, firmware):
        pass
    
    
    def writeBinary(self, path):
        pass
        