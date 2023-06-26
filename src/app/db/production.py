'''

:author:  F. Voillat
:date: 2022-10-17 Creation
:copyright: Dassym SA 2021
'''


from pathlib import Path
from serialnumbers import SerialNumber, SerialNumberList, SerialNumberRange
from .base import DbObject
 


class DbManufacturingOrder(DbObject):
    def __init__(self, owner, oid ): 
        super().__init__(owner, oid=oid)
        self.snRanges = SerialNumberList()
        self.qty = None
        self.produced = None
    
    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        self.qty = xelement.get('qty', 1)
        self.produced = xelement.get('produced', 0)
        for xsn in xelement.findall('sn'):
            self.snRanges.addRange(SerialNumberRange.fromString(xsn.text))
        
    @property
    def board(self):
        return self.owner.board
    
    @property
    def customer(self):
        return self.owner.customer
    
class DbBoardProduction(DbObject):
    
    def __init__(self, owner, oid, board=None, customer=None): 
        super().__init__(owner, oid=oid)
        self.board = board
        self.customer = customer
        self.lastSn = None
        self.order = None
        
        
    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        bid, cid = xelement.get('id').split(':')
        self.board = self.db.getBoard(bid)
        self.customer = self.db.getCustomer(cid)
        xlastsn = xelement.find('last-sn')
        if xlastsn is not None:
            self.lastSn = SerialNumber(xlastsn.text)
        xorder = xelement.find('order')
        if xorder is not None:
            self.order = DbManufacturingOrder.fromXml(self, xorder)
        
        
    
