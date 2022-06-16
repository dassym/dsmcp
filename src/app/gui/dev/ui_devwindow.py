# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/app/gui/dev/devwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from ..widget.qactionbutton import QActionButton
from ..widget.qerror import QError
from ..widget.qregisterflag import QRegisterFlagDev
from ..widget.qspeed import QSpeed
from ..widget.qsystemmode import QSystemModeDev
from ..widget.qtorque import QTorque
from .res import img_rc


class Ui_DevWindow(object):
    def setupUi(self, DevWindow):
        DevWindow.setObjectName("DevWindow")
        DevWindow.resize(682, 403)
        self.centralwidget = QtWidgets.QWidget(DevWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBoxBoardStatus = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxBoardStatus.setObjectName("groupBoxBoardStatus")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxBoardStatus)
        self.gridLayout.setObjectName("gridLayout")
        self.frameBoardError = QError(self.groupBoxBoardStatus)
        self.frameBoardError.setObjectName("frameBoardError")
        self.gridLayout.addWidget(self.frameBoardError, 0, 0, 1, 2)
        self.frameBoardStatus1 = QRegisterFlagDev(self.groupBoxBoardStatus)
        self.frameBoardStatus1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBoardStatus1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBoardStatus1.setObjectName("frameBoardStatus1")
        self.gridLayout.addWidget(self.frameBoardStatus1, 1, 0, 1, 1)
        self.frameBoardStatus2 = QRegisterFlagDev(self.groupBoxBoardStatus)
        self.frameBoardStatus2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBoardStatus2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBoardStatus2.setObjectName("frameBoardStatus2")
        self.gridLayout.addWidget(self.frameBoardStatus2, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxBoardStatus)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabMotor = QtWidgets.QWidget()
        self.tabMotor.setObjectName("tabMotor")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabMotor)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxTorque = QtWidgets.QGroupBox(self.tabMotor)
        self.groupBoxTorque.setObjectName("groupBoxTorque")
        self.verticalLayoutTorque = QtWidgets.QVBoxLayout(self.groupBoxTorque)
        self.verticalLayoutTorque.setObjectName("verticalLayoutTorque")
        self.widgetTorque = QTorque(self.groupBoxTorque)
        self.widgetTorque.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.widgetTorque.setFrameShadow(QtWidgets.QFrame.Raised)
        self.widgetTorque.setObjectName("widgetTorque")
        self.verticalLayoutTorque.addWidget(self.widgetTorque)
        self.gridLayout_2.addWidget(self.groupBoxTorque, 0, 1, 1, 1)
        self.pushButtonStop = QActionButton(self.tabMotor)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/32/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonStop.setIcon(icon)
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.gridLayout_2.addWidget(self.pushButtonStop, 1, 1, 1, 1)
        self.pushButtonStart = QActionButton(self.tabMotor)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/32/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonStart.setIcon(icon1)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.gridLayout_2.addWidget(self.pushButtonStart, 1, 0, 1, 1)
        self.groupBoxSpeed = QtWidgets.QGroupBox(self.tabMotor)
        self.groupBoxSpeed.setObjectName("groupBoxSpeed")
        self.verticalLayoutSpeed = QtWidgets.QVBoxLayout(self.groupBoxSpeed)
        self.verticalLayoutSpeed.setObjectName("verticalLayoutSpeed")
        self.widgetSpeed = QSpeed(self.groupBoxSpeed)
        self.widgetSpeed.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.widgetSpeed.setFrameShadow(QtWidgets.QFrame.Raised)
        self.widgetSpeed.setObjectName("widgetSpeed")
        self.verticalLayoutSpeed.addWidget(self.widgetSpeed)
        self.gridLayout_2.addWidget(self.groupBoxSpeed, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabMotor, "")
        self.tabBoard = QtWidgets.QWidget()
        self.tabBoard.setObjectName("tabBoard")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabBoard)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBoxSystemMode = QtWidgets.QGroupBox(self.tabBoard)
        self.groupBoxSystemMode.setObjectName("groupBoxSystemMode")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBoxSystemMode)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frameSystemMode = QSystemModeDev(self.groupBoxSystemMode)
        self.frameSystemMode.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameSystemMode.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameSystemMode.setObjectName("frameSystemMode")
        self.verticalLayout_2.addWidget(self.frameSystemMode)
        self.gridLayout_3.addWidget(self.groupBoxSystemMode, 0, 0, 1, 1)
        self.groupBoxAnalogInputs = QtWidgets.QGroupBox(self.tabBoard)
        self.groupBoxAnalogInputs.setObjectName("groupBoxAnalogInputs")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBoxAnalogInputs)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_3.addWidget(self.groupBoxAnalogInputs, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tabBoard, "")
        self.tabDebug = QtWidgets.QWidget()
        self.tabDebug.setObjectName("tabDebug")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tabDebug)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBoxDebugValues = QtWidgets.QGroupBox(self.tabDebug)
        self.groupBoxDebugValues.setObjectName("groupBoxDebugValues")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxDebugValues)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_5.addWidget(self.groupBoxDebugValues, 0, 0, 3, 1)
        self.groupBoxDebugDAC = QtWidgets.QGroupBox(self.tabDebug)
        self.groupBoxDebugDAC.setObjectName("groupBoxDebugDAC")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxDebugDAC)
        self.formLayout.setObjectName("formLayout")
        self.labelDebugDac0 = QtWidgets.QLabel(self.groupBoxDebugDAC)
        self.labelDebugDac0.setObjectName("labelDebugDac0")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelDebugDac0)
        self.comboBoxDebugDac0 = QtWidgets.QComboBox(self.groupBoxDebugDAC)
        self.comboBoxDebugDac0.setObjectName("comboBoxDebugDac0")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBoxDebugDac0)
        self.labelDebugDac1 = QtWidgets.QLabel(self.groupBoxDebugDAC)
        self.labelDebugDac1.setObjectName("labelDebugDac1")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelDebugDac1)
        self.comboBoxDebugDac1 = QtWidgets.QComboBox(self.groupBoxDebugDAC)
        self.comboBoxDebugDac1.setObjectName("comboBoxDebugDac1")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxDebugDac1)
        self.gridLayout_5.addWidget(self.groupBoxDebugDAC, 2, 1, 1, 1)
        self.frame = QtWidgets.QFrame(self.tabDebug)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButtonRefreshDebug = QActionButton(self.frame)
        self.pushButtonRefreshDebug.setObjectName("pushButtonRefreshDebug")
        self.horizontalLayout_2.addWidget(self.pushButtonRefreshDebug)
        self.gridLayout_5.addWidget(self.frame, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tabDebug, "")
        self.verticalLayout.addWidget(self.tabWidget)
        DevWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(DevWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 682, 22))
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
        DevWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(DevWindow)
        self.statusBar.setObjectName("statusBar")
        DevWindow.setStatusBar(self.statusBar)
        self.toolBarSystem = QtWidgets.QToolBar(DevWindow)
        self.toolBarSystem.setObjectName("toolBarSystem")
        DevWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarSystem)
        self.toolBarMotor = QtWidgets.QToolBar(DevWindow)
        self.toolBarMotor.setObjectName("toolBarMotor")
        DevWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarMotor)
        self.actionLink = QtWidgets.QAction(DevWindow)
        self.actionLink.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/32/unlink.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/img/32/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon2.addPixmap(QtGui.QPixmap(":/img/32/link.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/img/32/unlink.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionLink.setIcon(icon2)
        self.actionLink.setObjectName("actionLink")
        self.actionMotorStart = QtWidgets.QAction(DevWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/32/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionMotorStart.setIcon(icon3)
        self.actionMotorStart.setObjectName("actionMotorStart")
        self.actionLightEnabled = QtWidgets.QAction(DevWindow)
        self.actionLightEnabled.setCheckable(True)
        self.actionLightEnabled.setChecked(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/32/light-off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/img/32/light-on.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon4.addPixmap(QtGui.QPixmap(":/img/32/light-on.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/img/32/light-off.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionLightEnabled.setIcon(icon4)
        self.actionLightEnabled.setObjectName("actionLightEnabled")
        self.actionLightBlue = QtWidgets.QAction(DevWindow)
        self.actionLightBlue.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/img/32/light.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(":/img/32/light-blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon5.addPixmap(QtGui.QPixmap(":/img/32/light-blue.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(":/img/32/light.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionLightBlue.setIcon(icon5)
        self.actionLightBlue.setObjectName("actionLightBlue")
        self.actionMotorReverse = QtWidgets.QAction(DevWindow)
        self.actionMotorReverse.setCheckable(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/img/32/clockwise.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(":/img/32/counterclockwise.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon6.addPixmap(QtGui.QPixmap(":/img/32/counterclockwise.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(":/img/32/clockwise.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionMotorReverse.setIcon(icon6)
        self.actionMotorReverse.setObjectName("actionMotorReverse")
        self.actionAbout = QtWidgets.QAction(DevWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(DevWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAutoRefresh = QtWidgets.QAction(DevWindow)
        self.actionAutoRefresh.setCheckable(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/img/32/autorefresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionAutoRefresh.setIcon(icon7)
        self.actionAutoRefresh.setObjectName("actionAutoRefresh")
        self.actionUnlink = QtWidgets.QAction(DevWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/img/32/unlink.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionUnlink.setIcon(icon8)
        self.actionUnlink.setObjectName("actionUnlink")
        self.actionRefresh = QtWidgets.QAction(DevWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/img/32/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRefresh.setIcon(icon9)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionHelp = QtWidgets.QAction(DevWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/img/32/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionHelp.setIcon(icon10)
        self.actionHelp.setObjectName("actionHelp")
        self.actionMotorStop = QtWidgets.QAction(DevWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/img/32/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionMotorStop.setIcon(icon11)
        self.actionMotorStop.setObjectName("actionMotorStop")
        self.actionFirmReset = QtWidgets.QAction(DevWindow)
        self.actionFirmReset.setObjectName("actionFirmReset")
        self.actionAPISendFirmware = QtWidgets.QAction(DevWindow)
        self.actionAPISendFirmware.setObjectName("actionAPISendFirmware")
        self.actionAboutBoard = QtWidgets.QAction(DevWindow)
        self.actionAboutBoard.setObjectName("actionAboutBoard")
        self.actionMotorMode = QtWidgets.QAction(DevWindow)
        self.actionMotorMode.setObjectName("actionMotorMode")
        self.actionRegistersView = QtWidgets.QAction(DevWindow)
        self.actionRegistersView.setObjectName("actionRegistersView")
        self.actionConnect = QtWidgets.QAction(DevWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/img/32/key.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnect.setIcon(icon12)
        self.actionConnect.setObjectName("actionConnect")
        self.actionRefreshDebug = QtWidgets.QAction(DevWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/img/32/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefreshDebug.setIcon(icon13)
        self.actionRefreshDebug.setObjectName("actionRefreshDebug")
        self.actionRefreshAnalogInputs = QtWidgets.QAction(DevWindow)
        self.actionRefreshAnalogInputs.setObjectName("actionRefreshAnalogInputs")
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
        self.menuBoard.addAction(self.actionRefreshDebug)
        self.menuBoard.addAction(self.actionRefreshAnalogInputs)
        self.menuBar.addAction(self.menuSystem.menuAction())
        self.menuBar.addAction(self.menuBoard.menuAction())
        self.menuBar.addAction(self.menuWorkspace.menuAction())
        self.menuBar.addAction(self.menuMotor.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.toolBarSystem.addAction(self.actionLink)
        self.toolBarSystem.addAction(self.actionConnect)
        self.toolBarSystem.addAction(self.actionRefresh)
        self.toolBarMotor.addAction(self.actionMotorStart)
        self.toolBarMotor.addAction(self.actionMotorStop)
        self.toolBarMotor.addAction(self.actionMotorReverse)
        self.toolBarMotor.addAction(self.actionLightEnabled)
        self.toolBarMotor.addAction(self.actionLightBlue)

        self.retranslateUi(DevWindow)
        self.tabWidget.setCurrentIndex(2)
        self.actionQuit.triggered.connect(DevWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DevWindow)

    def retranslateUi(self, DevWindow):
        _translate = QtCore.QCoreApplication.translate
        DevWindow.setWindowTitle(_translate("DevWindow", "DsmCP - Dev"))
        self.groupBoxBoardStatus.setTitle(_translate("DevWindow", "Status"))
        self.groupBoxTorque.setTitle(_translate("DevWindow", "Torque"))
        self.pushButtonStop.setText(_translate("DevWindow", "PushButton"))
        self.pushButtonStart.setText(_translate("DevWindow", "PushButton"))
        self.groupBoxSpeed.setTitle(_translate("DevWindow", "Speed"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMotor), _translate("DevWindow", "Motor"))
        self.groupBoxSystemMode.setTitle(_translate("DevWindow", "System mode"))
        self.groupBoxAnalogInputs.setTitle(_translate("DevWindow", "Analog inputs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBoard), _translate("DevWindow", "Board"))
        self.groupBoxDebugValues.setTitle(_translate("DevWindow", "Values"))
        self.groupBoxDebugDAC.setTitle(_translate("DevWindow", "DAC Signals"))
        self.labelDebugDac0.setText(_translate("DevWindow", "DAC #0"))
        self.labelDebugDac1.setText(_translate("DevWindow", "DAC #1"))
        self.pushButtonRefreshDebug.setText(_translate("DevWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDebug), _translate("DevWindow", "Debug"))
        self.menuSystem.setTitle(_translate("DevWindow", "System"))
        self.menuMotor.setTitle(_translate("DevWindow", "Motor"))
        self.menuHelp.setTitle(_translate("DevWindow", "Help"))
        self.menuWorkspace.setTitle(_translate("DevWindow", "Workspace"))
        self.menuBoard.setTitle(_translate("DevWindow", "Board"))
        self.toolBarSystem.setWindowTitle(_translate("DevWindow", "toolBar"))
        self.toolBarMotor.setWindowTitle(_translate("DevWindow", "toolBar_2"))
        self.actionLink.setText(_translate("DevWindow", "Link"))
        self.actionLink.setToolTip(_translate("DevWindow", "Link DCP to board"))
        self.actionMotorStart.setText(_translate("DevWindow", "Start"))
        self.actionMotorStart.setToolTip(_translate("DevWindow", "Start the motor"))
        self.actionMotorStart.setShortcut(_translate("DevWindow", "F2"))
        self.actionLightEnabled.setText(_translate("DevWindow", "Light Enabled"))
        self.actionLightEnabled.setToolTip(_translate("DevWindow", "Enable/disable Light"))
        self.actionLightEnabled.setShortcut(_translate("DevWindow", "F4"))
        self.actionLightBlue.setText(_translate("DevWindow", "BlueLight"))
        self.actionLightBlue.setToolTip(_translate("DevWindow", "Switch white / blue light"))
        self.actionLightBlue.setShortcut(_translate("DevWindow", "F9"))
        self.actionMotorReverse.setText(_translate("DevWindow", "Reverse"))
        self.actionMotorReverse.setToolTip(_translate("DevWindow", "Reverses the motor rotation direction"))
        self.actionMotorReverse.setShortcut(_translate("DevWindow", "F7"))
        self.actionAbout.setText(_translate("DevWindow", "About ..."))
        self.actionAbout.setShortcut(_translate("DevWindow", "Ctrl+F1"))
        self.actionQuit.setText(_translate("DevWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("DevWindow", "Ctrl+Q"))
        self.actionAutoRefresh.setText(_translate("DevWindow", "AutoRefresh"))
        self.actionUnlink.setText(_translate("DevWindow", "Unlink"))
        self.actionUnlink.setToolTip(_translate("DevWindow", "Unlink DCP from board"))
        self.actionRefresh.setText(_translate("DevWindow", "Refresh"))
        self.actionRefresh.setToolTip(_translate("DevWindow", "Refresh"))
        self.actionRefresh.setShortcut(_translate("DevWindow", "Ctrl+F5"))
        self.actionHelp.setText(_translate("DevWindow", "Help"))
        self.actionHelp.setShortcut(_translate("DevWindow", "F1"))
        self.actionMotorStop.setText(_translate("DevWindow", "Stop"))
        self.actionMotorStop.setToolTip(_translate("DevWindow", "Stop the motor"))
        self.actionMotorStop.setShortcut(_translate("DevWindow", "F3"))
        self.actionFirmReset.setText(_translate("DevWindow", "Firmware Reset"))
        self.actionFirmReset.setToolTip(_translate("DevWindow", "Reset the firmware settings"))
        self.actionAPISendFirmware.setText(_translate("DevWindow", "Send Firmware"))
        self.actionAboutBoard.setText(_translate("DevWindow", "About board..."))
        self.actionMotorMode.setText(_translate("DevWindow", "Motor mode..."))
        self.actionMotorMode.setToolTip(_translate("DevWindow", "Show motor mode dialog"))
        self.actionMotorMode.setShortcut(_translate("DevWindow", "F10"))
        self.actionRegistersView.setText(_translate("DevWindow", "Registers view"))
        self.actionRegistersView.setShortcut(_translate("DevWindow", "Shift+F1"))
        self.actionConnect.setText(_translate("DevWindow", "Connect..."))
        self.actionConnect.setToolTip(_translate("DevWindow", "Connect"))
        self.actionRefreshDebug.setText(_translate("DevWindow", "Refresh debug"))
        self.actionRefreshDebug.setShortcut(_translate("DevWindow", "F5"))
        self.actionRefreshAnalogInputs.setText(_translate("DevWindow", "Refresh Analog Inputs"))
        self.actionRefreshAnalogInputs.setToolTip(_translate("DevWindow", "Refresh Analog Inputs"))
        self.actionRefreshAnalogInputs.setShortcut(_translate("DevWindow", "Shift+F5"))
