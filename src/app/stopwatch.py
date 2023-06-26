'''

:author: fv
:date: Created on 29 janv. 2022
'''
import time


class Stopwatch(object):
    '''Class allowing to time the time between 2 execution points.
    
    :param autostart bool: If True, automatically starts the stopwatch after initialization.
    
    '''
    

    def __init__(self, autostart=False):
        '''Constructor'''
        self._start_time = None
        '''Start time of stopwatch'''
        self._time = None
        '''Measured time between start and stop'''
        
        if autostart:
            self.start()
        
        
    def start(self):
        '''Starts the stopwatch'''
        
        self._start_time = time.perf_counter()
        self._time = None
        
    def stop(self):
        '''Stops the stopwatch and return the elapsed time.
        
        :return: The elapsed time in second [s]
        :rtype: float
        '''
        try:
            self._time = time.perf_counter() - self._start_time 
            self._start_time = None
            return self._time
        except TypeError:
            raise Exception('Chronometer is not running. Use .start() to start it')
        
    def get(self):
        '''Gets the actual elapsed time
        :return: The actual elapsed time in second [s].
        :rtype: float
        '''
        try:
            return time.perf_counter() - self._start_time 
        except TypeError:
            raise Exception('Chronometer is not running. Use .start() to start it')
        
    @property
    def time(self):
        '''The elapsed time in second [s]'''
        return self._time