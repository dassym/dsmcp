'''

:author: fv
:date: Created on 24 juin 2022
'''

class BaseMcuInterface(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    
    def setUp(self):
        assert False, 'Abstract method!'
    
    
    def execute(self):
        assert False, 'Abstract method!'
        

    def tearDown(self):
        assert False, 'Abstract method!'
        
        
class BaseInternalMcuInterface(BaseMcuInterface):
    pass        

class BaseExternalMcuInterface(BaseMcuInterface):
    
    EXEC = None
    
    