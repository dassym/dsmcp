# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/app/gui/basic/basicwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BasicWindow(object):
    def setupUi(self, BasicWindow):
        BasicWindow.setObjectName("BasicWindow")
        BasicWindow.resize(568, 476)
        self.centralwidget = QtWidgets.QWidget(BasicWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widgetSpeed = QSpeed(self.centralwidget)
        self.widgetSpeed.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.widgetSpeed.setFrameShadow(QtWidgets.QFrame.Raised)
        self.widgetSpeed.setObjectName("widgetSpeed")
        self.horizontalLayout.addWidget(self.widgetSpeed)
        self.widgetTorque = QTorque(self.centralwidget)
        self.widgetTorque.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.widgetTorque.setFrameShadow(QtWidgets.QFrame.Raised)
        self.widgetTorque.setObjectName("widgetTorque")
        self.horizontalLayout.addWidget(self.widgetTorque)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.frameError = QError(self.centralwidget)
        self.frameError.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameError.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameError.setObjectName("frameError")
        self.verticalLayout.addWidget(self.frameError)
        self.groupBoxMemories = QMemories(self.centralwidget)
        self.groupBoxMemories.setObjectName("groupBoxMemories")
        self.verticalLayout.addWidget(self.groupBoxMemories)
        BasicWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(BasicWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 568, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuSystem = QtWidgets.QMenu(self.menuBar)
        self.menuSystem.setObjectName("menuSystem")
        self.menuMotor = QtWidgets.QMenu(self.menuBar)
        self.menuMotor.setObjectName("menuMotor")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuWorkspace = QtWidgets.QMenu(self.menuBar)
        self.menuWorkspace.setObjectName("menuWorkspace")
        self.menuBoard = QtWidgets.QMenu(self.menuBar)
        self.menuBoard.setObjectName("menuBoard")
        self.menuMemory = QtWidgets.QMenu(self.menuBar)
        self.menuMemory.setObjectName("menuMemory")
        BasicWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(BasicWindow)
        self.statusBar.setObjectName("statusBar")
        BasicWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(BasicWindow)
        self.toolBar.setObjectName("toolBar")
        BasicWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLink = QtWidgets.QAction(BasicWindow)
        self.actionLink.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/32/unlink.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/img/32/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/img/32/link.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/img/32/unlink.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionLink.setIcon(icon)
        self.actionLink.setObjectName("actionLink")
        self.actionMotorStart = QtWidgets.QAction(BasicWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/32/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionMotorStart.setIcon(icon1)
        self.actionMotorStart.setObjectName("actionMotorStart")
        self.actionLightEnabled = QtWidgets.QAction(BasicWindow)
        self.actionLightEnabled.setCheckable(True)
        self.actionLightEnabled.setChecked(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/32/light-off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/img/32/light-on.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon2.addPixmap(QtGui.QPixmap(":/img/32/light-on.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/img/32/light-off.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionLightEnabled.setIcon(icon2)
        self.actionLightEnabled.setObjectName("actionLightEnabled")
        self.actionLightBlue = QtWidgets.QAction(BasicWindow)
        self.actionLightBlue.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/32/light.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/img/32/light-blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon3.addPixmap(QtGui.QPixmap(":/img/32/light-blue.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/img/32/light.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionLightBlue.setIcon(icon3)
        self.actionLightBlue.setObjectName("actionLightBlue")
        self.actionMotorReverse = QtWidgets.QAction(BasicWindow)
        self.actionMotorReverse.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/32/clockwise.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/img/32/counterclockwise.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon4.addPixmap(QtGui.QPixmap(":/img/32/counterclockwise.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/img/32/clockwise.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionMotorReverse.setIcon(icon4)
        self.actionMotorReverse.setObjectName("actionMotorReverse")
        self.actionAbout = QtWidgets.QAction(BasicWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(BasicWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAutoRefresh = QtWidgets.QAction(BasicWindow)
        self.actionAutoRefresh.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/img/32/autorefresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionAutoRefresh.setIcon(icon5)
        self.actionAutoRefresh.setObjectName("actionAutoRefresh")
        self.actionUnlink = QtWidgets.QAction(BasicWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/img/32/unlink.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionUnlink.setIcon(icon6)
        self.actionUnlink.setObjectName("actionUnlink")
        self.actionRefresh = QtWidgets.QAction(BasicWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/img/32/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRefresh.setIcon(icon7)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionHelp = QtWidgets.QAction(BasicWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/img/32/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionHelp.setIcon(icon8)
        self.actionHelp.setObjectName("actionHelp")
        self.actionMotorStop = QtWidgets.QAction(BasicWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/img/32/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionMotorStop.setIcon(icon9)
        self.actionMotorStop.setObjectName("actionMotorStop")
        self.actionFirmReset = QtWidgets.QAction(BasicWindow)
        self.actionFirmReset.setObjectName("actionFirmReset")
        self.actionAPISendFirmware = QtWidgets.QAction(BasicWindow)
        self.actionAPISendFirmware.setObjectName("actionAPISendFirmware")
        self.actionAboutBoard = QtWidgets.QAction(BasicWindow)
        self.actionAboutBoard.setObjectName("actionAboutBoard")
        self.actionMotorMode = QtWidgets.QAction(BasicWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/img/32/parameters.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMotorMode.setIcon(icon10)
        self.actionMotorMode.setObjectName("actionMotorMode")
        self.actionRegistersView = QtWidgets.QAction(BasicWindow)
        self.actionRegistersView.setObjectName("actionRegistersView")
        self.actionConnect = QtWidgets.QAction(BasicWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/img/32/key.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnect.setIcon(icon11)
        self.actionConnect.setObjectName("actionConnect")
        self.actionRebootBoard = QtWidgets.QAction(BasicWindow)
        self.actionRebootBoard.setObjectName("actionRebootBoard")
        self.actionStore = QtWidgets.QAction(BasicWindow)
        self.actionStore.setCheckable(True)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/img/24/memory-set.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStore.setIcon(icon12)
        self.actionStore.setObjectName("actionStore")
        self.menuSystem.addAction(self.actionLink)
        self.menuSystem.addAction(self.actionConnect)
        self.menuSystem.addAction(self.actionRefresh)
        self.menuSystem.addAction(self.actionAutoRefresh)
        self.menuSystem.addSeparator()
        self.menuSystem.addAction(self.actionQuit)
        self.menuMotor.addAction(self.actionMotorMode)
        self.menuMotor.addAction(self.actionMotorStart)
        self.menuMotor.addAction(self.actionMotorStop)
        self.menuMotor.addAction(self.actionLightEnabled)
        self.menuMotor.addAction(self.actionLightBlue)
        self.menuMotor.addAction(self.actionMotorReverse)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionRegistersView)
        self.menuBoard.addAction(self.actionFirmReset)
        self.menuBoard.addAction(self.actionAPISendFirmware)
        self.menuBoard.addAction(self.actionAboutBoard)
        self.menuBoard.addAction(self.actionRebootBoard)
        self.menuMemory.addAction(self.actionStore)
        self.menuBar.addAction(self.menuSystem.menuAction())
        self.menuBar.addAction(self.menuBoard.menuAction())
        self.menuBar.addAction(self.menuWorkspace.menuAction())
        self.menuBar.addAction(self.menuMotor.menuAction())
        self.menuBar.addAction(self.menuMemory.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionLink)
        self.toolBar.addAction(self.actionAutoRefresh)
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addAction(self.actionConnect)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMotorStart)
        self.toolBar.addAction(self.actionMotorStop)
        self.toolBar.addAction(self.actionMotorReverse)
        self.toolBar.addAction(self.actionLightEnabled)
        self.toolBar.addAction(self.actionLightBlue)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMotorMode)
        self.toolBar.addSeparator()

        self.retranslateUi(BasicWindow)
        self.actionQuit.triggered.connect(BasicWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(BasicWindow)

    def retranslateUi(self, BasicWindow):
        _translate = QtCore.QCoreApplication.translate
        BasicWindow.setWindowTitle(_translate("BasicWindow", "DsmCP - Basic"))
        self.groupBoxMemories.setTitle(_translate("BasicWindow", "Memories"))
        self.menuSystem.setTitle(_translate("BasicWindow", "System"))
        self.menuMotor.setTitle(_translate("BasicWindow", "Motor"))
        self.menuHelp.setTitle(_translate("BasicWindow", "Help"))
        self.menuWorkspace.setTitle(_translate("BasicWindow", "Workspace"))
        self.menuBoard.setTitle(_translate("BasicWindow", "Board"))
        self.menuMemory.setTitle(_translate("BasicWindow", "Memory"))
        self.toolBar.setWindowTitle(_translate("BasicWindow", "toolBar"))
        self.actionLink.setText(_translate("BasicWindow", "Link"))
        self.actionLink.setToolTip(_translate("BasicWindow", "Link DCP to board"))
        self.actionMotorStart.setText(_translate("BasicWindow", "Start"))
        self.actionMotorStart.setToolTip(_translate("BasicWindow", "Start the motor"))
        self.actionMotorStart.setShortcut(_translate("BasicWindow", "F2"))
        self.actionLightEnabled.setText(_translate("BasicWindow", "Light Enabled"))
        self.actionLightEnabled.setToolTip(_translate("BasicWindow", "Enable/disable Light"))
        self.actionLightEnabled.setShortcut(_translate("BasicWindow", "F4"))
        self.actionLightBlue.setText(_translate("BasicWindow", "BlueLight"))
        self.actionLightBlue.setToolTip(_translate("BasicWindow", "Switch white / blue light"))
        self.actionLightBlue.setShortcut(_translate("BasicWindow", "F9"))
        self.actionMotorReverse.setText(_translate("BasicWindow", "Reverse"))
        self.actionMotorReverse.setToolTip(_translate("BasicWindow", "Reverses the motor rotation direction"))
        self.actionMotorReverse.setShortcut(_translate("BasicWindow", "F7"))
        self.actionAbout.setText(_translate("BasicWindow", "About ..."))
        self.actionAbout.setShortcut(_translate("BasicWindow", "Ctrl+F1"))
        self.actionQuit.setText(_translate("BasicWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("BasicWindow", "Ctrl+Q"))
        self.actionAutoRefresh.setText(_translate("BasicWindow", "AutoRefresh"))
        self.actionUnlink.setText(_translate("BasicWindow", "Unlink"))
        self.actionUnlink.setToolTip(_translate("BasicWindow", "Unlink DCP from board"))
        self.actionRefresh.setText(_translate("BasicWindow", "Refresh"))
        self.actionRefresh.setToolTip(_translate("BasicWindow", "Refresh"))
        self.actionRefresh.setShortcut(_translate("BasicWindow", "F5"))
        self.actionHelp.setText(_translate("BasicWindow", "Help"))
        self.actionHelp.setShortcut(_translate("BasicWindow", "F1"))
        self.actionMotorStop.setText(_translate("BasicWindow", "Stop"))
        self.actionMotorStop.setToolTip(_translate("BasicWindow", "Stop the motor"))
        self.actionMotorStop.setShortcut(_translate("BasicWindow", "F3"))
        self.actionFirmReset.setText(_translate("BasicWindow", "Frimware Reset..."))
        self.actionFirmReset.setToolTip(_translate("BasicWindow", "Reset the firmware settings"))
        self.actionAPISendFirmware.setText(_translate("BasicWindow", "Send Firmware..."))
        self.actionAboutBoard.setText(_translate("BasicWindow", "About board..."))
        self.actionMotorMode.setText(_translate("BasicWindow", "Motor mode..."))
        self.actionMotorMode.setToolTip(_translate("BasicWindow", "Show motor mode dialog"))
        self.actionMotorMode.setShortcut(_translate("BasicWindow", "F10"))
        self.actionRegistersView.setText(_translate("BasicWindow", "Registers view"))
        self.actionRegistersView.setShortcut(_translate("BasicWindow", "Shift+F1"))
        self.actionConnect.setText(_translate("BasicWindow", "Connect..."))
        self.actionConnect.setToolTip(_translate("BasicWindow", "Connect"))
        self.actionRebootBoard.setText(_translate("BasicWindow", "Reboot"))
        self.actionRebootBoard.setToolTip(_translate("BasicWindow", "Reboot the board"))
        self.actionStore.setText(_translate("BasicWindow", "Store"))
from ..widget.qerror import QError
from ..widget.qmemories import QMemories
from ..widget.qspeed import QSpeed
from ..widget.qtorque import QTorque
from .res import img_rc
