import io
import sys

import pyAesCrypt
from PyQt5.QtCore import QEvent, QEventLoop, QTimer, QSettings
from PyQt5.QtWidgets import QMainWindow, QApplication

from src import crypto
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
        self.ui.actionAdd_Group.triggered.connect(lambda: self.add_group_action())

        self.ui.actionEdit_Group.triggered.connect(lambda: self.edit_group_action())

        self.ui.actionDelete_Group.triggered.connect(lambda: self.delete_group_action())

        self.ui.actionDark_Theme.triggered.connect(lambda: self.dark_theme_activated())
        self.ui.actionLight_Theme.triggered.connect(lambda: self.light_theme_activated())
        self.ui.actionSave_Database.triggered.connect(lambda: self.save_requested())

        self.ui.actionNew_Entry.triggered.connect(lambda: self.new_entry_action())
        self.ui.actionEdit_Entry.triggered.connect(lambda: self.edit_entry_action())
        self.ui.actionDelete_Entry.triggered.connect(lambda: self.delete_entry_action())

        self.ui.tableWidget_entries.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ui.tableWidget_entries.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_entries.verticalHeader().setVisible(False)
        self.ui.tableWidget_entries.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.tableWidget_entries.setColumnHidden(0, True)  # Hides entry ID.
        self.ui.tableWidget_entries.setColumnHidden(7, True)  # Hides entry groupID.

        # User password that will be used to re-encrypt database (ie: save)
        self.current_password = None

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

        self.settings = QSettings("Armour", "Armour Password Manager")
        print(self.settings.fileName())

        try:
            self.resize(self.settings.value("Window Size"))
            self.move(self.settings.value("Window Position"))
            self.setStyleSheet(self.settings.value("Theme"))
        except:
            pass

        self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.settings.setValue("Window Size", self.size())
        self.settings.setValue("Window Position", self.pos())
        print("Closed event")

    def new_entry_action(self):
        try:
            table_widget.new_or_edit_entry(self.id_of_groups_password_entries, self.con, False)
            self.reload_database()
            self.ui.statusbar.showMessage("New entry complete", 10000)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def edit_entry_action(self):
        try:
            table_widget.new_or_edit_entry(self.id_of_groups_password_entries,
                                           self.con,
                                           True,
                                           self.entries,
                                           self.current_selected_row)
            self.reload_database()
            self.ui.statusbar.showMessage("Edit entry complete", 1000)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def delete_entry_action(self):
        try:
            table_widget.delete_entry(self.current_selected_row,
                                      self.ui.tableWidget_entries.item(self.current_selected_row, 0).text(),
                                      self.ui.tableWidget_entries.item(self.current_selected_row, 7).text(),
                                      self,
                                      self.con)
            self.reload_database()
            self.ui.statusbar.showMessage("Delete entry complete", 1000)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def add_group_action(self):
        try:
            group_widget.add_to_group(self.cur, self.ui.listWidget_groups, self.con, self)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def edit_group_action(self):
        try:
            group_widget.edit_group(self.id_of_groups_password_entries,
                                    self.groups[self.id_of_groups_password_entries - 1][1],
                                    self,
                                    self.cur,
                                    self.con)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def delete_group_action(self):
        try:
            group_widget.delete_group(self.groups[self.id_of_groups_password_entries - 1][0],
                                      self.groups[self.id_of_groups_password_entries - 1][1],
                                      self,
                                      self.ui.listWidget_groups,
                                      self.con,
                                      True)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def save_requested(self):
        buffer_size = 64 * 1024

        try:
            with open(self.tempdir_location, 'rb') as file:

                # Read initial unencrypted database and copy its contents to a variable.
                content = file.read()

                # Input plaintext binary stream
                plaintext = io.BytesIO(content)

                # Initialize ciphertext binary stream
                cipher = io.BytesIO()

                # Encrypt stream
                pyAesCrypt.encryptStream(plaintext, cipher, self.current_password, buffer_size)

                # Print encrypted data
                print("This is the ciphertext:\n" + str(cipher.getvalue()))

                file.close()
            print(self.current_database)

            # Overwrite database file with encryption.
            with open(self.current_db_location, 'wb') as file:
                file.write(cipher.getvalue())
                file.close()
        except:
            print("Error occurred in method main.py save_requested()")

    def dark_theme_activated(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.settings.setValue("Theme", qdarkstyle.load_stylesheet_pyqt5())

    def light_theme_activated(self):
        self.setStyleSheet(self.light_stylesheet)
        self.settings.setValue("Theme", self.light_stylesheet)

    def group_clicked(self, item):
        self.current_selected_group = item.text()
        print("Clicked group: {}".format(item.text()))

        # Clear current selected entry row as new group is clicked.
        self.current_selected_row = False

        self.reload_database()

    def table_clicked(self, item):
        self.current_selected_entry = item.text()
        self.item_clicked = item
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
        self.count = 30
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(self.current_selected_entry, mode=clipboard.Clipboard)
        print("Current Column: " + str(self.ui.tableWidget_entries.currentColumn()))
        # Timer initialisation.
        self.timer = QTimer()

        # Timer stops in case another timer was previously called.
        self.timer.stop()

        # Call functions each second.
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
        self.tempdir = tempfile.TemporaryDirectory()
        self.tempdir_location = self.tempdir.name + "/armour.db"
        print(self.tempdir_location)

        with open(self.tempdir_location, 'wb') as file:
            file.write(self.current_database)
            file.close()

        self.con = database.make_connection(self.tempdir_location)

        # Need to close database connection someday.
        # Cleanup cleans up directory.
        # self.tempdir.cleanup()

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
            self.current_db_location = self.UI_Log.current_database_location
            print("password passed {}".format(self.current_password))
            print("database passed {}".format(self.current_database))
            print("Db directory location {}".format(self.current_db_location))
            self.reload_database()

    def eventFilter(self, source, event):
        # Event filter for QTableWidget
        try:
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
        except:
            self.ui.statusbar.showMessage("To use the password manager please login or register at the top "
                                          "right corner", 10000)

        # Event filter for QListWidget
        try:
            if event.type() == QEvent.ContextMenu and source is self.ui.listWidget_groups:
                # Display menu on group selected.
                success = group_widget.group_widget(source, event, self.cur, self.ui.listWidget_groups, self.con, self)
                # Reload database when group was updated.
                if success is True:
                    self.reload_database()
                else:
                    print("Something in QListWidget went wrong.")
        except:
            self.ui.statusbar.showMessage("To use the password manager please login or register at the top right "
                                          "corner", 10000)

        return super(MainWindow, self).eventFilter(source, event)


class PasswordHide(QtWidgets.QStyledItemDelegate):
    """
    Used to convert plaintext to password text (asterisks ****) in QTableWidget.
    """
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
