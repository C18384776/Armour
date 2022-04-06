from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings

import file_explorer
import error_checking
import crypto
import information


class UiRegistration(object):
    """
    UI + Functionality for the register view.
    """
    def setup_ui_registration(self, Registration):
        self.password_bits_value = 0
        self.register_button = QtWidgets.QPushButton(Registration)
        self.quit_button = QtWidgets.QPushButton(Registration)
        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.secret_help_button = QtWidgets.QToolButton(Registration)
        self.secret_button = QtWidgets.QPushButton(Registration)
        self.secret_warning = QtWidgets.QLabel(Registration)
        self.secret_edit = QtWidgets.QLineEdit(Registration)
        self.layout_secret_edit = QtWidgets.QVBoxLayout()
        self.secret_label = QtWidgets.QLabel(Registration)
        self.layout_secret = QtWidgets.QHBoxLayout()
        self.expert_checkBox = QtWidgets.QCheckBox(Registration)
        self.strength_help_button = QtWidgets.QToolButton(Registration)
        self.strength_progress_bar = QtWidgets.QProgressBar(Registration)
        self.strength_label = QtWidgets.QLabel(Registration)
        self.layout_strength = QtWidgets.QHBoxLayout()
        self.password_help = QtWidgets.QToolButton(Registration)
        self.password_view_button = QtWidgets.QPushButton(Registration)
        self.password_warning = QtWidgets.QLabel(Registration)
        self.password_edit = QtWidgets.QLineEdit(Registration)
        self.layout_password_edit_2 = QtWidgets.QVBoxLayout()
        self.password_label = QtWidgets.QLabel(Registration)
        self.layout_password = QtWidgets.QHBoxLayout()
        self.directory_help = QtWidgets.QToolButton(Registration)
        self.directory_browse_button = QtWidgets.QPushButton(Registration)
        self.directory_warning = QtWidgets.QLabel(Registration)
        self.directory_edit = QtWidgets.QLineEdit(Registration)
        self.layout_directory_edit = QtWidgets.QVBoxLayout()
        self.directory_label = QtWidgets.QLabel(Registration)
        self.layout_directory = QtWidgets.QHBoxLayout()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(Registration)
        Registration.setObjectName("Registration")
        Registration.resize(437, 290)
        Registration.setMinimumSize(QtCore.QSize(437, 290))
        Registration.setMaximumSize(QtCore.QSize(696, 349))
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.main_layout.setObjectName("main_layout")
        self.layout_directory.setObjectName("layout_directory")
        self.directory_label.setTextFormat(QtCore.Qt.PlainText)
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
        self.layout_password_edit_2.setObjectName("layout_password_edit_2")
        self.password_edit.setObjectName("password_edit")
        self.layout_password_edit_2.addWidget(self.password_edit)
        self.password_warning.setObjectName("password_warning")
        self.layout_password_edit_2.addWidget(self.password_warning)
        self.layout_password.addLayout(self.layout_password_edit_2)
        self.password_view_button.setObjectName("password_view_button")
        self.layout_password.addWidget(self.password_view_button)
        self.password_help.setObjectName("password_help")
        self.layout_password.addWidget(self.password_help)
        self.main_layout.addLayout(self.layout_password)
        self.layout_strength.setObjectName("layout_strength")
        self.strength_label.setEnabled(True)
        self.strength_label.setLineWidth(1)
        self.strength_label.setTextFormat(QtCore.Qt.PlainText)
        self.strength_label.setWordWrap(False)
        self.strength_label.setObjectName("strength_label")
        self.layout_strength.addWidget(self.strength_label)
        self.strength_progress_bar.setMinimumSize(QtCore.QSize(0, 25))
        self.strength_progress_bar.setMaximumSize(QtCore.QSize(16777215, 25))
        self.strength_progress_bar.setProperty("value", 24)
        self.strength_progress_bar.setObjectName("strength_progress_bar")
        self.layout_strength.addWidget(self.strength_progress_bar)
        self.strength_help_button.setObjectName("strength_help_button")
        self.layout_strength.addWidget(self.strength_help_button)
        self.main_layout.addLayout(self.layout_strength)
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
        self.register_button.setObjectName("register_button")
        self.layout_buttons.addWidget(self.register_button)
        self.main_layout.addLayout(self.layout_buttons)
        self.horizontalLayout_6.addLayout(self.main_layout)

        self.expert_checkBox.stateChanged.connect(
            lambda: error_checking.expert_box_clicked(self.expert_checkBox.isChecked(),
                                                      self.secret_label,
                                                      self.secret_edit,
                                                      self.secret_button,
                                                      self.secret_help_button,
                                                      self.secret_warning))

        # Expert checkbox is hidden by default.
        self.secret_label.hide()
        self.secret_edit.hide()
        self.secret_button.hide()
        self.secret_help_button.hide()

        # Cancel button clicked will close the program.
        self.quit_button.clicked.connect(Registration.close)

        # Each key press on password field will call function.
        self.password_edit.textChanged.connect(lambda: crypto.update_password_bits(self.password_edit,
                                                                                   self.password_bits_value,
                                                                                   self.strength_progress_bar,
                                                                                   self.password_warning))

        # Browse for folder path to save password database file in.
        self.directory_browse_button.clicked.connect(lambda: self.browse_dir())
        self.directory_edit.setReadOnly(True)

        # Set edit to password mode.
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Set range for progress bar.
        self.strength_progress_bar.setRange(0, 1000)
        self.strength_progress_bar.setValue(0)

        # Browse for file path.
        self.secret_button.clicked.connect(lambda: file_explorer.browse_file(self.secret_edit,
                                                                             self.secret_warning))
        self.secret_edit.setReadOnly(True)

        # Ok button clicked; create database from provided fields.
        self.register_button.clicked.connect(lambda: crypto.sign_up(
            error_checking.check_fields(self.directory_edit,
                                        self.directory_warning,
                                        self.password_edit,
                                        self.password_warning,
                                        self.expert_checkBox.isChecked(),
                                        self.secret_edit,
                                        self.secret_warning),
            self.strength_progress_bar.value(),
            self.directory_edit,
            self.expert_checkBox.isChecked(),
            self.secret_edit,
            self.password_edit,
            Registration))

        self.password_view_button.clicked.connect(lambda: error_checking.view_hide_password(self.password_view_button,
                                                                                            self.password_edit))

        # Clear warning labels.
        self.directory_warning.hide()
        self.password_warning.hide()
        self.secret_warning.hide()

        self.retranslateUi(Registration)
        QtCore.QMetaObject.connectSlotsByName(Registration)

        # Attempt to load previously loaded settings.
        self.settings = QSettings("Armour", "Armour Password Manager")

        try:
            Registration.setStyleSheet(self.settings.value("Theme"))
        except:
            pass

        # Help buttons.
        self.directory_help.clicked.connect(lambda: information.directory_edit_registration_moment())
        self.password_help.clicked.connect(lambda: information.password_registration_help_moment())
        self.strength_help_button.clicked.connect(lambda: information.password_strength_help_moment())
        self.secret_help_button.clicked.connect(lambda: information.secret_file_registration_moment())

    def browse_dir(self):
        """
        Browse the directory to find the database save location.
        """
        self.dir_path = QtWidgets.QFileDialog.getExistingDirectory()
        self.directory_edit.setText(self.dir_path)

        # Hides directory warning if directory path is selected.
        if self.directory_edit.text():
            self.directory_warning.hide()

    def retranslateUi(self, Registration):
        _translate = QtCore.QCoreApplication.translate
        Registration.setWindowTitle(_translate("Registration", "Registration"))
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
        self.quit_button.setText(_translate("Registration", "Quit"))
        self.register_button.setText(_translate("Registration", "Register"))
