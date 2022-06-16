'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.Qt import QAbstractItemModel, QModelIndex, QVariant, Qt, QStyledItemDelegate, QFont, QHeaderView, \
    QCoreApplication
from PyQt5.QtWidgets import QDialog
from dapi2.dreg.register import RegisterArray, BitFieldRegister
import logging

from .basedialog import BaseDialog
from .ui_registersviewdialog import Ui_RegistersViewDialog


class TreeItemModel(object):
    def __init__(self, data, parent=None):
        self.parentItem = None
        self.itemData = data
        self.childItems = []
        if parent is not None:
            parent.appendChild(self)

    def appendChild(self, item):
        self.childItems.append(item)
        item.parentItem = self

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 6

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

    def init_tree(self):
        pass
    
    @property
    def lang(self):
        return self.parent().lang

        
class TreeItemRegisters(TreeItemModel):
    
    def __init__(self, data, lang=None):
        self._lang = lang
        TreeItemModel.__init__(self, data, None)
        
    def init_tree(self):
        for group in self.itemData.groups.values():
            item = TreeItemGroup(group, self)
            item.init_tree()
        
    @property
    def lang(self):
        return self._lang        

class TreeItemBitRegister(TreeItemModel):
    
    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(self.itemData.name)
            elif column == 1:
                return QVariant(self.itemData.addr)
            elif column == 2:
                return QVariant(self.itemData.size)
            elif column == 3:
                return QVariant(self.itemData.getDescription(self.lang))
        elif role == Qt.TextAlignmentRole:
            if 1 <= column <= 2:
                return Qt.AlignRight
                
        
class TreeItemRegister(TreeItemModel):
    
    def init_tree(self):
        if isinstance(self.itemData, BitFieldRegister):
            for bit in self.itemData.bits:
                item = TreeItemBitRegister(bit, self)
                item.init_tree()
            
    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(self.itemData.name)
            elif column == 1:
                return QVariant('0x{0:02x}'.format(self.itemData.addr))
            elif column == 3:
                return QVariant(self.itemData.getDescription(self.lang))
        elif role == Qt.TextAlignmentRole:
            if column == 2:
                return Qt.AlignRight
            

class TreeItemRegArray(TreeItemModel):

    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(self.itemData.name)
            elif column == 1:
                return QVariant('0x{0:02x}'.format(self.itemData.addr))
            elif column == 2:
                return QVariant(len(self.itemData))
            elif column == 3:
                return QVariant(self.itemData.getDescription(self.lang))
        elif role == Qt.TextAlignmentRole:
            if column == 2:
                return Qt.AlignRight                
    
    def init_tree(self):
        for reg in self.itemData:
            item = TreeItemRegister(reg, self)
            item.init_tree()

class TreeItemGroup(TreeItemModel):

    def init_tree(self):
        for reg in self.itemData:
            if isinstance(reg, RegisterArray):
                item = TreeItemRegArray(reg, self)
            else:
                item = TreeItemRegister(reg, self)
            item.init_tree()
            
    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(self.itemData.name)
            elif column == 1:
                return QVariant('0x{0:02x}'.format(self.itemData.addr))
            elif column == 2:
                return QVariant(self.itemData.size)
            elif column == 3:
                return QVariant(self.itemData.getDescription(self.lang))
        elif role == Qt.TextAlignmentRole:
            if column == 2:
                return Qt.AlignRight            
        

class FontDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # decide here if item should be bold and set font weight to bold if needed
        if isinstance(index.internalPointer(),TreeItemGroup):  
            option.font.setWeight(QFont.Bold)
        if isinstance(index.internalPointer(),TreeItemBitRegister):  
            option.font.setWeight(QFont.StyleItalic)
        QStyledItemDelegate.paint(self, painter, option, index)

class QRegistersTreeModel(QAbstractItemModel):
    
    def __init__(self, registers=None, parent=None ):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug( 'Initialize' )
        self.registers = registers
        self._header = [
                RegistersViewDialog.tr('Name'),
                RegistersViewDialog.tr('Addr'),
                RegistersViewDialog.tr('Size'),
                RegistersViewDialog.tr('Description')
            ]
        QAbstractItemModel.__init__(self,parent)
        self.log.debug( 'Create TreeItemRegisters lang='+str(parent.lang) )
        self.root  = TreeItemRegisters(self.registers, parent.lang)
        self.init_tree()
        
        
    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.root
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()
        
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        if childItem is None:
            return QModelIndex() 
        parentItem = childItem.parentItem
        if parentItem == self.root or parentItem is None:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)
        
    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.root
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()
    
    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(self._header)
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole: 
            if orientation == Qt.Horizontal:
                return QVariant(self._header[section])
        return None  
    
    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()
        item = index.internalPointer();
        return item.data(index.column(), role);
    
    def get_data(self, index):
        if index.isValid():
            return self._data[index.row()]
        return None
    
    def init_tree(self):
        self.root.init_tree()
        
    def flags(self, index):
        if not index.isValid():
            return 0
        return QAbstractItemModel.flags(self,index)   


class RegistersViewDialog(BaseDialog, QDialog, Ui_RegistersViewDialog): 
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        BaseDialog.__init__(self, parent.app)
        self._registers = None
        self.setupUi(self)
        
        self.treeView.setItemDelegate(FontDelegate(self))
        self.treeView.resizeColumnToContents(0)
        self.treeView.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        
    def _initialize(self):
        self.registers_model = QRegistersTreeModel(self.dapi.regs, self)
        self.treeView.setModel(self.registers_model)
        self.treeView.resizeColumnToContents(0)
        self.treeView.header().setStretchLastSection(True)
        self.treeView.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        
        
        