import io
import math
import pyAesCrypt
from zxcvbn import zxcvbn
import hash
import database
import warn
import datetime


def sign_up(check_fields, password_bits, directory_edit, expert_checkbox, secret_edit, password_edit, Registration):
    """
    Create database file.
    There are three tables: 1. groups; 2. passwords; 3. previous_passwords.
    Also provides database with sample inserts into tables.

    :param check_fields:
    Boolean check if required fields are complete.

    :param password_bits:
    Password bits value.

    :param directory_edit:
    Location of save directory.

    :param expert_checkbox:
    Boolean check if expert checkbox activated.

    :param secret_edit:
    Location of secret file given by user to encrypt with.

    :param password_edit:
    Password given by user to encrypt with.
    """
    # Registration begins once all required fields are entered.
    if not check_fields:

        # Show warning if weak password.
        if password_bits < 100:
            response_to_password_warning = warn.password_warning_message()

            # Exit function if user does not want to continue with a weak password.
            if response_to_password_warning == 'No':
                return 1

        # Where database will be saved on PC.
        database_save_path = directory_edit.text()
        database_save_path = database_save_path + "/Password.db"

        # Database table creates.
        sql_create_group_table = """
                                CREATE TABLE IF NOT EXISTS groups (
                                    groupId INTEGER PRIMARY KEY,
                                    groupName text NOT NULL);"""

        sql_create_password_table = """
                                CREATE TABLE IF NOT EXISTS passwords (
                                    passwordId INTEGER PRIMARY KEY,
                                    passwordWebsite text,
                                    passwordName text,
                                    passwordPassword text NOT NULL,
                                    passwordUrl text,
                                    passwordCreation timestamp,
                                    password2FA text,
                                    groupId integer NOT NULL,
                                    FOREIGN KEY (groupId) REFERENCES groups(groupId));"""

        sql_create_previous_password_table = """
                                CREATE TABLE IF NOT EXISTS previous_passwords (
                                    prevPasswordId INTEGER PRIMARY KEY,
                                    prevPassword text NOT NULL,
                                    prevPasswordCreation timestamp,
                                    passwordId integer NOT NULL,
                                    FOREIGN KEY (passwordId) REFERENCES groups(passwordId));"""

        # Database inserts.
        sql_group_insert = """INSERT INTO groups(groupName) VALUES(?)"""

        sql_entry_insert = """INSERT INTO passwords(passwordWebsite,
        passwordName, passwordPassword, passwordUrl,
        passwordCreation, password2FA, groupId) VALUES(?,?,?,?,?,?,?)"""

        sql_prev_pass_insert = """INSERT INTO previous_passwords(prevPassword,
        prevPasswordCreation, passwordId) VALUES(?,?,?)"""

        # Create database connection.
        connection = database.make_connection(database_save_path)

        # If connection is make.
        if connection is not None:
            # Database sample insert values.
            group_name_sm = ['Social Media']
            group_name_bank = ['Bank']
            group_name_school = ['School']
            group_name_other = ['Other']
            group_name_bin = ['Recycle Bin']

            pass_entry_one = ['Facebook', 'Declan', 'password1',
                              'www.facebook.com', datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                              'JBSWY3DPEHPK3PXP', 1]

            pass_entry_two = ['Twitter', 'Declan', 'password2',
                              'www.twitter.com', datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                              'JBSWY3DPEHPK3PXP', 1]

            pass_entry_three = ['AIB', 'Declan', 'password3',
                                'www.aib.ie', datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                                'JBSWY3DPEHPK3PXP', 2]

            prev_pass_entry_one = ['previouspassword123',
                                   datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                                   2]

            prev_pass_entry_two = ['previouspassword456',
                                   datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                                   3]

            # Query to create SQL tables.
            database.database_query(connection, sql_create_group_table, None)
            database.database_query(connection, sql_create_password_table, None)
            database.database_query(connection, sql_create_previous_password_table, None)

            # Sample database inserts into groups table.
            database.database_query(connection, sql_group_insert, group_name_sm)
            database.database_query(connection, sql_group_insert, group_name_bank)
            database.database_query(connection, sql_group_insert, group_name_school)
            database.database_query(connection, sql_group_insert, group_name_other)
            database.database_query(connection, sql_group_insert, group_name_bin)

            # Sample database inserts into passwords table.
            database.database_query(connection, sql_entry_insert, pass_entry_one)
            database.database_query(connection, sql_entry_insert, pass_entry_two)
            database.database_query(connection, sql_entry_insert, pass_entry_three)

            # Sample database inserts into previous_passwords table.
            database.database_query(connection, sql_prev_pass_insert, prev_pass_entry_one)
            database.database_query(connection, sql_prev_pass_insert, prev_pass_entry_two)

            # Commit changes to database.
            connection.commit()

            # Close database.
            connection.close()

            # Start preparation to encrypt database by hashing password (and file if available).
            password = hash.password_hash_collection(expert_checkbox,
                                                     secret_edit.text(),
                                                     password_edit.text())

            # Encrypt database with hashed password value from above.
            database_encryption(password, database_save_path)

            Registration.close()
        else:
            print("Problem making database?")


def database_encryption(password, database_save_path):
    """
    Encrypts database file.

    :param password:
    Password that will encrypt database file.

    :param database_save_path:
    File to be encrypted.
    """
    buffer_size = 64 * 1024

    try:
        with open(database_save_path, 'rb') as file:

            # Read initial unencrypted database and copy its contents to a variable.
            content = file.read()

            # Input plaintext binary stream
            plaintext = io.BytesIO(content)

            # Initialize ciphertext binary stream
            cipher = io.BytesIO()

            # Encrypt stream
            pyAesCrypt.encryptStream(plaintext, cipher, password, buffer_size)

            file.close()

        # Overwrite database file with encryption.
        with open(database_save_path, 'wb') as file:

            file.write(cipher.getvalue())
            file.close()
    except:
        print("Error occurred in method database_encryption")


def login(check_fields, expert_checkbox, secret_edit, password_edit, directory_edit):
    """
    Opens the database file by decrypting it.

    :param check_fields:
    Boolean check if required fields are complete.

    :param expert_checkbox:
    Boolean check if expert checkbox activated.

    :param secret_edit:
    Location of secret file given by user to encrypt with.

    :param password_edit:
    Password given by user to encrypt with.

    :param directory_edit:
    Location of database file.

    :return:
    Master password and decrypted data.
    """

    # Login begins once all required fields are entered.
    if not check_fields:
        # Start preparation to decrypt database by hashing password (and file if available).
        password = hash.password_hash_collection(expert_checkbox,
                                                 secret_edit.text(),
                                                 password_edit.text())

        # Where database will be saved on PC.
        database_path = directory_edit.text()

        buffer_size = 64 * 1024
        try:
            with open(database_path, 'rb') as file:
                # Read contents of encrypted database.
                cipher = io.BytesIO(file.read())

                # Initialize decrypted binary stream
                decrypted = io.BytesIO()

                # Get ciphertext length
                ciphertext_length = len(cipher.getvalue())

                # Go back to the start of the ciphertext stream
                cipher.seek(0)

                # Decrypt stream
                pyAesCrypt.decryptStream(cipher, decrypted, password, buffer_size, ciphertext_length)

                return password, decrypted.getvalue()
        except:
            print("Wrong password?")


def update_password_bits(password_edit, password_bits_value, strength_progress_bar, password_warning):
    """
    Update bits on progress bar.

    :param password_edit:
    Password given by user.

    :param password_bits_value:
    Password bits value.

    :param strength_progress_bar:
    QProgressBar.

    :param password_warning:
    Trigger to display/hide password warning.

    """

    # Entropy is calculated when text field is not empty.
    if password_edit.text():
        # Generate bits entropy from password given by user.
        result = zxcvbn(password_edit.text())
        password_bits_value = math.log2(result["guesses"]).__floor__()
        strength_progress_bar.setValue(password_bits_value)

        # Hides password warning if a password is typed.
        try:
            if password_edit.text():
                password_warning.hide()
        except AttributeError:
            pass
    # If password value given by user is empty.
    elif password_edit.text() == '':
        strength_progress_bar.setValue(0)

        # User is warned that password cannot be blank.
        try:
            password_warning.show()
        except AttributeError:
            pass
