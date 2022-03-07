import sys
import string
from PyQt5 import QtWidgets
from ui_passgen import Ui_PasswordGen
import error_checking
import crypto
import secrets


class PassGen(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_PasswordGen()
        self.ui.setupUi(self)

        # Character types.
        self.lower_alphabet = list(string.ascii_lowercase)
        self.higher_alphabet = list(string.ascii_uppercase)
        self.punctuation = list(string.punctuation)
        self.digits = list(string.digits)

        # Close on cancel button click.
        self.ui.cancel_pushButton.clicked.connect(self.close)

        # Hide/view password.
        self.ui.password_hide_pushButton. \
            clicked.connect(lambda:
                            error_checking.view_hide_password(self.ui.password_hide_pushButton,
                                                              self.ui.password_lineEdit))

        # Set range for progress bar.
        self.ui.strength_progressBar.setRange(0, 1000)
        self.ui.strength_progressBar.setValue(0)
        self.ui.strength_progressBar.setFormat("%v bits")

        # Each key press on password field will call function.
        self.ui.password_lineEdit. \
            textChanged. \
            connect(lambda: crypto.update_password_bits(self.ui.password_lineEdit,
                                                        None,
                                                        self.ui.strength_progressBar,
                                                        None))

        self.ui.password_lineEdit.textChanged.connect(self.password_changed)

        self.ui.length_horizontalSlider.valueChanged.connect(self.slider_changed)
        self.ui.length_spinBox.valueChanged.connect(self.spinbox_changed)

        self.ui.types_lower_alphabet_pushButton.setCheckable(True)
        self.ui.types_higher_alphabet_pushButton.setCheckable(True)
        self.ui.types_numbers_pushButton.setCheckable(True)
        self.ui.types_punctuation_pushButton.setCheckable(True)

        self.length_of_password = 0

        self.ui.types_lower_alphabet_pushButton. \
            clicked.connect(lambda: self.update_password(self.length_of_password))

        self.ui.types_higher_alphabet_pushButton. \
            clicked.connect(lambda: self.update_password(self.length_of_password))

        self.ui.types_numbers_pushButton. \
            clicked.connect(lambda: self.update_password(self.length_of_password))

        self.ui.types_punctuation_pushButton. \
            clicked.connect(lambda: self.update_password(self.length_of_password))

        self.ui.exclude_lineEdit.textChanged.connect(lambda: self.update_password(self.length_of_password))
        self.ui.include_lineEdit.textChanged.connect(lambda: self.update_password(self.length_of_password))

    def slider_changed(self, value):
        self.ui.length_spinBox.setValue(value)
        self.length_of_password = value
        self.update_password(value)

    def spinbox_changed(self, value):
        self.ui.length_horizontalSlider.setValue(value)

    def password_changed(self, value):
        length = len(value)
        self.ui.length_spinBox.setValue(length)
        self.ui.length_horizontalSlider.setValue(length)

    def update_password(self, value):
        password = ''
        available_values = []
        exclude = list(self.ui.exclude_lineEdit.text())
        include = list(self.ui.include_lineEdit.text())

        if self.ui.types_lower_alphabet_pushButton.isChecked():
            available_values += self.lower_alphabet

        if self.ui.types_higher_alphabet_pushButton.isChecked():
            available_values += self.higher_alphabet

        if self.ui.types_numbers_pushButton.isChecked():
            available_values += self.digits

        if self.ui.types_punctuation_pushButton.isChecked():
            available_values += self.punctuation

        # Use all available characters if none were toggled.
        if not available_values:
            available_values += self.lower_alphabet
            available_values += self.higher_alphabet
            available_values += self.digits
            available_values += self.punctuation

        for x in exclude:
            if x in available_values:
                available_values.remove(x)

        for x in include:
            if x not in available_values:
                available_values.append(x)

        for _ in range(value):
            password += secrets.choice(available_values)

        self.ui.password_lineEdit.setText(password)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PassGen()
    window.show()
    sys.exit(app.exec_())
