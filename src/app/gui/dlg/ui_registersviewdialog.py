# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/app/gui/dlg/registersviewdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegistersViewDialog(object):
    def setupUi(self, RegistersViewDialog):
        RegistersViewDialog.setObjectName("RegistersViewDialog")
        RegistersViewDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(RegistersViewDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtWidgets.QTreeView(RegistersViewDialog)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.treeView)
        self.buttonBox = QtWidgets.QDialogButtonBox(RegistersViewDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RegistersViewDialog)
        self.buttonBox.accepted.connect(RegistersViewDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(RegistersViewDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(RegistersViewDialog)

    def retranslateUi(self, RegistersViewDialog):
        _translate = QtCore.QCoreApplication.translate
        RegistersViewDialog.setWindowTitle(_translate("RegistersViewDialog", "DsmCP - Registers View"))
