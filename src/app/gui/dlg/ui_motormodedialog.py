# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/app/gui/dlg/motormodedialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MotorModeDialog(object):
    def setupUi(self, MotorModeDialog):
        MotorModeDialog.setObjectName("MotorModeDialog")
        MotorModeDialog.resize(400, 313)
        self.verticalLayout = QtWidgets.QVBoxLayout(MotorModeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(MotorModeDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 2, 1, 1)
        self.labeLightIntensity = QtWidgets.QLabel(MotorModeDialog)
        self.labeLightIntensity.setObjectName("labeLightIntensity")
        self.gridLayout.addWidget(self.labeLightIntensity, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(MotorModeDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.labelAcceleration = QtWidgets.QLabel(MotorModeDialog)
        self.labelAcceleration.setObjectName("labelAcceleration")
        self.gridLayout.addWidget(self.labelAcceleration, 1, 0, 1, 1)
        self.registerAcceleration = QSpinBoxRegister(MotorModeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerAcceleration.sizePolicy().hasHeightForWidth())
        self.registerAcceleration.setSizePolicy(sizePolicy)
        self.registerAcceleration.setObjectName("registerAcceleration")
        self.gridLayout.addWidget(self.registerAcceleration, 1, 1, 1, 1)
        self.registerLightIntensity = QSpinBoxRegister(MotorModeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerLightIntensity.sizePolicy().hasHeightForWidth())
        self.registerLightIntensity.setSizePolicy(sizePolicy)
        self.registerLightIntensity.setObjectName("registerLightIntensity")
        self.gridLayout.addWidget(self.registerLightIntensity, 2, 1, 1, 1)
        self.systemMode = QSystemMode(MotorModeDialog)
        self.systemMode.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.systemMode.setFrameShadow(QtWidgets.QFrame.Raised)
        self.systemMode.setObjectName("systemMode")
        self.gridLayout.addWidget(self.systemMode, 0, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(MotorModeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MotorModeDialog)
        self.buttonBox.accepted.connect(MotorModeDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(MotorModeDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MotorModeDialog)

    def retranslateUi(self, MotorModeDialog):
        _translate = QtCore.QCoreApplication.translate
        MotorModeDialog.setWindowTitle(_translate("MotorModeDialog", "DsmCP - Motor set points"))
        self.label.setText(_translate("MotorModeDialog", "krpm/s"))
        self.labeLightIntensity.setText(_translate("MotorModeDialog", "Light intensity"))
        self.label_2.setText(_translate("MotorModeDialog", "mA"))
        self.labelAcceleration.setText(_translate("MotorModeDialog", "Acceleration"))
from ..widget.qspinboxregister import QSpinBoxRegister
from ..widget.qsystemmode import QSystemMode
