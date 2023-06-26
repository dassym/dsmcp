from argparse import Namespace

from .common import VERBOSITY


class TellerInterface():
    '''Class offering facilities for displaying messages on the command line.'''
    
    def __init__(self):
        if not hasattr(self, 'config'):
            self.config = Namespace(verbosity=4)
        if not hasattr(self, 'log_to_file'):
            self.log_to_file = False
        

    def say(self, level, text):
        '''Display text on stdout
        
        Args:
            level (VERBOSITY): The level needed to display this text.
            text (str): Text to display.
            
        Returns:
            True, if the text was displayed.
        '''
        ret = False
        if self.config.verbosity >= level:
            print( text )
            ret = True
            if self.log_to_file:
                if level >= VERBOSITY.MEDIUM:
                    self.log.debug( text )
                else:
                    self.log.info( text )
        else:
            if level >= VERBOSITY.MEDIUM:
                self.log.debug( text )
            else:
                    self.log.info( text )
        return ret
        
    def sayMinimal(self, text):
        return self.say(VERBOSITY.MINIMAL, text)
    
    def sayLow(self, text):
        return self.say(VERBOSITY.LOW, text)
    
    def sayMedium(self, text):
        return self.say(VERBOSITY.MEDIUM, text)
    
    def sayHigh(self, text):
        return self.say(VERBOSITY.HIGH, text)
      
    def sayError(self, text):
        ret = False
        if self.config.verbosity >= VERBOSITY.MINIMAL or self.isCli():
            print( self.tr('ERROR:')+str(text) )
            ret = True
            if self.log_to_file:
                self.log.error(text)
        else:
            self.log.error(text)
        return ret
            
    def sayWarning(self, text):
        ret = False
        if self.config.verbosity >= VERBOSITY.MINIMAL or self.isCli():
            print( self.tr('WARNING:')+str(text) )
            ret = True
            if self.log_to_file:
                self.log.warning(text)
        else:
            self.log.warning(text)
        return ret        
            
