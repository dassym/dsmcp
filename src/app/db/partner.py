'''

:author:  F. Voillat
:date: 2022-06-03 Creation
:copyright: Dassym SA 2021
'''
from pathlib import Path

from .base import DbObject


class DbCountry(DbObject):
    pass        

class DbAddress(DbObject):
    
    def __init__(self, owner, oid=None, street=None, number=None, city=None, country=None, zip=None, state=None ): 
        super().__init__(owner, oid=oid)
        self.street = None
        self.number = None
        self.street2 = None
        self.city = None
        self.country = None
        self.zip = None
        self.city = None
        self.state = None
        
    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        self.street = xelement.find('street').text
        xnumber = xelement.find('number')
        if xnumber is not None: 
            self.number = xnumber.text
        xstreet2 = xelement.find('street2')
        if xstreet2 is not None: 
            self.street2 = xstreet2.text
        self.zip = xelement.find('zip').text
        self.city = xelement.find('city').text
        xstate = xelement.find('state')
        if xstate is not None: 
            self.state = xstate.text
        xcountry = xelement.find('country')
        if xcountry is not None: 
            self.country = DbCountry.fromXml(self, xcountry)

class DbCustomer(DbObject):
    
    standard = False
    
    def __init__(self, owner, oid, name=None, address=None, logo=None): 
        self.address = address
        self.logo = logo
        super().__init__(owner, oid=oid)
        self.setName(name)
        
    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        self.brand = xelement.find('brand').text
        xaddr = xelement.find('addr')
        if xaddr is not None:
            self.address = DbAddress.fromXml(self, xaddr)
        
        xlogo = xelement.find('logo')
        if xlogo is not None:
            s = xlogo.text
            s.strip()
            path = Path(s) 
            if path.name == s:
                path = self.db.getCurrentLoadingPath().parent.joinpath(path)  
            self.logo = path
            
    def getKey(self):
        return self.id
        
    def isStandard(self):
        return self.standard
    
    @property
    def key(self):
        return self.getKey()
    
class DbStandardCustomer(DbCustomer):
    standard = True
    
    