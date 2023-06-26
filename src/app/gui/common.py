'''
Created on Aug 25, 2021

@author: hd
'''

from dapi2.derror import DApiComError
from os.path import os

import app


TIMEOUT_MS = 250
'''GUI timer delay [ms]'''

REFRESH_COUNT_INIT = 2
'''Value for initialize count between 2 refresh'''

REFRESH_ALL_REF_TIME = 0.250
'''Temps de référence pour l'actualisation de tous les registres [s]'''

STANDARD_LAYOUTS = {
    'vantage': os.path.join(app.IMG_DIR, 'layout-vantage.svg'),
    'vantage-dark': os.path.join(app.IMG_DIR, 'layout-vantage-dark.svg'),
    'lipo': os.path.join(app.IMG_DIR, 'layout-lipo.svg'),
    }

   

def UserActionHandler(function):
    
    def wrapper(self, *args, **kwargs):
        if not self.eventsEnabled: return
        self.log.debug(function.__name__+str(args))
        self.disableEvents()            
        try:
            return function(self, *args, **kwargs)
        except DApiComError as e:
            self.handleDApiComError(e)
        except Exception as e:
            self.log.error(f'UserActionHandler : {e!r}')
            self.app.handleError(e)
        finally:
            self.enableEvents()    
            return None
    
    return wrapper


def DisableEvent(function):
    
    def wrapper(self, *args, **kwargs):
        self.disableEvents()
        ret = None
        try:
            ret = function(self, *args, **kwargs)
        finally:
            self.enableEvents()
        return ret
    
    return wrapper

def UserBoardActionHandler(function):
    
    def wrapper(self, *args, **kwargs):
        ret = None
        if not self.eventsEnabled: return
        self.log.debug(function.__name__+str(args))
        self.disableEvents()            
        try:
            ret = function(self, *args, **kwargs)
        except DApiComError as e:
            self.handleDApiComError(e)
        except Exception as e:
            self.handleError(e)
        finally:
            self.enableEvents()    

        self.refresh()
        return ret 

    return wrapper