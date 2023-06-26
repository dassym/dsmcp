'''

:author:  F. Voillat
:date: 2022-06-03 Creation
:copyright: Dassym SA 2021
'''

import logging



from ..utils import getXmlName, getXmlDescr


class DbObject(object):
    
    @classmethod
    def fromXml(cls, owner, xelement, oid=None):
        if xelement is None:
            return None
        obj = cls(owner, oid=oid)
        obj._initFromXml(xelement)
        return obj 
   
    def __init__(self, owner, oid=None):
        self._log = logging.getLogger(self.__class__.__name__)
        self._owner = owner
        self._id = None
        self._name = None
        self.descr = None
        if self._id is None:
            self.setId(oid)
        
        
    def __str__(self):
        try:
            return f"{self.__class__.__name__!s}[{self.id!r}]"
        except:
            return object.__str__(self)
        
    def _initFromXml(self, xelement):
        if self._id is None:
            self.setId(xelement.get('id'))
        self._name = getXmlName(xelement, self.db.lang)
        self.descr = getXmlDescr(xelement, self.db.lang)
        if self._name is None and self.id is not None:
            self._name = f"{self.__class__.__name__} {self.id!s}"
        self.log.name = f"{self.__class__.__name__}[{self.id!s}]"
        #self.log.debug(f'{self.name} initialized from XML // {id(self)}')        
    # def __bool__(self):
    #     return self._id is not None 
        
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id
    
    def __lt__(self, other):
        return isinstance(other, type(self)) and self.id < other.id
    
    def __str__(self):
        try:
            return self.name or str(self.id)
        except:
            super().__str__()

    def child(self, index):
        return None
    
    def childCount(self):
        return 0
    
    def setId(self, oid):
        # if isinstance(oid, str):
        #     self._id = oid.upper()
        # else:
        self._id = oid
            
    def setOwner(self, owner):
        self._owner = owner
    
    def setName(self, name):
        self._name = name
        
    def getId(self):
        return self._id
    
    def getName(self):
        return self._name
    
    @property
    def id(self):
        return self.getId()
    @property
    def name(self):
        return self.getName()
    @property
    def owner(self):
        return self._owner
    @property
    def parent(self):
        return self._owner
    @property
    def db(self):
        return self._owner.db
    @property
    def log(self):
        return self._log
    
    
# class DbVersionedObject(DbObject):
#
#     def __init__(self, owner, oid=None, version=None, date=None, obsolete=None): 
#         self.obsolete = obsolete
#         self.version = version
#         self.date = date
#         super().__init__(owner, oid=oid )
#
#     def __eq__(self, other):
#         assert other is None or isinstance(other, DbVersionedObject)
#         return other is not None and self.id == other.id and self.version == other.version    
#
#     def __lt__(self, other):
#         assert isinstance(other, DbVersionedObject)
#         return self.id < other.id or (self.id == other.id and self.version < other.version)    
#
#     def _initFromXml(self, xelement):
#         super()._initFromXml(xelement)
#         self.version = str2version(xelement.get('version'))
#         self.obsolete = str2bool(xelement.get('obsolete'))
#         if 'date' in xelement.keys():
#             self.date = DT.datetime.strptime(xelement.get('date'), '%Y-%m-%d').date() 
    
    