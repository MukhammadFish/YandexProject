# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Window_Expenses_Story.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(672, 354)
        Form.setStyleSheet("background-color: rgb(97, 97, 97);")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(540, 310, 101, 31))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 201, 21))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 14pt \"Times New Roman\";")
        self.label.setObjectName("label")
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setGeometry(QtCore.QRect(10, 40, 651, 261))
        self.tableView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableView.setObjectName("tableView")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Закрыть"))
        self.label.setText(_translate("Form", "История расходов"))