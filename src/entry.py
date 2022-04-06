from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEventLoop, QSettings
import information
from ui_entry import Ui_Entry
import crypto
from passgen import PassGen


class Entry(QtWidgets.QWidget):
    """
    Functionality for the Password Entry view.
    UI is in the ui_entry.py file.
    """
    def __init__(self):
        # Initialise UI.
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Entry()
        self.ui.setupUi(self)
        self.website = ''
        self.username = ''
        self.password = ''
        self.url = ''
        self.twofa = ''
        self.submitted_info = False

        # Close window when user clicks close.
        self.ui.cancel_button.clicked.connect(self.close)

        # Error checking labels are hidden as no data is yet entered.
        self.ui.password_error_label.hide()
        self.ui.repeat_error_label.hide()

        # Set edit to password mode.
        self.ui.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.repeat_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Hide view passwords on click.
        self.ui.password_view_button.clicked.connect(lambda: self.password_view_clicked())

        # Each key press on password field will call function.
        self.ui.password_lineEdit.textChanged.connect(lambda: self.update_if_field_nonempty())

        # Set range for progress bar.
        self.ui.strength_progressBar.setRange(0, 1000)
        self.ui.strength_progressBar.setValue(0)
        self.ui.strength_progressBar.setFormat("%v bits")

        # Each key press on password field will call function.
        self.ui.password_lineEdit.textChanged.connect(lambda: crypto.update_password_bits(self.ui.password_lineEdit,
                                                                                          None,
                                                                                          self.ui.strength_progressBar,
                                                                                          self.ui.password_error_label))

        # Open password generator on click.
        self.ui.password_generator_button.clicked.connect(lambda: self.password_generator_clicked())

        # Setup global program settings.
        self.settings = QSettings("Armour", "Armour Password Manager")

        # Set stylesheet.
        try:
            self.setStyleSheet(self.settings.value("Theme"))
        except:
            pass

        # Help buttons.
        self.ui.website_help.clicked.connect(lambda: information.entry_website_help_moment())
        self.ui.username_help.clicked.connect(lambda: information.entry_username_help_moment())
        self.ui.password_help.clicked.connect(lambda: information.entry_password_help_moment())
        self.ui.strength_help.clicked.connect(lambda: information.password_strength_help_moment())
        self.ui.url_help.clicked.connect(lambda: information.entry_url_help_moment())
        self.ui.twofa_help.clicked.connect(lambda: information.entry_twofa_help_moment())

    def password_view_clicked(self):
        """
        View/hide password and repeat password on button click..
        """
        if self.ui.password_lineEdit.echoMode() == 2:
            self.ui.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ui.repeat_lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.ui.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ui.repeat_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

    def password_generator_clicked(self):
        """
        Open password generator and input generated password into current entry.py program.
        """
        # Initialise and show password generator window.
        UI_passgen = PassGen()
        UI_passgen.__init__()
        UI_passgen.ui.submit_pushButton.clicked.connect(lambda: self.passgen_submit(UI_passgen))
        UI_passgen.show()

        # By default, login is hidden on close()
        # This attribute makes it destroyed.
        loop = QEventLoop()
        UI_passgen.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        UI_passgen.destroyed.connect(loop.quit)

    def passgen_submit(self, UI_passgen):
        """
        Places generated password into entry.py window values.

        :param UI_passgen:
        Class object for password generator.
        """
        self.ui.password_lineEdit.setText(UI_passgen.ui.password_lineEdit.text())
        self.ui.repeat_lineEdit.setText(UI_passgen.ui.password_lineEdit.text())
        UI_passgen.close()

    def get_entry_fields(self):
        """
        Used to receive entered values from entry into table_widget.py.

        :return:
        Values from current window.
        """
        return [self.website, self.username, self.password, self.url, self.twofa, self.submitted_info]

    def submitted(self):
        """
        Packs values from QT into custom variable, ready to be sent to table_widget.py.
        """
        fields_complete = self.check_fields()

        # If all needed fields are entered.
        if not fields_complete:
            print("Ready to submit")
            self.website = self.ui.website_lineEdit.text()
            self.username = self.ui.username_lineEdit.text()
            self.password = self.ui.password_lineEdit.text()
            self.url = self.ui.url_lineEdit.text()
            self.twofa = self.ui.twofa_lineEdit.text()
            self.submitted_info = True
            print("Submitted")
            self.close()

    def check_fields(self):
        """
        Check if password fields are entered and match.

        :return:
        True - fields are not fully entered. Show warning.
        False - fields are fully entered. Can proceed.
        """
        error = 0

        if self.ui.password_lineEdit.text() == '':
            self.ui.password_error_label.show()
            error = 1

        if self.ui.password_lineEdit.text() != self.ui.repeat_lineEdit.text():
            self.ui.repeat_error_label.show()
            error = 1

        if error == 1:
            return True
        else:
            return False

    def update_if_field_nonempty(self):
        """
        Show warning if field is empty and vice versa.
        """
        if self.ui.password_lineEdit.text() == '':
            self.ui.password_error_label.show()
        else:
            self.ui.password_error_label.hide()