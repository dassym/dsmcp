# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/app/gui/dlg/sendfirmwaredialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SendFirmwareDialog(object):
    def setupUi(self, SendFirmwareDialog):
        SendFirmwareDialog.setObjectName("SendFirmwareDialog")
        SendFirmwareDialog.resize(407, 233)
        SendFirmwareDialog.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SendFirmwareDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(SendFirmwareDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelActual = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setItalic(True)
        self.labelActual.setFont(font)
        self.labelActual.setObjectName("labelActual")
        self.verticalLayout.addWidget(self.labelActual)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBoxFirmware = QtWidgets.QComboBox(self.frame)
        self.comboBoxFirmware.setObjectName("comboBoxFirmware")
        self.verticalLayout.addWidget(self.comboBoxFirmware)
        self.groupBoxAboutFirmware = QtWidgets.QGroupBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxAboutFirmware.sizePolicy().hasHeightForWidth())
        self.groupBoxAboutFirmware.setSizePolicy(sizePolicy)
        self.groupBoxAboutFirmware.setObjectName("groupBoxAboutFirmware")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBoxAboutFirmware)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelFirmwareDesc = QtWidgets.QLabel(self.groupBoxAboutFirmware)
        self.labelFirmwareDesc.setObjectName("labelFirmwareDesc")
        self.verticalLayout_3.addWidget(self.labelFirmwareDesc)
        self.verticalLayout.addWidget(self.groupBoxAboutFirmware)
        self.verticalLayout_2.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(SendFirmwareDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SendFirmwareDialog)
        self.buttonBox.accepted.connect(SendFirmwareDialog.accept)
        self.buttonBox.rejected.connect(SendFirmwareDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SendFirmwareDialog)

    def retranslateUi(self, SendFirmwareDialog):
        _translate = QtCore.QCoreApplication.translate
        SendFirmwareDialog.setWindowTitle(_translate("SendFirmwareDialog", "DSMCP - Programming"))
        self.labelActual.setText(_translate("SendFirmwareDialog", "TextLabel"))
        self.label.setText(_translate("SendFirmwareDialog", "Firmware:"))
        self.groupBoxAboutFirmware.setTitle(_translate("SendFirmwareDialog", "GroupBox"))
        self.labelFirmwareDesc.setText(_translate("SendFirmwareDialog", "labelFirmwareDesc"))
