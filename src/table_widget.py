import datetime

import pyotp
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtWidgets import QAction, QMessageBox, QApplication
import database
from entry import Entry
from prevpass import PreviousPasswords

global entry_result


def table_widget(source, event, table_wid, main_window, connection, id_of_group, entries, row):
    """
    Generate a menu for password entries tables.

    :param source:
    The object being clicked on.

    :param event:
    The right click on the object.

    :param table_wid:
    QTableWidget from the main window.

    :param main_window:
    Main window class.

    :param connection:
    Database connection

    :param id_of_group:
    The id of the group the user is in.

    :param entries:
    The password entries of the group of entries.

    :param row:
    The password entry row clicked.
    """
    if event.button() == QtCore.Qt.RightButton:
        index = table_wid.indexAt(event.pos())

        # Initialise a right click menu.
        menu = QtWidgets.QMenu()
        copy_username_action = QAction("Copy Username")
        copy_password_action = QAction("Copy Password")
        copy_totp_action = QAction("Copy 2FA")
        new_entry_action = QAction("New Entry")
        edit_entry_action = QAction("Edit Entry")
        delete_entry_action = QAction("Delete Entry")
        open_previous_passwords = QAction("Open Previous Passwords")

        menu.addAction(copy_username_action)
        menu.addAction(copy_password_action)
        menu.addAction(copy_totp_action)
        menu.addSeparator()
        menu.addAction(new_entry_action)
        menu.addAction(edit_entry_action)
        menu.addAction(delete_entry_action)
        menu.addSeparator()
        menu.addAction(open_previous_passwords)

        if index.data() is not None:

            menu_select = menu.exec(event.globalPos())

            # What menu item the user selects.
            if menu_select == copy_username_action:
                temp_value_from_click = main_window.ui.tableWidget_entries.item(
                    main_window.ui.tableWidget_entries.row(main_window.item_clicked), 2).text()

                copy_item(temp_value_from_click, main_window)

            elif menu_select == copy_password_action:
                temp_value_from_click = main_window.ui.tableWidget_entries.item(
                    main_window.ui.tableWidget_entries.row(main_window.item_clicked), 3).text()

                copy_item(temp_value_from_click, main_window)

            elif menu_select == copy_totp_action:
                temp_value_from_click = main_window.ui.tableWidget_entries.item(
                    main_window.ui.tableWidget_entries.row(main_window.item_clicked), 6).text()

                copy_item(temp_value_from_click, main_window, True)

            elif menu_select == new_entry_action:
                new_entry_list = new_or_edit_entry(id_of_group, connection, False, main_window, entries, row)
                return new_entry_list

            elif menu_select == edit_entry_action:
                edit_entry_list = new_or_edit_entry(id_of_group, connection, True, main_window, entries, row)
                return edit_entry_list

            elif menu_select == delete_entry_action:
                # Selected row to delete.
                row_to_remove = index.row()
                # Selected row ID from database.
                id_of_entry = table_wid.item(row_to_remove, 0)
                # Selected row group ID from database.
                group_id_of_entry = table_wid.item(row_to_remove, 7)
                delete_entry(index.row(), id_of_entry.text(), group_id_of_entry.text(), main_window, connection)
            elif menu_select == open_previous_passwords:
                previous_passwords_window(entries, row, connection)
            else:
                print("user clicked out of group.")

            return True
        # User right clicks empty space.
        else:
            # Clears the big menu above if empty space clicked.
            menu.clear()

            # Since no password entry was clicked, there can only be an option to add a new entry.
            menu.addAction(new_entry_action)
            menu_select = menu.exec(event.globalPos())

            if menu_select == new_entry_action:
                new_entry_list = new_or_edit_entry(id_of_group, connection, False, main_window, entries, row)
                return new_entry_list

            return True
    elif event.button() == QtCore.Qt.LeftButton:
        index = table_wid.indexAt(event.pos())


def copy_item(item, main_window, trigger=False):
    """
    Copy selected item to clipboard.

    :param item:
    Item to be copied to clipboard.

    :param main_window:
    Main window class.

    :param trigger:
    Check if totp code
    """
    # Check if TOTP code requested.
    if trigger:
        # Initialisation of TOTP code.
        totp = pyotp.TOTP(item)
        # Generate time based code.
        item = totp.now()

    # Amount of seconds content will be copied to clipboard.
    main_window.count = 30

    # Setup and copy item to clipboard.
    clipboard = QApplication.clipboard()
    clipboard.clear(mode=clipboard.Clipboard)
    clipboard.setText(item, mode=clipboard.Clipboard)

    # Timer initialisation, stop the timer incase a current count is in progress,
    # and run the timer for 30 seconds.
    main_window.timer = QTimer()
    main_window.timer.stop()
    main_window.timer.timeout.connect(lambda: clipboard_timer(clipboard, main_window))
    main_window.timer.start(1000)


def clipboard_timer(clipboard, main_window):
    """
    This method is called every second until the end of the timer.

    :param main_window:
    Main window class.

    :param clipboard:
    The clipboard.

    """
    # Each call remove a second and display seconds to statusbar for user.
    main_window.count -= 1
    main_window.ui.statusbar.showMessage("Item copied to clipboard for " + str(main_window.count) + " seconds")

    # Stop the timer, clear the clipboard and display a statusbar for the user about this action.
    if main_window.count == 0:
        main_window.timer.stop()
        clipboard.clear(mode=clipboard.Clipboard)
        main_window.ui.statusbar.showMessage("Cleared from clipboard", 10000)


def get_entry_fields(UI_entry):
    """
    Responsible for getting password entry fields from an existing database entry.
    """
    result = UI_entry.get_entry_fields()
    globals()['entry_result'] = result


def new_or_edit_entry(id_of_group, connection, new_or_edit, main_window, entries=False, row=False):
    """
    Add or edit a password entry.

    :param id_of_group:
    The id of the group the user is in.

    :param connection:
    Database connection.

    :param new_or_edit:
    Check if the user wants to add a new entry or edit an entry.

    :param entries:
    The password entries of that group.

    :param row:
    The specific row that was selected by the user.
    """
    # Setup password entry window.
    UI_entry = Entry()
    UI_entry.__init__()
    # False is if it's a new password entry.
    # Else it is an edit entry - fill out the fields with their contents.
    if row is False:
        print("Row is false in new_or_edit_entry")
    else:
        entry = entries[row]
        if new_or_edit is True:
            UI_entry.ui.website_lineEdit.setText(entry[1])
            UI_entry.ui.username_lineEdit.setText(entry[2])
            UI_entry.ui.password_lineEdit.setText(entry[3])
            UI_entry.ui.repeat_lineEdit.setText(entry[3])
            old_password = entry[3]
            UI_entry.ui.url_lineEdit.setText(entry[4])
            UI_entry.ui.twofa_lineEdit.setText(entry[6])

    # Detect that button was clicked from here and pass down variables
    UI_entry.ui.submit_button.clicked.connect(lambda: UI_entry.submitted())
    UI_entry.ui.submit_button.clicked.connect(lambda: get_entry_fields(UI_entry))
    UI_entry.show()

    # Start a loop until password entry window is destroyed.
    loop = QEventLoop()
    # By default, login is hidden on close()
    # This attribute makes it destroyed.
    UI_entry.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    UI_entry.destroyed.connect(loop.quit)
    loop.exec()

    # Insert fields to database.
    if new_or_edit is False:
        try:
            if entry_result[5] is False:
                return False
            else:
                insert_entry(entry_result, id_of_group, connection)
                globals()['entry_result'][5] = False
                main_window.ui.statusbar.showMessage("Password entry successfully created.", 10000)
                return True
        except NameError:
            print("table_widget.py: entry_result does not exist.")
    # Edit fields in database.
    else:
        try:
            if entry_result[5] is False:
                return False
            else:
                edit_entry(entry_result, entry[0], connection, old_password)
                globals()['entry_result'][5] = False
                main_window.ui.statusbar.showMessage("Password entry successfully edited.", 10000)
                return True
        except NameError:
            print("table_widget.py: entry_result does not exist.")


def insert_entry(entry_result, id_of_group, connection):
    """
    Insert an entry into the database.

    :param entry_result:
    List of items that need to be inserted to database.

    :param id_of_group:
    The id of group to insert password entry into.

    :param connection:
    Database connection
    """
    # SQL query to insert password entry into database.
    sql_entry_insert = """INSERT INTO passwords( passwordWebsite, 
    passwordName, passwordPassword, passwordUrl, 
    passwordCreation, password2FA, groupId) VALUES(?,?,?,?,?,?,?)"""

    # Password entry insert order, run query and commit to database.
    pass_entry_one = [entry_result[0], entry_result[1], entry_result[2],
                      entry_result[3], datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                      entry_result[4], id_of_group]
    database.database_query(connection, sql_entry_insert, pass_entry_one)
    connection.commit()


def edit_entry(entry_result, entry_id, connection, old_password):
    """
    Edit an entry in the database.

    :param entry_result:
    List of items that need to be updated to database.

    :param entry_id:
    The specific entry id that needs to be edited.

    :param connection:
    The database connection.

    :param old_password:
    The old password is used to save to the previous passwords table.
    """

    # SQL query to update password entry in database.
    sql_entry_edit = """UPDATE passwords SET passwordWebsite=(?),
    passwordName=(?), passwordPassword=(?), 
    passwordUrl=(?), password2FA=(?) 
    WHERE passwordId = (?)"""

    # Password entry update order and run.
    pass_entry_one = [entry_result[0], entry_result[1], entry_result[2],
                      entry_result[3], entry_result[4], entry_id]
    database.database_query(connection, sql_entry_edit, pass_entry_one)

    # SQL query to insert password entry into database.
    sql_prev_pass_insert = """INSERT INTO previous_passwords(prevPassword, 
    prevPasswordCreation, passwordId) VALUES(?,?,?)"""

    # Password entry insert order, run and commit.
    prev_pass_entry = [old_password,
                       datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                       entry_id]
    database.database_query(connection, sql_prev_pass_insert, prev_pass_entry)
    connection.commit()


def delete_entry(row_to_delete, id_of_entry, group_id_of_entry, main_window, connection):
    """
    Delete an entry from the database.

    :param row_to_delete:
    The specific password entry row that needs to be deleted.

    :param id_of_entry:
    The specific id of the password entry that needs to be deleted.

    :param group_id_of_entry:
    The group id of the specific password entry that needs to be deleted.

    :param main_window:
    Main window class.

    :param connection:
    Database connection.
    """
    # Ask users if they want to remove an entry.
    reply = QMessageBox.question(main_window, "Remove a group",
                                 "Do you really want to remove this entry?\n"
                                 "It will be moved to the Recycle Bin or deleted entirely "
                                 "if it's there already.",
                                 QMessageBox.Yes | QMessageBox.No)

    # Move to recycle bin if not in it already; otherwise delete forever.
    if reply == QMessageBox.Yes and int(group_id_of_entry) != 5:
        sql_entry_move_to_bin = """UPDATE passwords SET groupId = 5 WHERE passwordId = (?)"""
        database.database_query(connection, sql_entry_move_to_bin, [id_of_entry])
        connection.commit()
        main_window.ui.statusbar.showMessage("Password entry successfully moved to recycle bin.", 10000)
        return True
    elif reply == QMessageBox.Yes and int(group_id_of_entry) == 5:
        sql_delete_entry = """DELETE FROM passwords WHERE passwordId = (?)"""
        database.database_query(connection, sql_delete_entry, [id_of_entry])
        connection.commit()
        main_window.ui.statusbar.showMessage("Password entry successfully deleted.", 10000)
        return True


def previous_passwords_window(entries, row, connection):
    """
    Load the previous password view for a specific password entry.

    :param entries:
    The password entries of the group of entries.

    :param row:
    The specific password entry row that the user wants to get previous passwords from.

    :param connection:
    Database connection.
    """
    # Load the particular row of an entry.
    entry = entries[row]

    # Initialise previous password view.
    UI_prevpass = PreviousPasswords()
    UI_prevpass.__init__()

    # Method that loads all previous passwords associated with the entry.
    UI_prevpass.set_previous_password_list(entry, connection)
    UI_prevpass.show()

    # Loop stays until close event.
    loop = QEventLoop()
    # By default, login is hidden on close()
    # This attribute makes it destroyed.
    UI_prevpass.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    UI_prevpass.destroyed.connect(loop.quit)
    loop.exec()
