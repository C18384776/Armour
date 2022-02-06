from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from zxcvbn import zxcvbn
import math

class Ui_Registration(object):
    def setupUi(self, Registration):
        Registration.setObjectName("Registration")
        Registration.resize(465, 239)
        self.verticalLayout = QtWidgets.QVBoxLayout(Registration)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_directory = QtWidgets.QHBoxLayout()
        self.layout_directory.setObjectName("layout_directory")
        self.directory_label = QtWidgets.QLabel(Registration)
        self.directory_label.setMinimumSize(QtCore.QSize(60, 29))
        self.directory_label.setMaximumSize(QtCore.QSize(60, 29))
        self.directory_label.setObjectName("directory_label")
        self.layout_directory.addWidget(self.directory_label)
        self.directory_edit = QtWidgets.QLineEdit(Registration)
        self.directory_edit.setMinimumSize(QtCore.QSize(256, 29))
        self.directory_edit.setMaximumSize(QtCore.QSize(256, 29))
        self.directory_edit.setObjectName("directory_edit")
        self.layout_directory.addWidget(self.directory_edit)
        self.directory_browse_button = QtWidgets.QPushButton(Registration)
        self.directory_browse_button.setMinimumSize(QtCore.QSize(80, 25))
        self.directory_browse_button.setMaximumSize(QtCore.QSize(80, 25))
        self.directory_browse_button.setObjectName("directory_browse_button")
        self.layout_directory.addWidget(self.directory_browse_button)
        self.directory_help = QtWidgets.QToolButton(Registration)
        self.directory_help.setMinimumSize(QtCore.QSize(23, 24))
        self.directory_help.setMaximumSize(QtCore.QSize(23, 24))
        self.directory_help.setObjectName("directory_help")
        self.layout_directory.addWidget(self.directory_help)
        self.verticalLayout.addLayout(self.layout_directory)
        self.layout_password = QtWidgets.QHBoxLayout()
        self.layout_password.setObjectName("layout_password")
        self.password_label = QtWidgets.QLabel(Registration)
        self.password_label.setMinimumSize(QtCore.QSize(61, 29))
        self.password_label.setMaximumSize(QtCore.QSize(61, 29))
        self.password_label.setObjectName("password_label")
        self.layout_password.addWidget(self.password_label)
        self.password_edit = QtWidgets.QLineEdit(Registration)
        self.password_edit.setMinimumSize(QtCore.QSize(256, 29))
        self.password_edit.setMaximumSize(QtCore.QSize(256, 29))
        self.password_edit.setObjectName("password_edit")
        self.layout_password.addWidget(self.password_edit)
        self.password_help = QtWidgets.QToolButton(Registration)
        self.password_help.setMinimumSize(QtCore.QSize(23, 24))
        self.password_help.setMaximumSize(QtCore.QSize(23, 24))
        self.password_help.setObjectName("password_help")
        self.layout_password.addWidget(self.password_help)
        self.verticalLayout.addLayout(self.layout_password)
        self.layout_strength = QtWidgets.QHBoxLayout()
        self.layout_strength.setObjectName("layout_strength")
        self.strength_label = QtWidgets.QLabel(Registration)
        self.strength_label.setEnabled(True)
        self.strength_label.setMinimumSize(QtCore.QSize(61, 46))
        self.strength_label.setMaximumSize(QtCore.QSize(61, 46))
        self.strength_label.setWordWrap(False)
        self.strength_label.setObjectName("strength_label")
        self.layout_strength.addWidget(self.strength_label)
        self.strength_progress_bar = QtWidgets.QProgressBar(Registration)
        self.strength_progress_bar.setMinimumSize(QtCore.QSize(253, 25))
        self.strength_progress_bar.setMaximumSize(QtCore.QSize(253, 25))
        self.strength_progress_bar.setProperty("value", 0)
        self.strength_progress_bar.setObjectName("strength_progress_bar")
        self.layout_strength.addWidget(self.strength_progress_bar)
        self.strength_help_button = QtWidgets.QToolButton(Registration)
        self.strength_help_button.setMinimumSize(QtCore.QSize(23, 24))
        self.strength_help_button.setMaximumSize(QtCore.QSize(23, 24))
        self.strength_help_button.setObjectName("strength_help_button")
        self.layout_strength.addWidget(self.strength_help_button)
        self.verticalLayout.addLayout(self.layout_strength)
        self.expert_checkBox = QtWidgets.QCheckBox(Registration)
        self.expert_checkBox.setObjectName("expert_checkBox")
        self.verticalLayout.addWidget(self.expert_checkBox)
        self.layout_secret_file = QtWidgets.QHBoxLayout()
        self.layout_secret_file.setObjectName("layout_secret_file")
        self.secret_label = QtWidgets.QLabel(Registration)
        self.secret_label.setMinimumSize(QtCore.QSize(68, 29))
        self.secret_label.setMaximumSize(QtCore.QSize(68, 29))
        self.secret_label.setObjectName("secret_label")
        self.layout_secret_file.addWidget(self.secret_label)
        self.secret_edit = QtWidgets.QLineEdit(Registration)
        self.secret_edit.setMinimumSize(QtCore.QSize(256, 29))
        self.secret_edit.setMaximumSize(QtCore.QSize(256, 29))
        self.secret_edit.setObjectName("secret_edit")
        self.layout_secret_file.addWidget(self.secret_edit)
        self.secret_button = QtWidgets.QPushButton(Registration)
        self.secret_button.setMinimumSize(QtCore.QSize(80, 25))
        self.secret_button.setMaximumSize(QtCore.QSize(80, 25))
        self.secret_button.setObjectName("secret_button")
        self.layout_secret_file.addWidget(self.secret_button)
        self.secret_help_button = QtWidgets.QToolButton(Registration)
        self.secret_help_button.setMinimumSize(QtCore.QSize(23, 24))
        self.secret_help_button.setMaximumSize(QtCore.QSize(23, 24))
        self.secret_help_button.setObjectName("secret_help_button")
        self.layout_secret_file.addWidget(self.secret_help_button)
        self.verticalLayout.addLayout(self.layout_secret_file)
        self.layout_ok_and_cancel = QtWidgets.QHBoxLayout()
        self.layout_ok_and_cancel.setObjectName("layout_ok_and_cancel")
        self.cancel_button = QtWidgets.QPushButton(Registration)
        self.cancel_button.setMinimumSize(QtCore.QSize(83, 25))
        self.cancel_button.setMaximumSize(QtCore.QSize(83, 25))
        self.cancel_button.setObjectName("cancel_button")
        self.layout_ok_and_cancel.addWidget(self.cancel_button)
        self.ok_button = QtWidgets.QPushButton(Registration)
        self.ok_button.setMinimumSize(QtCore.QSize(83, 25))
        self.ok_button.setMaximumSize(QtCore.QSize(83, 25))
        self.ok_button.setObjectName("ok_button")
        self.layout_ok_and_cancel.addWidget(self.ok_button)
        self.verticalLayout.addLayout(self.layout_ok_and_cancel)

        # Expert checkbox is hidden by default.
        self.expert_checkBox.stateChanged.connect(lambda: self.expert_box_clicked())
        self.secret_label.hide()
        self.secret_edit.hide()
        self.secret_button.hide()
        self.secret_help_button.hide()

        # Cancel button clicked will close the program.
        self.cancel_button.clicked.connect(QtWidgets.QApplication.instance().quit)

        # Each key press on password field will call function.
        self.password_edit.textChanged.connect(lambda: self.update_password_bits())

        # Browse for folder path to save password database file in.
        self.directory_browse_button.clicked.connect(lambda: self.browse_dir())
        self.directory_edit.setReadOnly(True)

        # Set edit to password mode.
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Set range for progress bar.
        self.strength_progress_bar.setRange(0, 1000)

        self.retranslateUi(Registration)
        QtCore.QMetaObject.connectSlotsByName(Registration)

    def expert_box_clicked(self):
        if self.expert_checkBox.isChecked() == False:
            self.secret_label.hide()
            self.secret_edit.hide()
            self.secret_button.hide()
            self.secret_help_button.hide()
        else:
            self.secret_label.show()
            self.secret_edit.show()
            self.secret_button.show()
            self.secret_help_button.show()

    def update_password_bits(self):
        # Entropy is calculated when text field is not empty.
        if self.password_edit.text():
            result = zxcvbn(self.password_edit.text())
            print(math.log2(result["guesses"]).__floor__())
            self.strength_progress_bar.setValue(math.log2(result["guesses"]).__floor__())
        else:
            pass

    def browse_dir(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory()
        self.directory_edit.setText(dir_path)
        print(dir_path)

    def retranslateUi(self, Registration):
        _translate = QtCore.QCoreApplication.translate
        Registration.setWindowTitle(_translate("Registration", "Registration"))
        self.directory_label.setText(_translate("Registration", "Directory"))
        self.directory_browse_button.setText(_translate("Registration", "Browse"))
        self.directory_help.setText(_translate("Registration", "?"))
        self.password_label.setText(_translate("Registration", "Password"))
        self.password_help.setText(_translate("Registration", "?"))
        self.strength_label.setText(_translate("Registration", "Strength"))
        self.strength_progress_bar.setFormat(_translate("Registration", "%v bits"))
        self.strength_help_button.setText(_translate("Registration", "?"))
        self.expert_checkBox.setText(_translate("Registration", "Expert Options"))
        self.secret_label.setText(_translate("Registration", "<html><head/><body><p>Secret File</p></body></html>"))
        self.secret_button.setText(_translate("Registration", "Browse"))
        self.secret_help_button.setText(_translate("Registration", "?"))
        self.cancel_button.setText(_translate("Registration", "Cancel"))
        self.ok_button.setText(_translate("Registration", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Registration = QtWidgets.QWidget()
    ui = Ui_Registration()
    ui.setupUi(Registration)
    Registration.show()
    sys.exit(app.exec_())
