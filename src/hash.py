import hashlib


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
