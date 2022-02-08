from PyQt5 import QtWidgets


def browse_file(edit, warning):
    """
    Sets the QLineEdit file path for register and login views.

    :param edit:
    QLineEdit field from either the register or login view.

    :param warning:
    QLabel from either the register or login view.
    """
    file_path = QtWidgets.QFileDialog.getOpenFileName()
    edit.setText(file_path[0])

    if edit.text():
        warning.hide()
