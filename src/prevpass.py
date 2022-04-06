from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
from ui_prevpass import Ui_PreviousPasswords


class PreviousPasswords(QtWidgets.QWidget):
    """
    Functionality for the Previous Password view.
    UI is in the ui_prevpass.py file.
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_PreviousPasswords()
        self.ui.setupUi(self)

        self.ui.prevpass_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Attempt to load previously loaded settings.
        self.settings = QSettings("Armour", "Armour Password Manager")
        try:
            self.setStyleSheet(self.settings.value("Theme"))
        except:
            pass

    def set_previous_password_list(self, entry, connection):
        """
        Load the previous passwords for a specific password entry.

        :param entry:
        The specific password entry.

        :param connection:
        Database connection.
        """
        # Create database cursor.
        cur = connection.cursor()
        # Execute select statement that catches all previous password entries from entry.
        cur.execute("SELECT * FROM previous_passwords WHERE passwordId = (?)", [entry[0]])
        prev_passwords = cur.fetchall()

        # Dynamically set the rows of password according to the length of available passwords.
        self.ui.prevpass_tableWidget.setRowCount(len(prev_passwords))
        row = 0
        # Set column password and date of each old password.
        for entry in prev_passwords:
            self.ui.prevpass_tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(entry[1])))
            self.ui.prevpass_tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(entry[2])))
            row += 1
