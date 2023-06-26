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
    
    def __init__(self, owner, oid=None, street=None, number=None, city=None, country=None, zip=None, state=None ):  # @ReservedAssignment
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
        self.boards = []
        self.boardvariants = []
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
            
        for xboard in xelement.findall('board'):
            try:
                cust_board = DbCustomerBoard.fromXml(self,xboard) 
                self.boards.append(cust_board)
            except KeyError as e:
                self.db.app.sayError(str(e))
            
            
    def getKey(self):
        return self.id
        
    def isStandard(self):
        return self.standard
    
    @property
    def key(self):
        return self.getKey()
    
class DbStandardCustomer(DbCustomer):
    standard = True
    
    
        
    
class DbSerialNumber(DbObject):
    
    def __init__(self, owner, oid=None, prefix=None, nbfmt='04d', nbinc=1, suffix=None): 
        super().__init__(owner, oid=oid)
        self._prefix = prefix
        self._suffix = suffix
        self._nbfmt = nbfmt
        self._nbinc = nbinc
        
        
    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        
        xprefix = xelement.find('prefix')
        if xprefix is not None:
            self._prefix = xprefix.text
        
        xnumber = xelement.find('number')
        if xnumber is not None:
            self._nbfmt = xnumber.get('fmt', self._nbfmt)        
            self._nbinc = int(xnumber.get('inc', str(self._nbinc)),0)
        
        xsuffix = xelement.find('suffix')
        if xsuffix is not None:
            self._sufix = xsuffix.text        
        
        
    
class DbCustomerBoard(DbObject):
    
    def __init__(self, owner, oid, board=None): 
        self._board = None
        super().__init__(owner, oid=oid)
        if board:
            self.setBoard(board)
        
    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        self.setBoard(self.db.getBoard(xelement.get('id')))
        for xvariant in xelement.findall('variant'):
            cust_variant = DbCustomerBoardVariant.fromXml(self,xvariant)
            self.customer.boardvariants.append(cust_variant)
        
    def setBoard(self, board):
        self._board = board
        self.setName(board.name)
        
        
    @property
    def board(self):
        return self._board
    
    @property
    def customer(self):
        return self.owner
    
    
class DbCustomerBoardVariant(DbObject):    
    def __init__(self, owner, oid, variant=None): 
        self._variant = None
        super().__init__(owner, oid=oid)
    
    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        self.setVariant(self.db.getBoardVariant(xelement.get('id')))
    
    def setVariant(self, variant):
        self._variant = variant
        self.setName(variant.name)
    
    @property
    def customer(self):
        return self.owner.customer
    
    @property
    def variant(self):
        return self._variant
    