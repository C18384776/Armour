import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sqlite3
from PyQt5 import Qt
from PyQt5 import QtCore

class DataEntry(QWidget):
    def __init__(self):
        super().__init__()

        self.myLayout = QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.email = QLineEdit()
        self.website = QLineEdit()
        self.note = QLineEdit()

        self.addButton = QPushButton("Save to database")

        self.myLayout.setSpacing(5)
        self.myLayout.addWidget(QLabel("Username"))
        self.myLayout.addWidget(self.username)
        self.myLayout.addWidget(QLabel("Password"))
        self.myLayout.addWidget(self.password)
        self.myLayout.addWidget(QLabel("Email"))
        self.myLayout.addWidget(self.email)
        self.myLayout.addWidget(QLabel("Website"))
        self.myLayout.addWidget(self.website)
        self.myLayout.addWidget(QLabel("Note"))
        self.myLayout.addWidget(self.note)
        self.myLayout.addWidget(self.addButton)

        self.addButton.clicked.connect(self.add_to_database)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.myLayout)
        self.setLayout(self.layout)

    def add_to_database(self):
        try:
            a = self.username.text()
            b = self.password.text()
            c = self.email.text()
            d = self.website.text()
            e = self.note.text()

            con = sqlite3.connect("Database.db")
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS info(username TEXT, password TEXT, email TEXT, website TEXT, note TEXT)")
            con.commit()
            cursor.execute("INSERT INTO info VALUES(?,?,?,?,?)", (a, b, c, d, e))
            con.commit()
        finally:
            pass


class MainWindow(QMainWindow):
    def __init__(self, w):
        super().__init__()
        self.setWindowTitle("Database proof of concept")
        self.setWindowIcon(QIcon(""))
        self.setFixedSize(1200,400)
        self.setCentralWidget(w)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DataEntry()
    demo = MainWindow(w)
    demo.show()
    sys.exit(app.exec_())