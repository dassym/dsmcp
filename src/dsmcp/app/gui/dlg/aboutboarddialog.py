'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.QtWidgets import QDialog
import logging

from .ui_aboutboarddialog import Ui_AboutBoardDialog 
from PyQt5.Qt import QIcon, QPixmap, Qt, QLabel
from app.gui.res import SystemModeConfigIcon
from dboard import SystemModeConfig

class AboutBoardDialog(QDialog, Ui_AboutBoardDialog):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.app = parent.app
        self._board = None
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug( 'Initialize' )
        self.setupUi(self)
        
        self.labelFactoryDateIcon.setPixmap(QIcon(':/img/factory-date.svg').pixmap(32,32) )
        self.labelSnIcon.setPixmap(QIcon(':/img/sn.svg').pixmap(32,32))
        self.labelFirmwareIcon.setPixmap(QIcon(':/img/firmware.svg').pixmap(32,32))
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
        self.labelBoardName.setText(self._board.getName())
        data = self._board.getFactoryData()
        firm_version = self._board.getFirmwareVersion()
        firm_tag = self._board.getFirmwareTag()
        firm_date = self._board.getFirmwareDate()
        self.labelSerialNumber.setText("{0:05d}".format(data[0]))
        self.labelFactoryDate.setText(data[1].isoformat())
        firm = self.app.firmwares.get(
                        self._board,
                        firm_tag,
                        firm_version, 
                        firm_date
                        )
        if firm is not None:
            self.labelFirmware.setText('v<b>{sv[0]:d}.{sv[1]:02d}</b> – {f!s}'.format(sv=firm_version, f=firm))
        else:
            self.labelFirmware.setText("v<b>{sv[0]:d}.{sv[1]:02d}</b> – undefined {fd:s} 0x{ft:04x}".format(sv=firm_version, ft=firm_tag, fd=firm_date.isoformat()))

        rimg = ":/img/board/{0:s}.png".format(self._board.getName().lower())
        self.labelImage.setPixmap(
            QPixmap(rimg).scaled(self.labelImage.minimumSize(),  Qt.KeepAspectRatio, Qt.SmoothTransformation) 
            )


        cfg = self._board.getSystemModeConfiguration()
        self.groupBoxConfig.setTitle('Configuration (0x{0:04x})'.format(cfg.value))
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
        
        
    def setBoard(self, board):
        self._board = board
        self._update() 
    
