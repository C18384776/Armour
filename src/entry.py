import sys

from PyQt5 import QtWidgets
from ui_entry import Ui_Entry
import error_checking
import crypto


class Entry(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Entry()
        self.ui.setupUi(self)
        self.show()

        self.ui.cancel_button.clicked.connect(self.close)
        self.ui.password_error_label.hide()
        self.ui.repeat_error_label.hide()

        # Set edit to password mode.
        self.ui.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.password_view_button. \
            clicked.connect(lambda:
                            error_checking.view_hide_password(self.ui.password_view_button,
                                                              self.ui.password_lineEdit))

        self.ui.submit_button.clicked.connect(lambda: self.submitted())

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

        self.website = ''
        self.username = ''
        self.password = ''
        self.url = ''
        self.twofa = ''

    def submitted(self):
        fields_complete = self.check_fields()

        if not fields_complete:
            print("Ready to submit")

    def check_fields(self):
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
        if self.ui.password_lineEdit.text() == '':
            self.ui.password_error_label.show()
        else:
            self.ui.password_error_label.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Entry()
    window.show()
    sys.exit(app.exec_())
