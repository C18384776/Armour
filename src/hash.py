import hashlib


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

    # Get hash of secret file if checkbox was enabled in registration/login.
    if checkbox:
        expert_file_hash = get_hash(secret_edit, None)

    # Get hash of password.
    password_edit_hash = get_hash(None, password_edit)

    # Combine password + secret file if selected, otherwise return password only.
    if expert_file_hash is None:
        return password_edit_hash
    else:
        combined_password = expert_file_hash + password_edit_hash
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

    # If text is None means that a file was passed instead of plaintext to be hashed.
    if text is None:
        with open(file_path, 'rb') as file:
            content = file.read()
            sha512.update(content)
            file.close()
    else:
        sha512.update(text.encode('utf-8'))

    return sha512.hexdigest()
