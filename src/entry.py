import sys

from PyQt5 import QtWidgets
from ui_entry import Ui_Entry


class Entry(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Entry()
        self.ui.setupUi(self)
        self.show()

        self.ui.cancel_button.clicked.connect(Entry.close)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Entry()
    window.show()
    sys.exit(app.exec_())
