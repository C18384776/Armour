import hashlib


# Repurpose password_edit to overwrite password.
def password_hash_collection(checkbox, secret_edit, password_edit):
    """
    Hash password from password field & secret file (if selected).

    :param checkbox:
    Checkbox checked? True/False

    :param secret_edit:
    Path of the secret file.

    :param password_edit:
    Password entered by user.

    :return:
    Combined SHA512 hashes or password hash alone if checkbox is not selected.
    """
    expert_file_hash = None
    if checkbox:
        print(secret_edit)
        expert_file_hash = get_hash(secret_edit, None)

    password_edit_hash = get_hash(None, password_edit)

    if expert_file_hash is None:
        print("password edit hash" + str(password_edit_hash))
        return password_edit_hash
    else:
        combined_password = expert_file_hash + password_edit_hash
        print("combined pass" + str(combined_password))
        return combined_password


def get_hash(file_path, text):
    """
    Compute the SHA512 hash of a file or text.

    :param file_path:
    The path of a file.

    :param text:
    Text to be hashed.

    :return:
    SHA512 hash of a file.
    """
    sha512 = hashlib.sha512()

    if text is None:
        with open(file_path, 'rb') as file:
            content = file.read()
            sha512.update(content)
            print('SHA512 of secret file:{}'.format(sha512.hexdigest()))
            file.close()
    else:
        sha512.update(text.encode('utf-8'))
        print("SHA512 of: {} : is {}".format(text, sha512.hexdigest()))

    return sha512.hexdigest()
