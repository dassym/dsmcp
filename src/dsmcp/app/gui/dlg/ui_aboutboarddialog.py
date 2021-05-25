# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/app/gui/dlg/aboutboarddialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutBoardDialog(object):
    def setupUi(self, AboutBoardDialog):
        AboutBoardDialog.setObjectName("AboutBoardDialog")
        AboutBoardDialog.resize(377, 203)
        AboutBoardDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(AboutBoardDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.labelImage = QtWidgets.QLabel(AboutBoardDialog)
        self.labelImage.setMinimumSize(QtCore.QSize(128, 64))
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
        self.labelBoardName.setTextFormat(QtCore.Qt.RichText)
        self.labelBoardName.setObjectName("labelBoardName")
        self.gridLayout.addWidget(self.labelBoardName, 0, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelSnIcon = QtWidgets.QLabel(AboutBoardDialog)
        self.labelSnIcon.setObjectName("labelSnIcon")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelSnIcon)
        self.labelSerialNumber = QtWidgets.QLabel(AboutBoardDialog)
        self.labelSerialNumber.setTextFormat(QtCore.Qt.RichText)
        self.labelSerialNumber.setObjectName("labelSerialNumber")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.labelSerialNumber)
        self.labelFactoryDateIcon = QtWidgets.QLabel(AboutBoardDialog)
        self.labelFactoryDateIcon.setObjectName("labelFactoryDateIcon")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelFactoryDateIcon)
        self.labelFactoryDate = QtWidgets.QLabel(AboutBoardDialog)
        self.labelFactoryDate.setTextFormat(QtCore.Qt.RichText)
        self.labelFactoryDate.setObjectName("labelFactoryDate")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.labelFactoryDate)
        self.labelFirmwareIcon = QtWidgets.QLabel(AboutBoardDialog)
        self.labelFirmwareIcon.setObjectName("labelFirmwareIcon")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelFirmwareIcon)
        self.labelFirmware = QtWidgets.QLabel(AboutBoardDialog)
        self.labelFirmware.setTextFormat(QtCore.Qt.RichText)
        self.labelFirmware.setObjectName("labelFirmware")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.labelFirmware)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutBoardDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 2, 1, 1)
        self.groupBoxConfig = QtWidgets.QGroupBox(AboutBoardDialog)
        self.groupBoxConfig.setObjectName("groupBoxConfig")
        self.gridLayoutConfig = QtWidgets.QGridLayout(self.groupBoxConfig)
        self.gridLayoutConfig.setObjectName("gridLayoutConfig")
        self.gridLayout.addWidget(self.groupBoxConfig, 2, 0, 1, 2)

        self.retranslateUi(AboutBoardDialog)
        self.buttonBox.accepted.connect(AboutBoardDialog.accept)
        self.buttonBox.rejected.connect(AboutBoardDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutBoardDialog)

    def retranslateUi(self, AboutBoardDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutBoardDialog.setWindowTitle(_translate("AboutBoardDialog", "About board"))
        self.labelImage.setText(_translate("AboutBoardDialog", "BOARD"))
        self.labelBoardName.setText(_translate("AboutBoardDialog", "MB-xx"))
        self.labelSnIcon.setText(_translate("AboutBoardDialog", "SN"))
        self.labelSerialNumber.setText(_translate("AboutBoardDialog", "00000"))
        self.labelFactoryDateIcon.setText(_translate("AboutBoardDialog", "Date"))
        self.labelFactoryDate.setText(_translate("AboutBoardDialog", "0000-00-00"))
        self.labelFirmwareIcon.setText(_translate("AboutBoardDialog", "Firmware"))
        self.labelFirmware.setText(_translate("AboutBoardDialog", "TextLabel"))
        self.groupBoxConfig.setTitle(_translate("AboutBoardDialog", "Configuration"))