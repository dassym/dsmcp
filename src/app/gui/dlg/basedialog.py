'''

:author: fv
:date: Created on 3 juin 2021
'''
from PyQt5.QtCore import QCoreApplication
import logging


class BaseDialog(object):
    '''
    classdocs
    '''

    @classmethod
    def tr(cls, text, disambiguation=None, n=-1):
        return QCoreApplication.translate(cls.__name__,text, disambiguation, n)    

    def __init__(self, app):
        '''
        Constructor
        '''
        self.app = app
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug( 'Construct' )
        self._disable_events_cnt = 0
        self._initialized = False
        
    def _initialize(self, **kwargs):
        pass
    
    def _reset(self, **kwargs):
        pass
    
    def initialize(self, app=None, **kwargs):
        self.log.debug('Initialize')
        if app is not None:
            self.app = app
        assert self.app is not None
        self._initialize(**kwargs)
        self._initialized = True
        
    def boardInit(self):
        pass
    
    def onWorkspaceChanged(self, workspace):
        pass
        
    def disableEvents(self):
        '''Disable event processing'''
        self._disable_events_cnt += 1
        return self._disable_events_cnt
    
    def enableEvents(self):
        '''Enable event processing.
        
        For the processing of events to be active, the number of nested calls for deactivation and activation must be equal.
        '''
        if self._disable_events_cnt > 0:
            self._disable_events_cnt -= 1
        return self._disable_events_cnt
    
    def handleError(self, exception):
        '''Handling an error or exception
        :param Exception e: the exception to be processed
        '''
        if self.app is not None:
            self.app.handleError(exception)
        else:
            raise exception
        
        
    def exec(self, **kwargs):
        if not self._initialized:
            self.initialize(**kwargs)
        self._reset(**kwargs)
        return super().exec()
        
        
    @property
    def board(self):
        return self.app.board
    @property
    def dapi(self):
        return self.app.dapi
    @property
    def config(self):
        return self.app.config
    @property
    def lang(self):
        return self.app.lang
    @property
    def db(self):
        return self.app.db
    @property
    def eventsEnabled(self):
        '''The events processing activation status'''
        return self._disable_events_cnt == 0          
    