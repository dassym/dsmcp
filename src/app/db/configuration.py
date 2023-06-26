'''

:author: fv
:date: Created on 24 août 2022
'''


import dapi2
from .base import DbObject

class DbConfiguration(DbObject):
    '''
    classdocs
    '''
    
    @classmethod
    def fromFile(cls, fpath):
        pass 

    def __init__(self, owner, oid=None):
        '''
        Constructor
        '''
        super().__init__(owner, oid=oid)
        