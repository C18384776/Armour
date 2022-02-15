import io
import pyAesCrypt
import hash
import database
import warn
import datetime

def sign_up(check_fields, password_bits, directory_edit, expert_checkbox, secret_edit, password_edit):
    # Function checks if fields are entered.
    # True = All needed fields are non-blank.
    # False = One or more fields are blank.
    # fields_filled = check_fields

    # Begin database registration once fields are non-blank.
    if not check_fields:
        # Show a warning if given password that is deemed weak.
        if password_bits < 100:
            response_to_password_warning = warn.password_warning_message()
            # If users password was weak and they decided to change it from the warning.
            if response_to_password_warning == "No":
                print("said no")
                return 1
            else:
                database_save_path = directory_edit.text()
                database_save_path = database_save_path + "/Password.db"
                print(database_save_path)

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

                sql_group_insert = """INSERT INTO groups(groupName) VALUES(?)"""

                sql_entry_insert = """INSERT INTO passwords( passwordWebsite, 
                passwordName, passwordPassword, passwordUrl, 
                passwordCreation, password2FA, groupId) VALUES(?,?,?,?,?,?,?)"""

                connection = database.make_connection(database_save_path)
                print("connection made? {}".format(connection))

                if connection is not None:
                    group_name_sm = ['Social Media']
                    group_name_bank = ['Bank']
                    group_name_school = ['School']
                    group_name_other = ['Other']
                    group_name_bin = ['Recycle Bin']

                    pass_entry_one = ['Facebook', 'Declan', 'password1',
                                      'www.facebook.com', datetime.datetime.now(),
                                      '123456', 1]

                    pass_entry_two = ['Twitter', 'Declan', 'password2',
                                      'www.twitter.com', datetime.datetime.now(),
                                      '123456', 1]

                    pass_entry_three = ['AIB', 'Declan', 'password3',
                                      'www.aib.ie', datetime.datetime.now(),
                                      '123456', 2]

                    database.database_query(connection, sql_create_group_table, None)
                    database.database_query(connection, sql_create_password_table, None)
                    database.database_query(connection, sql_group_insert, group_name_sm)
                    database.database_query(connection, sql_group_insert, group_name_bank)
                    database.database_query(connection, sql_group_insert, group_name_school)
                    database.database_query(connection, sql_group_insert, group_name_other)
                    database.database_query(connection, sql_group_insert, group_name_bin)
                    database.database_query(connection, sql_entry_insert, pass_entry_one)
                    database.database_query(connection, sql_entry_insert, pass_entry_two)
                    database.database_query(connection, sql_entry_insert, pass_entry_three)

                    connection.commit()
                    connection.close()
                    print("Database created.")

                    # Start preparation to encrypt database.
                    password = hash.password_hash_collection(expert_checkbox,
                                                             secret_edit.text(),
                                                             password_edit.text())

                    database_encryption(password, database_save_path)

                    print("Database encrypted")
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
            content = file.read()
            # Input plaintext binary stream
            plaintext = io.BytesIO(content)
            # Initialize ciphertext binary stream
            cipher = io.BytesIO()
            # encrypt stream
            pyAesCrypt.encryptStream(plaintext, cipher, password, buffer_size)
            # print encrypted data
            print("This is the ciphertext:\n" + str(cipher.getvalue()))
            file.close()

        # Writing encryption
        with open(database_save_path, 'wb') as file:
            file.write(cipher.getvalue())
            file.close()
    except:
        print("Error occurred in method database_encryption")


def login(check_fields, expert_checkbox, secret_edit, password_edit, directory_edit):
    # Function checks if fields are entered.
    # True = All needed fields are non-blank.
    # False = One or more fields are blank.
    if not check_fields:
        password = hash.password_hash_collection(expert_checkbox,
                                                 secret_edit.text(),
                                                 password_edit.text())

        database_path = directory_edit.text()

        buffer_size = 64 * 1024
        try:
            with open(database_path, 'rb') as file:
                cipher = io.BytesIO(file.read())
                # initialize decrypted binary stream
                decrypted = io.BytesIO()
                # get ciphertext length
                ciphertext_length = len(cipher.getvalue())
                # go back to the start of the ciphertext stream
                cipher.seek(0)
                # decrypt stream
                pyAesCrypt.decryptStream(cipher, decrypted, password, buffer_size, ciphertext_length)
                # print decrypted data
                print("Decrypted data:\n" + str(decrypted.getvalue()))
                return password, decrypted.getvalue()
        except:
            print("Wrong password?")
