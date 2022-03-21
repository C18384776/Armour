from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PreviousPasswords(object):
    def setupUi(self, PreviousPasswords):
        PreviousPasswords.setObjectName("PreviousPasswords")
        PreviousPasswords.resize(381, 264)
        PreviousPasswords.setMinimumSize(QtCore.QSize(381, 264))
        self.horizontalLayout = QtWidgets.QHBoxLayout(PreviousPasswords)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.prevpass_tableWidget = QtWidgets.QTableWidget(PreviousPasswords)
        self.prevpass_tableWidget.setObjectName("prevpass_tableWidget")
        self.prevpass_tableWidget.setColumnCount(0)
        self.prevpass_tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.prevpass_tableWidget)

        self.retranslateUi(PreviousPasswords)
        QtCore.QMetaObject.connectSlotsByName(PreviousPasswords)

    def retranslateUi(self, PreviousPasswords):
        _translate = QtCore.QCoreApplication.translate
        PreviousPasswords.setWindowTitle(_translate("PreviousPasswords", "Previous Passwords"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PreviousPasswords = QtWidgets.QWidget()
    ui = Ui_PreviousPasswords()
    ui.setupUi(PreviousPasswords)
    PreviousPasswords.show()
    sys.exit(app.exec_())
