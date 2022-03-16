# import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEventLoop

from ui_entry import Ui_Entry
import error_checking
import crypto
from passgen import PassGen


class Entry(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Entry()
        self.ui.setupUi(self)
        # self.show()

        self.ui.cancel_button.clicked.connect(self.close)
        self.ui.password_error_label.hide()
        self.ui.repeat_error_label.hide()

        # Set edit to password mode.
        self.ui.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.password_view_button. \
            clicked.connect(lambda:
                            error_checking.view_hide_password(self.ui.password_view_button,
                                                              self.ui.password_lineEdit))

        # self.ui.submit_button.clicked.connect(lambda: self.submitted())

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

        self.submitted_info = False

        self.ui.password_generator_button.clicked.connect(lambda: self.password_generator_clicked())

    def password_generator_clicked(self):
        print("Password generator clicked")
        UI_passgen = PassGen()
        UI_passgen.__init__()
        UI_passgen.ui.submit_pushButton.clicked.connect(lambda: self.passgen_submit(UI_passgen))
        UI_passgen.show()
        loop = QEventLoop()
        # By default, login is hidden on close()
        # This attribute makes it destroyed.
        UI_passgen.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        UI_passgen.destroyed.connect(loop.quit)

    def passgen_submit(self, UI_passgen):
        self.ui.password_lineEdit.setText(UI_passgen.ui.password_lineEdit.text())
        self.ui.repeat_lineEdit.setText(UI_passgen.ui.password_lineEdit.text())
        UI_passgen.close()

    def get_entry_fields(self):
        return [self.website, self.username, self.password, self.url, self.twofa, self.submitted_info]

    def submitted(self):
        fields_complete = self.check_fields()

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


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = Entry()
#     window.show()
#     sys.exit(app.exec_())
