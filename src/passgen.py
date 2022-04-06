import string
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
import information
from ui_passgen import Ui_PasswordGen
import error_checking
import crypto
import secrets


class PassGen(QtWidgets.QWidget):
    """
    Functionality for the Password Generator view.
    UI is in the ui_passgen.py file.
    """
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

        # Update password for every character type button click.
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

        # Attempt to load previously loaded settings.
        self.settings = QSettings("Armour", "Armour Password Manager")

        try:
            self.setStyleSheet(self.settings.value("Theme"))
        except:
            pass

        # Help buttons.
        self.ui.password_help_pushButton.clicked.connect(lambda: information.passgen_password_help_moment())
        self.ui.strength_help_pushButton.clicked.connect(lambda: information.passgen_strength_help_moment())
        self.ui.length_help_pushButton.clicked.connect(lambda: information.passgen_length_help_moment())
        self.ui.types_help_pushButton.clicked.connect(lambda: information.passgen_types_help_moment())
        self.ui.include_help_pushButton.clicked.connect(lambda: information.passgen_include_help_moment())
        self.ui.exclude_help_pushButton.clicked.connect(lambda: information.passgen_exclude_help_moment())

    def slider_changed(self, value):
        """
        Method calls when password length slider changes.

        :param value:
        Value that the slider changed to.
        """
        self.ui.length_spinBox.setValue(value)
        self.length_of_password = value
        self.update_password(value)

    def spinbox_changed(self, value):
        """
        Method calls when password length spinbox changes.

        :param value:
        Value that the slider changed to.
        """
        self.ui.length_horizontalSlider.setValue(value)

    def password_changed(self, value):
        """
        Method calls when password settings changed.

        :param value:
        Value that the password length should be.
        """
        length = len(value)
        self.ui.length_spinBox.setValue(length)
        self.ui.length_horizontalSlider.setValue(length)

    def update_password(self, value):
        """
        Update the random password to match the characteristics set-forth by the user.

        :param value:
        Value that the password length should be.
        """
        # The password that will be displayed to user.
        password = ''
        # Available characters types that can form the password.
        available_values = []
        exclude = list(self.ui.exclude_lineEdit.text())
        include = list(self.ui.include_lineEdit.text())

        # Includes character types if box is selected.
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

        # Appends or removes characters entered by include/exclude fields.
        for x in exclude:
            if x in available_values:
                available_values.remove(x)
        for x in include:
            if x not in available_values:
                available_values.append(x)

        # Choose randomly password values until password length reached.
        for _ in range(value):
            password += secrets.choice(available_values)

        # Set text to randomly generated password.
        self.ui.password_lineEdit.setText(password)
