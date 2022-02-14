from PyQt5 import QtCore, QtWidgets
import file_explorer
import error_checking
import crypto


class UiLogin(object):
    def setup_ui_login(self, Login):
        self.login_button = QtWidgets.QPushButton(Login)
        self.quit_button = QtWidgets.QPushButton(Login)
        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.secret_help_button = QtWidgets.QToolButton(Login)
        self.secret_button = QtWidgets.QPushButton(Login)
        self.secret_warning = QtWidgets.QLabel(Login)
        self.secret_edit = QtWidgets.QLineEdit(Login)
        self.layout_secret_edit = QtWidgets.QVBoxLayout()
        self.secret_label = QtWidgets.QLabel(Login)
        self.layout_secret = QtWidgets.QHBoxLayout()
        self.expert_checkBox = QtWidgets.QCheckBox(Login)
        self.password_help = QtWidgets.QToolButton(Login)
        self.password_view_button = QtWidgets.QPushButton(Login)
        self.password_warning = QtWidgets.QLabel(Login)
        self.password_edit = QtWidgets.QLineEdit(Login)
        self.layout_password_edit = QtWidgets.QVBoxLayout()
        self.password_label = QtWidgets.QLabel(Login)
        self.layout_password = QtWidgets.QHBoxLayout()
        self.directory_help = QtWidgets.QToolButton(Login)
        self.directory_browse_button = QtWidgets.QPushButton(Login)
        self.directory_warning = QtWidgets.QLabel(Login)
        self.directory_edit = QtWidgets.QLineEdit(Login)
        self.layout_directory_edit = QtWidgets.QVBoxLayout()
        self.directory_label = QtWidgets.QLabel(Login)
        self.layout_directory = QtWidgets.QHBoxLayout()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(Login)
        Login.setObjectName("Login")
        Login.resize(437, 349)
        Login.setMinimumSize(QtCore.QSize(437, 290))
        Login.setMaximumSize(QtCore.QSize(696, 349))
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.main_layout.setObjectName("main_layout")
        self.layout_directory.setObjectName("layout_directory")
        self.directory_label.setTextFormat(QtCore.Qt.PlainText)
        self.directory_label.setAlignment(QtCore.Qt.AlignCenter)
        self.directory_label.setObjectName("directory_label")
        self.layout_directory.addWidget(self.directory_label)
        self.layout_directory_edit.setObjectName("layout_directory_edit")
        self.directory_edit.setObjectName("directory_edit")
        self.layout_directory_edit.addWidget(self.directory_edit)
        self.directory_warning.setObjectName("directory_warning")
        self.layout_directory_edit.addWidget(self.directory_warning)
        self.layout_directory.addLayout(self.layout_directory_edit)
        self.directory_browse_button.setObjectName("directory_browse_button")
        self.layout_directory.addWidget(self.directory_browse_button)
        self.directory_help.setObjectName("directory_help")
        self.layout_directory.addWidget(self.directory_help)
        self.main_layout.addLayout(self.layout_directory)
        self.layout_password.setObjectName("layout_password")
        self.password_label.setTextFormat(QtCore.Qt.PlainText)
        self.password_label.setObjectName("password_label")
        self.layout_password.addWidget(self.password_label)
        self.layout_password_edit.setObjectName("layout_password_edit")
        self.password_edit.setObjectName("password_edit")
        self.layout_password_edit.addWidget(self.password_edit)
        self.password_warning.setObjectName("password_warning")
        self.layout_password_edit.addWidget(self.password_warning)
        self.layout_password.addLayout(self.layout_password_edit)
        self.password_view_button.setObjectName("password_view_button")
        self.layout_password.addWidget(self.password_view_button)
        self.password_help.setObjectName("password_help")
        self.layout_password.addWidget(self.password_help)
        self.main_layout.addLayout(self.layout_password)
        self.expert_checkBox.setObjectName("expert_checkBox")
        self.main_layout.addWidget(self.expert_checkBox)
        self.layout_secret.setObjectName("layout_secret")
        self.secret_label.setObjectName("secret_label")
        self.layout_secret.addWidget(self.secret_label)
        self.layout_secret_edit.setObjectName("layout_secret_edit")
        self.secret_edit.setObjectName("secret_edit")
        self.layout_secret_edit.addWidget(self.secret_edit)
        self.secret_warning.setObjectName("secret_warning")
        self.layout_secret_edit.addWidget(self.secret_warning)
        self.layout_secret.addLayout(self.layout_secret_edit)
        self.secret_button.setObjectName("secret_button")
        self.layout_secret.addWidget(self.secret_button)
        self.secret_help_button.setObjectName("secret_help_button")
        self.layout_secret.addWidget(self.secret_help_button)
        self.main_layout.addLayout(self.layout_secret)
        self.layout_buttons.setObjectName("layout_buttons")
        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_buttons.addItem(spacer_item)
        self.quit_button.setObjectName("quit_button")
        self.layout_buttons.addWidget(self.quit_button)
        self.login_button.setObjectName("login_button")
        self.layout_buttons.addWidget(self.login_button)
        self.main_layout.addLayout(self.layout_buttons)
        self.horizontalLayout_6.addLayout(self.main_layout)

        # Expert checkbox is hidden by default.
        self.expert_checkBox.stateChanged.connect(
            lambda: error_checking.expert_box_clicked(self.expert_checkBox.isChecked(),
                                                      self.secret_label,
                                                      self.secret_edit,
                                                      self.secret_button,
                                                      self.secret_help_button,
                                                      self.secret_warning))
        self.secret_label.hide()
        self.secret_edit.hide()
        self.secret_button.hide()
        self.secret_help_button.hide()

        # Browse for folder path to save password database file in.
        self.directory_browse_button.clicked.connect(lambda: file_explorer.browse_file(self.directory_edit,
                                                                                       self.directory_warning))
        self.directory_edit.setReadOnly(True)

        # Browse for file path.
        self.secret_button.clicked.connect(lambda: file_explorer.browse_file(self.secret_edit,
                                                                             self.secret_warning))
        self.secret_edit.setReadOnly(True)

        # Clear warning labels.
        self.directory_warning.hide()
        self.password_warning.hide()
        self.secret_warning.hide()

        # Cancel button clicked will close the program.
        self.quit_button.clicked.connect(Login.close)

        # Set edit to password mode.
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Each key press on password field will call function.
        self.password_edit.textChanged.connect(lambda: self.update_if_field_nonempty())

        self.password_view_button.clicked.connect(lambda: error_checking.view_hide_password(self.password_view_button,
                                                                                            self.password_edit))
        self.login_button.clicked.connect(lambda: self.login())
        self.login_button.clicked.connect(lambda: self.login_close(Login))

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

        self.master_password = None
        self.database = None

    def login_close(self, Login):
        # Closes login view if success.
        if self.master_password is not None:
            Login.close()

    def login(self):
        self.master_password, self.database = \
            crypto.login(error_checking.check_fields(self.directory_edit,
                                                     self.directory_warning,
                                                     self.password_edit,
                                                     self.password_warning,
                                                     self.expert_checkBox.isChecked(),
                                                     self.secret_edit,
                                                     self.secret_warning),
                         self.expert_checkBox.isChecked(),
                         self.secret_edit,
                         self.password_edit,
                         self.directory_edit)

    def update_if_field_nonempty(self):
        if self.password_edit.text() == '':
            self.password_warning.show()
        else:
            self.password_warning.hide()

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Login"))
        self.directory_label.setText(_translate("Login", "Database\n""File"))
        self.directory_warning.setText(_translate("Login", "Save location cannot be empty!"))
        self.directory_browse_button.setText(_translate("Login", "Browse"))
        self.directory_help.setText(_translate("Login", "?"))
        self.password_label.setText(_translate("Login", "Password"))
        self.password_warning.setText(_translate("Login", "Master password cannot be empty!"))
        self.password_view_button.setText(_translate("Login", "View"))
        self.password_help.setText(_translate("Login", "?"))
        self.expert_checkBox.setText(_translate("Login", "Expert Options"))
        self.secret_label.setText(_translate("Login", "<html><head/><body><p>Secret File</p></body></html>"))
        self.secret_warning.setText(_translate("Login", "Secret file cannot be empty!"))
        self.secret_button.setText(_translate("Login", "Browse"))
        self.secret_help_button.setText(_translate("Login", "?"))
        self.quit_button.setText(_translate("Login", "Quit"))
        self.login_button.setText(_translate("Login", "Login"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QWidget()
    ui = UiLogin()
    ui.setup_ui_login(Login)
    Login.show()
    sys.exit(app.exec_())
