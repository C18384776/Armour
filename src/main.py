import sys

from PyQt5.QtCore import QEvent, QEventLoop, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui_main import *
from registration import UiRegistration
from login import UiLogin
import database
import group_widget
import table_widget
import pyotp
import qdarkstyle
import tempfile


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.listWidget_groups.installEventFilter(self)
        self.ui.listWidget_groups.itemClicked.connect(self.group_clicked)

        self.ui.tableWidget_entries.viewport().installEventFilter(self)

        self.ui.actionNew_Database.triggered.connect(lambda: self.new_database_clicked())
        self.ui.actionOpen_Database.triggered.connect(lambda: self.open_database_clicked())
        self.ui.actionAdd_Group.triggered.connect(lambda: group_widget.add_to_group(self.cur,
                                                                                    self.ui.listWidget_groups,
                                                                                    self.con,
                                                                                    self))
        self.ui.actionEdit_Group.triggered.\
            connect(lambda: group_widget.edit_group(self.id_of_groups_password_entries,
                                                    self.groups[self.id_of_groups_password_entries][1],
                                                    self,
                                                    self.cur,
                                                    self.con))

        self.ui.actionDelete_Group.triggered.\
            connect(lambda: group_widget.delete_group(self.groups[self.id_of_groups_password_entries][0],
                                                      self.groups[self.id_of_groups_password_entries][1],
                                                      self,
                                                      self.ui.listWidget_groups,
                                                      self.con,
                                                      True))

        self.ui.actionDark_Theme.triggered.connect(lambda: self.dark_theme_activated())
        self.ui.actionLight_Theme.triggered.connect(lambda: self.light_theme_activated())

        self.ui.tableWidget_entries.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_entries.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_entries.verticalHeader().setVisible(False)
        self.ui.tableWidget_entries.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.tableWidget_entries.setColumnHidden(0, True)  # Hides entry ID.
        self.ui.tableWidget_entries.setColumnHidden(7, True)  # Hides entry groupID.

        # User password that will be used to re-encrypt database (ie: save)
        self.current_password = None

        #
        self.current_database = None
        self.current_selected_group = None
        self.current_selected_entry = None
        self.current_selected_row = False
        self.con = None

        # Hides password & 2FA columns
        self.password_hide_column = PasswordHide()
        self.ui.tableWidget_entries.setItemDelegateForColumn(3, self.password_hide_column)
        self.ui.tableWidget_entries.setItemDelegateForColumn(6, self.password_hide_column)
        self.ui.tableWidget_entries.itemClicked.connect(self.table_clicked)

        self.ui.tableWidget_entries.doubleClicked.connect(self.table_double_clicked)
        self.timer = QTimer()
        self.light_stylesheet = self.styleSheet()

    def dark_theme_activated(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def light_theme_activated(self):
        self.setStyleSheet(self.light_stylesheet)

    def group_clicked(self, item):
        self.current_selected_group = item.text()
        print("Clicked group: {}".format(item.text()))

        # Clear current selected entry row as new group is clicked.
        self.current_selected_row = False

        self.reload_database()

    def table_clicked(self, item):
        self.current_selected_entry = item.text()
        self.current_selected_row = self.ui.tableWidget_entries.row(item)
        print("Clicked entry: {}".format(item.text()))
        print(self.ui.tableWidget_entries.row(item))
        print(self.ui.tableWidget_entries.item(self.ui.tableWidget_entries.row(item), 3).text())
        # self.reload_database()

    def table_double_clicked(self, item):
        print("Inside double clicked")
        if self.ui.tableWidget_entries.currentColumn() == 6:
            # TOTP code.
            totp = pyotp.TOTP(self.current_selected_entry)
            self.current_selected_entry = totp.now()
        self.start = False
        self.count = 30
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(self.current_selected_entry, mode=clipboard.Clipboard)
        print("Current Column: " + str(self.ui.tableWidget_entries.currentColumn()))
        self.timer.stop()
        self.timer.timeout.connect(lambda: self.clipboard_timer(clipboard))
        self.timer.start(1000)

    def clipboard_timer(self, clipboard):
        self.count -= 1
        print(self.count)
        if self.count == 0:
            self.timer.stop()
            clipboard.clear(mode=clipboard.Clipboard)
            print("Clipboard cleared")

    def open_database(self):
        tempdir = tempfile.TemporaryDirectory()
        tempdir_location = tempdir.name + "/armour.db"
        print(tempdir_location)

        with open(tempdir_location, 'wb') as file:
            file.write(self.current_database)
            file.close()

        self.con = database.make_connection(tempdir_location)
        # Need to close database connection someday.

    def reload_database(self):
        self.id_of_groups_password_entries = 1

        # If database not loaded in.
        if self.con is None:
            self.open_database()
            print("CONNECTION HAPPENED")

        # (Re)load groups
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM groups")
        self.groups = self.cur.fetchall()
        print(self.groups)
        # Clear groups before import
        self.ui.listWidget_groups.clear()
        for group in self.groups:
            if group[1] == self.current_selected_group:
                self.id_of_groups_password_entries = group[0]
            self.ui.listWidget_groups.addItem(group[1])

        print("id of group pass entry: {}".format(self.id_of_groups_password_entries))
        self.cur.execute("SELECT * FROM passwords WHERE groupId = (?)", [self.id_of_groups_password_entries])
        self.entries = self.cur.fetchall()

        # (Re)load password entries for specific selected group.
        self.ui.tableWidget_entries.setRowCount(len(self.entries))
        print(self.entries)
        row = 0
        for entry in self.entries:
            self.ui.tableWidget_entries.setItem(row, 0, QtWidgets.QTableWidgetItem(str(entry[0])))
            self.ui.tableWidget_entries.setItem(row, 1, QtWidgets.QTableWidgetItem(str(entry[1])))
            self.ui.tableWidget_entries.setItem(row, 2, QtWidgets.QTableWidgetItem(str(entry[2])))
            self.ui.tableWidget_entries.setItem(row, 3, QtWidgets.QTableWidgetItem(str(entry[3])))
            self.ui.tableWidget_entries.setItem(row, 4, QtWidgets.QTableWidgetItem(str(entry[4])))
            self.ui.tableWidget_entries.setItem(row, 5, QtWidgets.QTableWidgetItem(str(entry[5])))
            self.ui.tableWidget_entries.setItem(row, 6, QtWidgets.QTableWidgetItem(str(entry[6])))
            self.ui.tableWidget_entries.setItem(row, 7, QtWidgets.QTableWidgetItem(str(entry[7])))
            row += 1

    def new_database_clicked(self):
        self.reg_window = QtWidgets.QWidget()
        self.UI_Reg = UiRegistration()
        self.UI_Reg.setup_ui_registration(self.reg_window)
        self.reg_window.show()
        print("Register Opened")

    def open_database_clicked(self):
        self.login_window = QtWidgets.QWidget()
        self.UI_Log = UiLogin()
        self.UI_Log.setup_ui_login(self.login_window)
        self.login_window.show()
        loop = QEventLoop()
        # By default, login is hidden on close()
        # This attribute makes it destroyed.
        self.login_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.login_window.destroyed.connect(loop.quit)
        loop.exec()
        print("Login Opened")
        # Assigns current settings.
        if self.UI_Log.master_password is not None:
            self.current_password = self.UI_Log.master_password
            self.current_database = self.UI_Log.database
            print("password passed {}".format(self.current_password))
            print("database passed {}".format(self.current_database))
            self.reload_database()

    def eventFilter(self, source, event):
        # Event filter for QTableWidget
        if event.type() == QtCore.QEvent.MouseButtonPress:
            success = table_widget.table_widget(source, event, self.ui.tableWidget_entries,
                                                self, self.con, self.id_of_groups_password_entries,
                                                self.entries, self.current_selected_row)
            if success is True:
                self.reload_database()
            elif success is False:
                print("QTableWidget event has closed.")
            else:
                print("No response received in eventFilter() in main.py")

        # Event filter for QListWidget
        if event.type() == QEvent.ContextMenu and source is self.ui.listWidget_groups:
            success = group_widget.group_widget(source, event, self.cur, self.ui.listWidget_groups, self.con, self)
            if success is True:
                self.reload_database()
            else:
                print("Something in QListWidget went wrong.")
        return super(MainWindow, self).eventFilter(source, event)


class PasswordHide(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        style = option.widget.style() or QtWidgets.QApplication.style()
        hint = style.styleHint(QtWidgets.QStyle.SH_LineEdit_PasswordCharacter)
        option.text = chr(hint) * len(option.text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
