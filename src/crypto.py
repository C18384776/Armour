import io
import pyAesCrypt
import hash
import database
import warn


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

                sql_create_group_table = """
                                        CREATE TABLE IF NOT EXISTS groups (
                                            groupId integer PRIMARY KEY,
                                            groupName text NOT NULL);"""

                sql_create_password_table = """
                                        CREATE TABLE IF NOT EXISTS passwords (
                                            passwordId integer PRIMARY KEY,
                                            passwordName text,
                                            passwordPassword NOT NULL,
                                            groupId integer NOT NULL,
                                            FOREIGN KEY (groupId) REFERENCES groups(groupId));"""

                connection = database.make_connection(database_save_path)
                print("connection made? {}".format(connection))

                if connection is not None:
                    database.database_query(connection, sql_create_group_table)
                    database.database_query(connection, sql_create_password_table)
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
