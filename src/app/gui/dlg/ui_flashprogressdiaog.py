# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/app/gui/qt5/dlg/flashprogressdiaog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FlashProgressDialog(object):
    def setupUi(self, FlashProgressDialog):
        FlashProgressDialog.setObjectName("FlashProgressDialog")
        FlashProgressDialog.resize(400, 141)
        FlashProgressDialog.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(FlashProgressDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.progressBar = QtWidgets.QProgressBar(FlashProgressDialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 2)
        self.labelIcon = QtWidgets.QLabel(FlashProgressDialog)
        self.labelIcon.setObjectName("labelIcon")
        self.gridLayout.addWidget(self.labelIcon, 0, 0, 1, 1)
        self.labelText = QtWidgets.QLabel(FlashProgressDialog)
        self.labelText.setObjectName("labelText")
        self.gridLayout.addWidget(self.labelText, 0, 1, 1, 1)
        self.labelRemainingTime = QtWidgets.QLabel(FlashProgressDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRemainingTime.sizePolicy().hasHeightForWidth())
        self.labelRemainingTime.setSizePolicy(sizePolicy)
        self.labelRemainingTime.setObjectName("labelRemainingTime")
        self.gridLayout.addWidget(self.labelRemainingTime, 1, 0, 1, 2)

        self.retranslateUi(FlashProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(FlashProgressDialog)

    def retranslateUi(self, FlashProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        FlashProgressDialog.setWindowTitle(_translate("FlashProgressDialog", "DsmCP - Writing progress"))
        self.labelIcon.setText(_translate("FlashProgressDialog", "TextLabel"))
        self.labelText.setText(_translate("FlashProgressDialog", "TextLabel"))
        self.labelRemainingTime.setText(_translate("FlashProgressDialog", "TextLabel"))
