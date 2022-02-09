from PyQt5 import QtWidgets


def view_hide_password(button, edit):
    """
    Toggles between password protected input and standard text.

    :param button:
    Button user toggles to view/hide password.

    :param edit:
    QLineEdit field of the password.
    """
    if button.text() == "View":
        button.setText("Hide")
        edit.setEchoMode(QtWidgets.QLineEdit.Normal)
    else:
        button.setText("View")
        edit.setEchoMode(QtWidgets.QLineEdit.Password)


def expert_box_clicked(checkbox, label, edit, button, help_button, warning):
    """
    Toggles between expert options on the login and register views.

    :param checkbox:
    Is responsible for toggling the option. True/False.

    :param label:
    QLabel for the secret file.

    :param edit:
    QLineEdit for the secret file.

    :param button:
    QPushButton for the secret file.

    :param help_button:
    QPushButton for the secret help file.

    :param warning:
    QLabel for the secret warning.
    """
    if checkbox:
        label.show()
        edit.show()
        button.show()
        help_button.show()
    else:
        label.hide()
        edit.hide()
        button.hide()
        help_button.hide()
        warning.hide()


def check_fields(dir_edit, dir_warning, pass_edit, pass_warning, checkbox, secret_edit, secret_warning):
    error = 0

    if dir_edit.text() == '':
        dir_warning.show()
        error = 1

    if pass_edit.text() == '':
        pass_warning.show()
        error = 1

    if checkbox:
        if secret_edit.text() == '':
            secret_warning.show()
            error = 1

    if error == 1:
        return True
    else:
        return False
