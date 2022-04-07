import io
import sys
import pyAesCrypt
from PyQt5.QtCore import QEvent, QEventLoop, QTimer, QSettings
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
import webbrowser


class MainWindow(QMainWindow):
    """
    Functionality for the Main view.
    UI is in the ui_main.py file.
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        # Top menu buttons.
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
        self.ui.actionManual.triggered.connect(lambda: self.open_manual())
        self.ui.actionSave_Exit.triggered.connect(lambda: self.close())

        # Event filter for group widget.
        self.ui.listWidget_groups.installEventFilter(self)
        self.ui.listWidget_groups.itemClicked.connect(self.group_clicked)

        # Password entry widget.
        self.ui.tableWidget_entries.viewport().installEventFilter(self)
        self.ui.tableWidget_entries.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_entries.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_entries.verticalHeader().setVisible(False)
        self.ui.tableWidget_entries.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # Hides entry ID & groupID as they are for internal use only for database control.
        self.ui.tableWidget_entries.setColumnHidden(0, True)
        self.ui.tableWidget_entries.setColumnHidden(7, True)

        # User password that will be used to re-encrypt database (ie: save)
        self.current_password = None

        # Variables used to control password and group entries.
        self.current_database = None
        self.current_selected_group = None
        self.current_selected_entry = None
        self.current_selected_row = False
        self.con = None

        # Hides password & 2FA columns
        self.password_hide_column = PasswordHide()
        self.ui.tableWidget_entries.setItemDelegateForColumn(3, self.password_hide_column)
        self.ui.tableWidget_entries.setItemDelegateForColumn(6, self.password_hide_column)

        # Control for when the user (double)clicks on table column.
        self.ui.tableWidget_entries.itemClicked.connect(self.table_clicked)
        self.ui.tableWidget_entries.doubleClicked.connect(self.table_double_clicked)

        # Timer init for clipboard clearance.
        self.timer = QTimer()

        # Load light mode theme into a variable to have a reference point for light mode if user attempts to
        # switch to dark mode.
        self.light_stylesheet = self.styleSheet()

        # Attempt to load previously loaded settings.
        self.settings = QSettings("Armour", "Armour Password Manager")
        try:
            self.resize(self.settings.value("Window Size"))
            self.move(self.settings.value("Window Position"))
            self.setStyleSheet(self.settings.value("Theme"))
        except:
            pass

        # Tells user what to do upon opening Armour.
        self.ui.statusbar.showMessage("Open or create database using the top left menu.")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """
        When users clicks the x button of the view, the program will save the
        window size and position and open the program back in the same position
        and size when loaded again.
        """
        self.settings.setValue("Window Size", self.size())
        self.settings.setValue("Window Position", self.pos())

    def open_manual(self):
        """
        Opens the user manual.
        """
        webbrowser.open_new("Armour_User_Manual.pdf")

    def new_entry_action(self):
        """
        Adds a new password entry.
        """
        try:
            table_widget.new_or_edit_entry(self.id_of_groups_password_entries, self.con, False)
            self.reload_database()
            self.ui.statusbar.showMessage("New entry complete", 10000)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def edit_entry_action(self):
        """
        Edit password entry.
        """
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
        """
        Delete password entry.
        """
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
        """
        Add group.
        """
        try:
            group_widget.add_to_group(self.cur, self.ui.listWidget_groups, self.con, self)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def edit_group_action(self):
        """
        Edit group.
        """
        try:
            group_widget.edit_group(self.id_of_groups_password_entries,
                                    self.groups[self.id_of_groups_password_entries - 1][1],
                                    self,
                                    self.cur,
                                    self.con)
        except:
            self.ui.statusbar.showMessage("Open or create database using top left menu.", 10000)

    def delete_group_action(self):
        """
        Delete group.
        """
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
        """
        Save current state of database back to database file.
        """
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

                file.close()

            # Overwrite database file with encryption.
            with open(self.current_db_location, 'wb') as file:
                file.write(cipher.getvalue())
                file.close()

            self.ui.statusbar.showMessage("Database saved successfully.", 10000)
        except:
            self.ui.statusbar.showMessage("There is no database open.", 10000)

    def dark_theme_activated(self):
        """
        Set program theme to dark.
        """
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.settings.setValue("Theme", qdarkstyle.load_stylesheet_pyqt5())

    def light_theme_activated(self):
        """
        Set program theme to light.
        """
        self.setStyleSheet(self.light_stylesheet)
        self.settings.setValue("Theme", self.light_stylesheet)

    def group_clicked(self, item):
        """
        Record the group clicked.
        
        :param item:
        Group that was clicked.
        """
        self.current_selected_group = item.text()

        # Clear current selected entry row as new group is clicked.
        self.current_selected_row = False

        self.reload_database()

    def table_clicked(self, item):
        """
        Record the password entry clicked.

        :param item:
        Group that was clicked.
        """
        self.current_selected_entry = item.text()
        self.item_clicked = item
        self.current_selected_row = self.ui.tableWidget_entries.row(item)

    def table_double_clicked(self, item):
        """
        Copy the cell clicked to clipboard for 30 seconds.

        :param item:
        Cell clicked that is to be copied.
        """
        # If the cell that was clicked is the 2FA column.
        if self.ui.tableWidget_entries.currentColumn() == 6:
            # TOTP six digit code.
            totp = pyotp.TOTP(self.current_selected_entry)
            self.current_selected_entry = totp.now()

        # 30 seconds.
        self.count = 30

        # Copy double-clicked cell to clipboard.
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(self.current_selected_entry, mode=clipboard.Clipboard)

        # Timer initialisation.
        self.timer = QTimer()

        # Timer stops in case another timer was previously called.
        self.timer.stop()

        # Call functions each second.
        self.timer.timeout.connect(lambda: self.clipboard_timer(clipboard))
        self.timer.start(1000)

    def clipboard_timer(self, clipboard):
        """
        This method is called every second until the end of the timer.

        :param clipboard:
        The clipboard.
        """
        self.count -= 1
        self.ui.statusbar.showMessage("Item copied to clipboard for " + str(self.count) + " seconds")
        if self.count == 0:
            self.timer.stop()
            clipboard.clear(mode=clipboard.Clipboard)
            self.ui.statusbar.showMessage("Cleared from clipboard", 10000)

    def open_database(self):
        """
        Open the decrypted database.
        """
        # Make a temp dir and file and write the database to it.
        self.tempdir = tempfile.TemporaryDirectory()
        self.tempdir_location = self.tempdir.name + "/armour.db"
        with open(self.tempdir_location, 'wb') as file:
            file.write(self.current_database)
            file.close()

        # Connect to database.
        self.con = database.make_connection(self.tempdir_location)

    def reload_database(self):
        """
        Reload the database to show any changes make.
        """
        self.id_of_groups_password_entries = 1

        # If database not loaded in.
        if self.con is None:
            self.open_database()

        # (Re)load groups
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM groups")
        self.groups = self.cur.fetchall()

        # Clear groups before import
        self.ui.listWidget_groups.clear()
        for group in self.groups:
            if group[1] == self.current_selected_group:
                self.id_of_groups_password_entries = group[0]
            self.ui.listWidget_groups.addItem(group[1])

        self.cur.execute("SELECT * FROM passwords WHERE groupId = (?)", [self.id_of_groups_password_entries])
        self.entries = self.cur.fetchall()

        # (Re)load password entries for specific selected group.
        self.ui.tableWidget_entries.setRowCount(len(self.entries))
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
        """
        Method to register a new database.
        """
        self.reg_window = QtWidgets.QWidget()
        self.UI_Reg = UiRegistration()
        self.UI_Reg.setup_ui_registration(self.reg_window)
        self.reg_window.show()

        # Loop that runs for the duration of the open window.
        loop = QEventLoop()
        # By default, login is hidden on close()
        # This attribute makes it destroyed.
        self.reg_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.reg_window.destroyed.connect(loop.quit)
        loop.exec()

        self.ui.statusbar.showMessage("Database successfully registered, now please login.", 10000)

    def open_database_clicked(self):
        """
        Method to open a previously created database.
        """
        self.login_window = QtWidgets.QWidget()
        self.UI_Log = UiLogin()
        self.UI_Log.setup_ui_login(self.login_window)
        self.login_window.show()

        # Loop that runs for the duration of the open window.
        loop = QEventLoop()
        # By default, login is hidden on close()
        # This attribute makes it destroyed.
        self.login_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.login_window.destroyed.connect(loop.quit)
        loop.exec()

        # Assigns current settings.
        if self.UI_Log.master_password is not None:
            self.current_password = self.UI_Log.master_password
            self.current_database = self.UI_Log.database
            self.current_db_location = self.UI_Log.current_database_location
            self.reload_database()
            self.ui.statusbar.showMessage("Database logged in.", 10000)

    def eventFilter(self, source, event):
        """
        Event filters for clicks on the groups and password entries fields.

        :param source:
        The object being clicked on.

        :param event:
        The right click on the object.
        """
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
