'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.Qt import QIcon, QPixmap, Qt, QDialogButtonBox, QDate
from PyQt5.QtWidgets import QDialog, QLabel
from dapi2 import DApiAccessLevel, SystemModeConfig

from ...base import BaseApp
from ..common import UserActionHandler
from ..res import SystemModeConfigIcon
from .basedialog import BaseDialog
from .ui_aboutboarddialog import Ui_AboutBoardDialog


class AboutBoardDialog(BaseDialog, QDialog, Ui_AboutBoardDialog ):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        BaseDialog.__init__(self, parent.app)
        self.setupUi(self)
        self.buttonApply = None
        self._systemModeConfigLabels = {}
        
        for i, config in enumerate(SystemModeConfig):
            o = QLabel(self)
            if SystemModeConfigIcon[config] is not None:
                o.setPixmap(QIcon(SystemModeConfigIcon[config]).pixmap(48,48, QIcon.Disabled))
            else:
                o.setText(config.shortname)
            o.setToolTip("#{0:2d}:{1:s}".format(i,config.help))
            o.setObjectName('labelSystemModeConfig'+config.name)
            self.gridLayoutConfig.addWidget( o, i % 2, i // 2, 1, 1)
            self._systemModeConfigLabels[config] = o
        
        
    def _update(self):
        self.log.debug('_update')
        self.labelBoardName.setText(self.board.getName())
        data = self.board.getFactoryData()
        firm_version = self.board.getFirmwareVersion()
        firm_tag = self.board.getFirmwareTag()
        firm_date = self.board.getFirmwareDate()
        self.lineEditSerialNumber.setText("{0:05d}".format(data[0]))
        if data[1]:
            self.dateEditFactoryDate.setDate(QDate(data[1]))
        firm = self.db.firmwares.get(
                        type(self.board),
                        tag=firm_tag,
                        version=firm_version, 
                        date=firm_date
                        )
        if firm is not None:
            self.labelFirmware.setText('v<b>{sv[0]:d}.{sv[1]:02d}</b> – {f!s}'.format(sv=firm_version, f=firm))
        else:
            self.labelFirmware.setText("v<b>{sv[0]:d}.{sv[1]:02d}</b> – undefined {fd:s} 0x{ft:04x}".format(sv=firm_version, ft=firm_tag, fd=firm_date.isoformat()))

        rimg = ":/img/board/{0:s}.png".format(self.board.getName().lower())
        self.labelImage.setPixmap(
            QPixmap(rimg).scaled(self.labelImage.minimumSize(),  Qt.KeepAspectRatio, Qt.SmoothTransformation) 
            )


        self.labelAccess.setText(self.board.getAccessLevel().name)

        cfg = self.board.getSystemModeConfiguration()
        self.groupBoxModeConfig.setTitle('Mode configuration (0x{0:04x})'.format(cfg.value))
        for i, config in enumerate(SystemModeConfig):
            o =  self._systemModeConfigLabels[config]
            if cfg & config != 0:
                if SystemModeConfigIcon[config] is not None:
                    o.setPixmap(QIcon(SystemModeConfigIcon[config]).pixmap(48,48, QIcon.Normal))
                else:
                    o.setText(config.shortname)
                o.setToolTip("#{0:2d}:{1:s}:YES".format(i,config.help))
            else:
                if SystemModeConfigIcon[config] is not None:
                    o.setPixmap(QIcon(SystemModeConfigIcon[config]).pixmap(48,48, QIcon.Disabled))
                else:
                    o.setText('¬'+config.shortname)
                o.setToolTip("#{0:2d}:{1:s}:NO".format(i,config.help))
                
        ab = self.board.getAdditionalBoard()
        self.labelAdditionalBoard.setText(BaseApp.tr("Additional board: ") + ab.descr)
        rst = self.board.getLastReset()
        self.labelReset.setText(BaseApp.tr("Reset reason: ") + rst.descr)
        wd = self.board.getPeripheralWatchdog()
        self.labelPeripheralWatchdog.setText(BaseApp.tr('Peripheral watchdog :')+ (BaseApp.tr('enabled') if wd else BaseApp.tr('disabled')))
        wd = self.board.getIndependentWatchdog()
        self.labelIndependentWatchdog.setText(BaseApp.tr('Independent watchdog :')+ (BaseApp.tr('enabled') if wd else BaseApp.tr('disabled')))

        
    def _initialize(self):
        if self.board:
            if self.board.getAccessLevel() >= DApiAccessLevel.SERVICE:
                self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Reset)
                self.lineEditSerialNumber.setReadOnly(False)
                self.dateEditFactoryDate.setReadOnly(False)
                self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect( self.onReset )
                self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect( self.onOk )
            else:
                self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
                self.lineEditSerialNumber.setReadOnly(True)
                self.dateEditFactoryDate.setReadOnly(True)                
            self._update()
    
    def exec(self):
        self.initialize()
        return super().exec()
        
    @property
    def sn(self):
        return int(self.lineEditSerialNumber.text()) 
    @property
    def fd(self):
        return self.dateEditFactoryDate.date().toPyDate() 
    
    @UserActionHandler
    def onReset(self, button):
        self._update()        
        
    @UserActionHandler
    def onOk(self, button):
        self.board.setFactoryData(self.sn, self.fd)        
        
        