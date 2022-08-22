from coincurve import PublicKey
from Crypto.Hash import keccak
from secrets import token_bytes


def generate_random_address():
    random_private_key = keccak.new(data=token_bytes(32), digest_bits=256).digest()

    random_public_key = PublicKey.from_valid_secret(random_private_key).format(compressed=False)[1:]

    random_address_data = keccak.new(data=random_public_key, digest_bits=256).digest()[-20:]

    random_address = '0x' + random_address_data.hex()

    print('Random address created ' + random_address)

    return random_address
