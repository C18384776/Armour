import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings

from ui_prevpass import Ui_PreviousPasswords
import qdarkstyle


class PreviousPasswords(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_PreviousPasswords()
        self.ui.setupUi(self)

        self.ui.prevpass_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.settings = QSettings("Armour", "Armour Password Manager")

        try:
            self.setStyleSheet(self.settings.value("Theme"))
        except:
            pass

    def set_previous_password_list(self, entry, connection):
        cur = connection.cursor()
        cur.execute("SELECT * FROM previous_passwords WHERE passwordId = (?)", [entry[0]])
        prev_passwords = cur.fetchall()
        print("In prevpass.py")
        print(prev_passwords)

        self.ui.prevpass_tableWidget.setRowCount(len(prev_passwords))
        row = 0
        for entry in prev_passwords:
            print(entry[1])
            print(entry[2])
            self.ui.prevpass_tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(entry[1])))
            self.ui.prevpass_tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(entry[2])))
            row += 1
