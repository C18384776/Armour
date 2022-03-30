from src import hash


def test_hash_password():
    SHA512_hash = "d9f62fd5dd33d3233075f2cd15584e4a7ad1e6ca5322f619d9aae7e6255465d6" \
                  "1ff9f1aa9f0ef69c8d0c235017857beb156c9fff86eefd3c3d7706e5e5ec1b71"
    computed_hash = hash.get_hash(None, "password_that_will_get_hashed")
    assert SHA512_hash == computed_hash

def test_hash_file():
    pass