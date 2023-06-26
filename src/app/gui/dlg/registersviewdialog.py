'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.Qt import QAbstractItemModel, QModelIndex, QVariant, Qt, QStyledItemDelegate, QFont, QHeaderView,\
    QColor, QBrush
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
import logging

from dapi2.dreg.register import RegisterArray, BitFieldRegister, Register, DRegType
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

    def root(self):
        return self.parentItem.root()

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

    def init_tree(self, dboard=None):
        pass

    @property
    def lang(self):
        return self.parent().lang


class TreeItemRegisters(TreeItemModel):

    def __init__(self, registers, lang=None, dboard=None):
        self._dboard = None
        self._lang = lang
        TreeItemModel.__init__(self, registers, None)
        if dboard:
            self.init_tree(dboard)

    def init_tree(self, dboard=None):
        assert self.itemData is not None
        self._dboard = dboard
        for group in self.itemData.groups.values():
            if dboard and group.name in dboard.REG_GROUPS:
                item = TreeItemGroup(group, self)
                item.init_tree(dboard)

    def clear(self):
        self.childItems.clear()

    def root(self):
        return self

    @property
    def lang(self):
        return self._lang
    @property
    def dboard(self):
        return self._dboard
    @property
    def registers(self):
        return self.itemData

class TreeItemBitRegister(TreeItemModel):

    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(self.itemData.name)
            elif column == 1:
                return QVariant(self.itemData.addr)
            elif column == 2:
                return QVariant(self.itemData.size)
            elif column == 3 and self.itemData.parent.isDefined():
                return QVariant(f'{{0:0{self.itemData.size}b}}'.format(self.itemData.value))
            elif column == 4 and self.itemData.parent.isDefined():
                return QVariant('{0:d}'.format(self.itemData.value))
            elif column == 5:
                return QVariant(self.itemData.getDescription(self.lang))
        elif role == Qt.TextAlignmentRole:
            if 1 <= column <= 4:
                return Qt.AlignRight
        elif role == Qt.ForegroundRole:
            return self.parent().data(column, role)


class TreeItemRegister(TreeItemModel):

    def init_tree(self, dboard=None):
        if isinstance(self.itemData, BitFieldRegister):
            for bit in self.itemData.bits:
                item = TreeItemBitRegister(bit, self)
                item.init_tree(dboard)

    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(self.itemData.name)
            elif column == 1:
                return QVariant('0x{0:02x}'.format(self.itemData.addr))
            elif column == 3 and self.itemData.isDefined():
                return QVariant('0x{0:04x}'.format(self.itemData.value))
            elif column == 4 and self.itemData.isDefined():
                return QVariant('{0:d}'.format(self.itemData.value))
            elif column == 5:
                #return QVariant("{0!s} - {1!s}".format(self.itemData.getDescription(self.lang) or '', self.itemData.rtype))
                return QVariant(self.itemData.getDescription(self.lang))
        elif role == Qt.TextAlignmentRole:
            if column == 4:
                return Qt.AlignRight
        elif role == Qt.ForegroundRole:
            if self.itemData.rtype == DRegType.WORKSPACE:
                if self.root().dboard and self.root().dboard.isOnStandby() and self.itemData.value != 0:
                    return QBrush(QColor('red'))
                else:
                    return QBrush(QColor('blue'))



class TreeItemRegArray(TreeItemModel):

    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(self.itemData.name)
            elif column == 1:
                return QVariant('0x{0:02x}'.format(self.itemData.addr))
            elif column == 2:
                return QVariant(len(self.itemData))
            elif column == 5:
                return QVariant(self.itemData.getDescription(self.lang))
        elif role == Qt.TextAlignmentRole:
            if column == 4:
                return Qt.AlignRight

    def init_tree(self, dboard=None):
        for reg in self.itemData:
            item = TreeItemRegister(reg, self)
            item.init_tree(dboard)

class TreeItemGroup(TreeItemModel):

    def init_tree(self, dboard=None):
        for reg in self.itemData:
            if isinstance(reg, RegisterArray):
                item = TreeItemRegArray(reg, self)
            else:
                item = TreeItemRegister(reg, self)
            item.init_tree(dboard)

    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(self.itemData.name)
            elif column == 1:
                return QVariant('0x{0:02x}'.format(self.itemData.addr))
            elif column == 2:
                return QVariant(self.itemData.size)
            elif column == 5:
                return QVariant(self.itemData.getDescription(self.lang))
        elif role == Qt.TextAlignmentRole:
            if column == 4:
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

    def __init__(self, dapi=None, parent=None, dboard=None ):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug( 'Initialize' )
        self.dapi = dapi
        self.dboard = dboard
        self.registers = dapi and dapi.regs or None
        self._header = [
                RegistersViewDialog.tr('Name'),
                RegistersViewDialog.tr('Addr'),
                RegistersViewDialog.tr('Size'),
                RegistersViewDialog.tr('Hex. value'),
                RegistersViewDialog.tr('Dec. value'),
                RegistersViewDialog.tr('Description')
            ]
        QAbstractItemModel.__init__(self,parent)
        self.log.debug( 'Create TreeItemRegisters lang='+str(parent.lang) )
        self.root = TreeItemRegisters(self.registers, parent.lang)
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
        item = index.internalPointer()
        ret = item.data(index.column(), role)
        #ret = item.data(index, role)
        return ret

    def setData(self, *args, **kwargs):
        return QAbstractItemModel.setData(self, *args, **kwargs)

    def get_data(self, index, role=None):
        if index.isValid():
            item = index.internalPointer()
            return item.itemData
        return None


    def setBoard(self, dboard):
        self.dboard = dboard
        self.root.clear()
        self.init_tree()


    def init_tree(self):
        self.root.init_tree(self.dboard)

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

        self.buttonRefresh = self.buttonBox.addButton("Refresh", QDialogButtonBox.ActionRole)
        self.buttonRefresh.clicked.connect(self.onRefreshClicked)
        self.treeView.setItemDelegate(FontDelegate(self))
        self.treeView.resizeColumnToContents(0)
        self.treeView.header().setSectionResizeMode(QHeaderView.ResizeToContents)



    def _initialize(self):
        self.registers_model = QRegistersTreeModel(self.dapi, self)
        self.treeView.setModel(self.registers_model)
        self.treeView.resizeColumnToContents(0)
        self.treeView.header().setStretchLastSection(True)
        self.treeView.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.treeView.selectionModel().selectionChanged.connect(self.onSelectionChanged)

    def boardInit(self):
        self.registers_model.setBoard(self.board)




    def onRefreshClicked(self):
        self.log.debug('onRefreshClicked')
        regs = []
        sel = self.treeView.selectionModel().selectedRows()
        self.registers_model.layoutAboutToBeChanged.emit()
        for idx in sel:
            idx0 = self.registers_model.index(idx.row(), 3)
            idx1 = self.registers_model.index(idx.row(), 4)
            reg = self.registers_model.get_data(idx)
            regs.append(reg)
            self.registers_model.dataChanged.emit(idx0, idx1,(Qt.DisplayRole, Qt.DecorationRole, Qt.BackgroundRole, ))
        self.board.getRegisters(*regs, refresh=True)
        self.registers_model.layoutChanged.emit()


    def onCurrentChanged(self, current, previous):
        self.log.debug('onCurrentChanged')


    def onSelectionChanged(self, selected, deselected):
        self.log.debug('onSelectionChanged')
        sel = self.treeView.selectionModel().selectedRows()
        regs = []
        self.registers_model.layoutAboutToBeChanged.emit()
        for idx in sel:
            reg = self.registers_model.get_data(idx)
            if isinstance(reg, Register) and reg.isUndefined():
                regs.append(reg)
                idx0 = self.registers_model.index(idx.row(), 3)
                idx1 = self.registers_model.index(idx.row(), 4)
                self.registers_model.dataChanged.emit(idx0, idx1,(Qt.DisplayRole, Qt.DecorationRole, Qt.BackgroundRole, ))
        self.board.getRegisters(*regs, refresh=True)
        self.registers_model.layoutChanged.emit()



        #for idx in sel:
            #self.registers_model.setData(idx, None, Qt.UserRole)
            #self.treeView.update(idx)





