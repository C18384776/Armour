from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from zxcvbn import zxcvbn
import math
import hashlib
from sqlite3 import Error
import sqlite3


class Ui_Registration(object):
    def setupUi(self, Registration):
        Registration.setObjectName("Registration")
        Registration.resize(437, 290)
        Registration.setMinimumSize(QtCore.QSize(437, 290))
        Registration.setMaximumSize(QtCore.QSize(696, 349))
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(Registration)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.layout_directory = QtWidgets.QHBoxLayout()
        self.layout_directory.setObjectName("layout_directory")
        self.directory_label = QtWidgets.QLabel(Registration)
        self.directory_label.setTextFormat(QtCore.Qt.PlainText)
        self.directory_label.setObjectName("directory_label")
        self.layout_directory.addWidget(self.directory_label)
        self.layout_directory_edit = QtWidgets.QVBoxLayout()
        self.layout_directory_edit.setObjectName("layout_directory_edit")
        self.directory_edit = QtWidgets.QLineEdit(Registration)
        self.directory_edit.setObjectName("directory_edit")
        self.layout_directory_edit.addWidget(self.directory_edit)
        self.directory_warning = QtWidgets.QLabel(Registration)
        self.directory_warning.setObjectName("directory_warning")
        self.layout_directory_edit.addWidget(self.directory_warning)
        self.layout_directory.addLayout(self.layout_directory_edit)
        self.directory_browse_button = QtWidgets.QPushButton(Registration)
        self.directory_browse_button.setObjectName("directory_browse_button")
        self.layout_directory.addWidget(self.directory_browse_button)
        self.directory_help = QtWidgets.QToolButton(Registration)
        self.directory_help.setObjectName("directory_help")
        self.layout_directory.addWidget(self.directory_help)
        self.main_layout.addLayout(self.layout_directory)
        self.layout_password = QtWidgets.QHBoxLayout()
        self.layout_password.setObjectName("layout_password")
        self.password_label = QtWidgets.QLabel(Registration)
        self.password_label.setTextFormat(QtCore.Qt.PlainText)
        self.password_label.setObjectName("password_label")
        self.layout_password.addWidget(self.password_label)
        self.layout_password_edit_2 = QtWidgets.QVBoxLayout()
        self.layout_password_edit_2.setObjectName("layout_password_edit_2")
        self.password_edit = QtWidgets.QLineEdit(Registration)
        self.password_edit.setObjectName("password_edit")
        self.layout_password_edit_2.addWidget(self.password_edit)
        self.password_warning = QtWidgets.QLabel(Registration)
        self.password_warning.setObjectName("password_warning")
        self.layout_password_edit_2.addWidget(self.password_warning)
        self.layout_password.addLayout(self.layout_password_edit_2)
        self.password_view_button = QtWidgets.QPushButton(Registration)
        self.password_view_button.setObjectName("password_view_button")
        self.layout_password.addWidget(self.password_view_button)
        self.password_help = QtWidgets.QToolButton(Registration)
        self.password_help.setObjectName("password_help")
        self.layout_password.addWidget(self.password_help)
        self.main_layout.addLayout(self.layout_password)
        self.layout_strength = QtWidgets.QHBoxLayout()
        self.layout_strength.setObjectName("layout_strength")
        self.strength_label = QtWidgets.QLabel(Registration)
        self.strength_label.setEnabled(True)
        self.strength_label.setLineWidth(1)
        self.strength_label.setTextFormat(QtCore.Qt.PlainText)
        self.strength_label.setWordWrap(False)
        self.strength_label.setObjectName("strength_label")
        self.layout_strength.addWidget(self.strength_label)
        self.strength_progress_bar = QtWidgets.QProgressBar(Registration)
        self.strength_progress_bar.setMinimumSize(QtCore.QSize(0, 25))
        self.strength_progress_bar.setMaximumSize(QtCore.QSize(16777215, 25))
        self.strength_progress_bar.setProperty("value", 24)
        self.strength_progress_bar.setObjectName("strength_progress_bar")
        self.layout_strength.addWidget(self.strength_progress_bar)
        self.strength_help_button = QtWidgets.QToolButton(Registration)
        self.strength_help_button.setObjectName("strength_help_button")
        self.layout_strength.addWidget(self.strength_help_button)
        self.main_layout.addLayout(self.layout_strength)
        self.expert_checkBox = QtWidgets.QCheckBox(Registration)
        self.expert_checkBox.setObjectName("expert_checkBox")
        self.main_layout.addWidget(self.expert_checkBox)
        self.layout_secret = QtWidgets.QHBoxLayout()
        self.layout_secret.setObjectName("layout_secret")
        self.secret_label = QtWidgets.QLabel(Registration)
        self.secret_label.setObjectName("secret_label")
        self.layout_secret.addWidget(self.secret_label)
        self.layout_secret_edit = QtWidgets.QVBoxLayout()
        self.layout_secret_edit.setObjectName("layout_secret_edit")
        self.secret_edit = QtWidgets.QLineEdit(Registration)
        self.secret_edit.setObjectName("secret_edit")
        self.layout_secret_edit.addWidget(self.secret_edit)
        self.secret_warning = QtWidgets.QLabel(Registration)
        self.secret_warning.setObjectName("secret_warning")
        self.layout_secret_edit.addWidget(self.secret_warning)
        self.layout_secret.addLayout(self.layout_secret_edit)
        self.secret_button = QtWidgets.QPushButton(Registration)
        self.secret_button.setObjectName("secret_button")
        self.layout_secret.addWidget(self.secret_button)
        self.secret_help_button = QtWidgets.QToolButton(Registration)
        self.secret_help_button.setObjectName("secret_help_button")
        self.layout_secret.addWidget(self.secret_help_button)
        self.main_layout.addLayout(self.layout_secret)
        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.layout_buttons.setObjectName("layout_buttons")
        self.login_button = QtWidgets.QPushButton(Registration)
        self.login_button.setObjectName("login_button")
        self.layout_buttons.addWidget(self.login_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_buttons.addItem(spacerItem)
        self.quit_button = QtWidgets.QPushButton(Registration)
        self.quit_button.setObjectName("quit_button")
        self.layout_buttons.addWidget(self.quit_button)
        self.register_button = QtWidgets.QPushButton(Registration)
        self.register_button.setObjectName("register_button")
        self.layout_buttons.addWidget(self.register_button)
        self.main_layout.addLayout(self.layout_buttons)
        self.horizontalLayout_6.addLayout(self.main_layout)

        # Expert checkbox is hidden by default.
        self.expert_checkBox.stateChanged.connect(lambda: self.expert_box_clicked())
        self.secret_label.hide()
        self.secret_edit.hide()
        self.secret_button.hide()
        self.secret_help_button.hide()

        # Cancel button clicked will close the program.
        self.quit_button.clicked.connect(QtWidgets.QApplication.instance().quit)

        # Each key press on password field will call function.
        self.password_edit.textChanged.connect(lambda: self.update_password_bits())

        # Browse for folder path to save password database file in.
        self.directory_browse_button.clicked.connect(lambda: self.browse_dir())
        self.directory_edit.setReadOnly(True)

        # Set edit to password mode.
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Set range for progress bar.
        self.strength_progress_bar.setRange(0, 1000)
        self.strength_progress_bar.setValue(0)

        # Browse for file path.
        self.secret_button.clicked.connect(lambda: self.browse_file())
        self.secret_edit.setReadOnly(True)

        # Ok button clicked; create database from provided fields.
        self.register_button.clicked.connect(lambda: self.registration())

        self.password_view_button.clicked.connect(lambda: self.view_hide_password())

        # Clear warning labels.
        self.directory_warning.hide()
        self.password_warning.hide()
        self.secret_warning.hide()

        self.retranslateUi(Registration)
        QtCore.QMetaObject.connectSlotsByName(Registration)

        self.retranslateUi(Registration)
        QtCore.QMetaObject.connectSlotsByName(Registration)

    def expert_box_clicked(self):
        if self.expert_checkBox.isChecked():
            self.secret_label.show()
            self.secret_edit.show()
            self.secret_button.show()
            self.secret_help_button.show()
        else:
            self.secret_label.hide()
            self.secret_edit.hide()
            self.secret_button.hide()
            self.secret_help_button.hide()
            self.secret_warning.hide()

    def update_password_bits(self):
        # Entropy is calculated when text field is not empty.
        if self.password_edit.text():
            result = zxcvbn(self.password_edit.text())
            self.password_bits_value = math.log2(result["guesses"]).__floor__()
            self.strength_progress_bar.setValue(self.password_bits_value)

            # Hides password warning if a password is typed.
            if self.password_edit.text():
                self.password_warning.hide()
        elif self.password_edit.text() == '':
            self.strength_progress_bar.setValue(0)

            # User is warned that password cannot be blank.
            self.password_warning.show()

    def browse_dir(self):
        self.dir_path = QtWidgets.QFileDialog.getExistingDirectory()
        self.directory_edit.setText(self.dir_path)

        # Hides directory warning if directory path is selected.
        if self.directory_edit.text():
            self.directory_warning.hide()

    def browse_file(self):
        self.file_path = QtWidgets.QFileDialog.getOpenFileName()
        self.secret_edit.setText(self.file_path[0])

        # Hides file warning if file path is selected.
        if self.secret_edit.text():
            self.secret_warning.hide()

    def registration(self):
        # Function checks if fields are entered.
        # True = All needed fields are non-blank.
        # False = One or more fields are blank.
        fields_filled = self.check_fields()

        # Begin database registration once fields are non-blank.
        if not fields_filled:
            # Show a warning if given password that is deemed weak.
            if self.password_bits_value < 100:
                self.password_warning_message()
                # If users password was weak and they decided to change it from the warning.
                if self.password_dialog_response == "No":
                    return 1
                else:
                    database_save_path = self.directory_edit.text()
                    database_save_path = database_save_path + "/Password.db"

                    sql_create_group_table = """
                                            CREATE TABLE IF NOT EXISTS groups (
                                                groupId integer PRIMARY KEY,
                                                groupName text NOT NULL);"""

                    sql_create_password_table = """
                                            CREATE TABLE IF NOT EXISTS passwords (
                                                passwordId integer PRIMARY KEY,
                                                passwordName text,
                                                passwordPassword NOT NULL,
                                                groupId integer NOT NULL,
                                                FOREIGN KEY (groupId) REFERENCES groups(groupId));"""

                    connection = self.make_connection(database_save_path)

                    if connection is not None:
                        self.make_table(connection, sql_create_group_table)
                        self.make_table(connection, sql_create_password_table)
                        connection.commit()
                        connection.close()
                        print("Database Made")
                    else:
                        print("Problem making database?")

    def make_table(self, connection, make_sql_table):
        try:
            cur = connection.cursor()
            cur.execute(make_sql_table)
        except Error as e:
            print(e)

    def make_connection(self, database_save_path):
        con = None
        try:
            con = sqlite3.connect(database_save_path)
        except Error as e:
            print(e)

        return con


    def check_fields(self):
        error = 0

        if self.directory_edit.text() == '':
            self.directory_warning.show()
            error = 1

        if self.password_edit.text() == '':
            self.password_warning.show()
            error = 1

        if self.expert_checkBox.isChecked():
            if self.secret_edit.text() == '':
                self.secret_warning.show()
                error = 1

        if error == 1:
            return True
        else:
            return False

    def password_warning_message(self):
        message = QMessageBox()
        message.setWindowTitle("Weak Password Detected")
        message.setText("""
                            Your password appears to be weak.
                            Weak password make it easier for people
                            to hack your account. While you may proceed 
                            with the current password, it is strongly 
                            recommended that you set a password of more 
                            than 100 bits as shown in the progress bar.

                            Click "Yes" to proceed or "No" to go back.""")
        message.setIcon(QMessageBox.Warning)
        message.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        message.setDefaultButton(QMessageBox.No)
        message.buttonClicked.connect(self.password_warning_response)
        x = message.exec_()

    def password_warning_response(self, response):
        self.password_dialog_response = response.text()
        self.password_dialog_response = self.password_dialog_response.strip('&')

    def view_hide_password(self):
        if self.password_view_button.text() == "View":
            self.password_view_button.setText("Hide")
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_view_button.setText("View")
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)


    def retranslateUi(self, Registration):
        _translate = QtCore.QCoreApplication.translate
        Registration.setWindowTitle(_translate("Registration", "Registation"))
        self.directory_label.setText(_translate("Registration", "Save\n"
"Location"))
        self.directory_warning.setText(_translate("Registration", "Save location cannot be empty!"))
        self.directory_browse_button.setText(_translate("Registration", "Browse"))
        self.directory_help.setText(_translate("Registration", "?"))
        self.password_label.setText(_translate("Registration", "Master\n"
"Password"))
        self.password_warning.setText(_translate("Registration", "Master password cannot be empty!"))
        self.password_view_button.setText(_translate("Registration", "View"))
        self.password_help.setText(_translate("Registration", "?"))
        self.strength_label.setText(_translate("Registration", "Password\n"
"Strength"))
        self.strength_progress_bar.setFormat(_translate("Registration", "%v bits"))
        self.strength_help_button.setText(_translate("Registration", "?"))
        self.expert_checkBox.setText(_translate("Registration", "Expert Options"))
        self.secret_label.setText(_translate("Registration", "<html><head/><body><p>Secret File</p></body></html>"))
        self.secret_warning.setText(_translate("Registration", "Secret file cannot be empty!"))
        self.secret_button.setText(_translate("Registration", "Browse"))
        self.secret_help_button.setText(_translate("Registration", "?"))
        self.login_button.setText(_translate("Registration", "Login"))
        self.quit_button.setText(_translate("Registration", "Quit"))
        self.register_button.setText(_translate("Registration", "Register"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Registration = QtWidgets.QWidget()
    ui = Ui_Registration()
    ui.setupUi(Registration)
    Registration.show()
    sys.exit(app.exec_())
