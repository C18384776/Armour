from src import hash


def test_hash_password():
    """
    Test that program password hashing works correctly.
    """
    SHA512_hash = "d9f62fd5dd33d3233075f2cd15584e4a7ad1e6ca5322f619d9aae7e6255465d6" \
                  "1ff9f1aa9f0ef69c8d0c235017857beb156c9fff86eefd3c3d7706e5e5ec1b71"
    computed_hash = hash.get_hash(None, "password_that_will_get_hashed")
    assert SHA512_hash == computed_hash


def test_hash_file():
    """
    Test that program file hashing works correctly.
    """
    SHA512_hash = "30ddb97e11a9c6db24c550f3e447798fa243bbe6bb8e471f38fde87381f21def" \
                  "b105408b1073e26af02cee3001c93c67bbd487017c967dee9dbecfc3f8c0a839"
    computed_hash = hash.get_hash("DONOTTOUCH", None)
    assert SHA512_hash == computed_hash


def test_master_password_just_pass():
    """
    Test that master password hashes correctly without secret file.
    """
    SHA512_hash = "d9f62fd5dd33d3233075f2cd15584e4a7ad1e6ca5322f619d9aae7e6255465d6" \
                  "1ff9f1aa9f0ef69c8d0c235017857beb156c9fff86eefd3c3d7706e5e5ec1b71"
    computed_hash = hash.password_hash_collection(None, None, "password_that_will_get_hashed")
    assert SHA512_hash == computed_hash


def test_master_password_combined():
    """
    Test that master password hashes correctly with secret file.
    """
    SHA512_pass_hash = "d9f62fd5dd33d3233075f2cd15584e4a7ad1e6ca5322f619d9aae7e6255465d6" \
                       "1ff9f1aa9f0ef69c8d0c235017857beb156c9fff86eefd3c3d7706e5e5ec1b71"
    SHA512_file_hash = "30ddb97e11a9c6db24c550f3e447798fa243bbe6bb8e471f38fde87381f21def" \
                       "b105408b1073e26af02cee3001c93c67bbd487017c967dee9dbecfc3f8c0a839"
    SHA512_combined = SHA512_file_hash + SHA512_pass_hash
    computed_hash = hash.password_hash_collection(True, "DONOTTOUCH", "password_that_will_get_hashed")
    assert SHA512_combined == computed_hash
