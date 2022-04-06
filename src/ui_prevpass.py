from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PreviousPasswords(object):
    """
    UI for prevpass.py
    """
    def setupUi(self, PreviousPasswords):
        PreviousPasswords.setObjectName("PreviousPasswords")
        PreviousPasswords.resize(381, 264)
        PreviousPasswords.setMinimumSize(QtCore.QSize(381, 264))
        self.horizontalLayout = QtWidgets.QHBoxLayout(PreviousPasswords)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.prevpass_tableWidget = QtWidgets.QTableWidget(PreviousPasswords)
        self.prevpass_tableWidget.setObjectName("prevpass_tableWidget")
        self.prevpass_tableWidget.setColumnCount(2)
        self.prevpass_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.prevpass_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.prevpass_tableWidget.setHorizontalHeaderItem(1, item)
        self.horizontalLayout.addWidget(self.prevpass_tableWidget)

        self.retranslateUi(PreviousPasswords)
        QtCore.QMetaObject.connectSlotsByName(PreviousPasswords)

    def retranslateUi(self, PreviousPasswords):
        _translate = QtCore.QCoreApplication.translate
        PreviousPasswords.setWindowTitle(_translate("PreviousPasswords", "Previous Passwords"))
        item = self.prevpass_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("PreviousPasswords", "Password"))
        item = self.prevpass_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("PreviousPasswords", "Date Changed"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PreviousPasswords = QtWidgets.QWidget()
    ui = Ui_PreviousPasswords()
    ui.setupUi(PreviousPasswords)
    PreviousPasswords.show()
    sys.exit(app.exec_())
