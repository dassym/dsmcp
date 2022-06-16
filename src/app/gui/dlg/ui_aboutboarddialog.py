# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/app/gui/qt5/dlg/aboutboarddialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from .res import img_rc


class Ui_AboutBoardDialog(object):
    def setupUi(self, AboutBoardDialog):
        AboutBoardDialog.setObjectName("AboutBoardDialog")
        AboutBoardDialog.resize(566, 286)
        AboutBoardDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(AboutBoardDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelSnIcon = QtWidgets.QLabel(AboutBoardDialog)
        self.labelSnIcon.setMaximumSize(QtCore.QSize(32, 32))
        self.labelSnIcon.setText("")
        self.labelSnIcon.setPixmap(QtGui.QPixmap(":/img/32/sn.png"))
        self.labelSnIcon.setScaledContents(True)
        self.labelSnIcon.setObjectName("labelSnIcon")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelSnIcon)
        self.labelFactoryDateIcon = QtWidgets.QLabel(AboutBoardDialog)
        self.labelFactoryDateIcon.setMaximumSize(QtCore.QSize(32, 32))
        self.labelFactoryDateIcon.setText("")
        self.labelFactoryDateIcon.setPixmap(QtGui.QPixmap(":/img/32/factory-date.png"))
        self.labelFactoryDateIcon.setScaledContents(True)
        self.labelFactoryDateIcon.setObjectName("labelFactoryDateIcon")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelFactoryDateIcon)
        self.labelFirmwareIcon = QtWidgets.QLabel(AboutBoardDialog)
        self.labelFirmwareIcon.setMaximumSize(QtCore.QSize(32, 32))
        self.labelFirmwareIcon.setText("")
        self.labelFirmwareIcon.setPixmap(QtGui.QPixmap(":/img/32/firmware.png"))
        self.labelFirmwareIcon.setScaledContents(True)
        self.labelFirmwareIcon.setObjectName("labelFirmwareIcon")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelFirmwareIcon)
        self.labelFirmware = QtWidgets.QLabel(AboutBoardDialog)
        self.labelFirmware.setText("Firmware")
        self.labelFirmware.setTextFormat(QtCore.Qt.RichText)
        self.labelFirmware.setObjectName("labelFirmware")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.labelFirmware)
        self.lineEditSerialNumber = QtWidgets.QLineEdit(AboutBoardDialog)
        self.lineEditSerialNumber.setObjectName("lineEditSerialNumber")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditSerialNumber)
        self.dateEditFactoryDate = QtWidgets.QDateEdit(AboutBoardDialog)
        self.dateEditFactoryDate.setDisplayFormat("yyyy-MM-dd")
        self.dateEditFactoryDate.setObjectName("dateEditFactoryDate")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dateEditFactoryDate)
        self.labelAccessIcon = QtWidgets.QLabel(AboutBoardDialog)
        self.labelAccessIcon.setMaximumSize(QtCore.QSize(32, 32))
        self.labelAccessIcon.setText("")
        self.labelAccessIcon.setPixmap(QtGui.QPixmap(":/img/32/key.png"))
        self.labelAccessIcon.setScaledContents(True)
        self.labelAccessIcon.setObjectName("labelAccessIcon")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelAccessIcon)
        self.labelAccess = QtWidgets.QLabel(AboutBoardDialog)
        self.labelAccess.setText("TextLabel")
        self.labelAccess.setObjectName("labelAccess")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.labelAccess)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutBoardDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 2, 1, 1)
        self.labelImage = QtWidgets.QLabel(AboutBoardDialog)
        self.labelImage.setMinimumSize(QtCore.QSize(128, 64))
        self.labelImage.setText("BOARD")
        self.labelImage.setObjectName("labelImage")
        self.gridLayout.addWidget(self.labelImage, 0, 1, 1, 1)
        self.labelBoardName = QtWidgets.QLabel(AboutBoardDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelBoardName.sizePolicy().hasHeightForWidth())
        self.labelBoardName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelBoardName.setFont(font)
        self.labelBoardName.setText("MB-xx")
        self.labelBoardName.setTextFormat(QtCore.Qt.RichText)
        self.labelBoardName.setObjectName("labelBoardName")
        self.gridLayout.addWidget(self.labelBoardName, 0, 0, 1, 1)
        self.groupBoxModeConfig = QtWidgets.QGroupBox(AboutBoardDialog)
        self.groupBoxModeConfig.setObjectName("groupBoxModeConfig")
        self.gridLayoutConfig = QtWidgets.QGridLayout(self.groupBoxModeConfig)
        self.gridLayoutConfig.setObjectName("gridLayoutConfig")
        self.gridLayout.addWidget(self.groupBoxModeConfig, 2, 0, 1, 2)
        self.groupBoxAdditionalBoard = QtWidgets.QGroupBox(AboutBoardDialog)
        self.groupBoxAdditionalBoard.setObjectName("groupBoxAdditionalBoard")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxAdditionalBoard)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelReset = QtWidgets.QLabel(self.groupBoxAdditionalBoard)
        self.labelReset.setObjectName("labelReset")
        self.gridLayout_2.addWidget(self.labelReset, 0, 1, 1, 1)
        self.labelAdditionalBoard = QtWidgets.QLabel(self.groupBoxAdditionalBoard)
        self.labelAdditionalBoard.setObjectName("labelAdditionalBoard")
        self.gridLayout_2.addWidget(self.labelAdditionalBoard, 0, 0, 1, 1)
        self.labelWatchdog = QtWidgets.QLabel(self.groupBoxAdditionalBoard)
        self.labelWatchdog.setObjectName("labelWatchdog")
        self.gridLayout_2.addWidget(self.labelWatchdog, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxAdditionalBoard, 3, 0, 1, 2)

        self.retranslateUi(AboutBoardDialog)
        self.buttonBox.accepted.connect(AboutBoardDialog.accept)
        self.buttonBox.rejected.connect(AboutBoardDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutBoardDialog)

    def retranslateUi(self, AboutBoardDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutBoardDialog.setWindowTitle(_translate("AboutBoardDialog", "DsmCP - About board"))
        self.groupBoxModeConfig.setTitle(_translate("AboutBoardDialog", "Mode configuration"))
        self.groupBoxAdditionalBoard.setTitle(_translate("AboutBoardDialog", "System configuration"))
        self.labelReset.setText(_translate("AboutBoardDialog", "Reset"))
        self.labelAdditionalBoard.setText(_translate("AboutBoardDialog", "Additional board"))
        self.labelWatchdog.setText(_translate("AboutBoardDialog", "Watch dog"))