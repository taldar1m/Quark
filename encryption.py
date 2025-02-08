from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from binascii import hexlify, unhexlify
import hashlib, secrets


def aes_decrypt(key, ciphertext):
    plaintext = AESGCM(key).decrypt(ciphertext[:12], ciphertext[12:], b'')
    return plaintext


def aes_encrypt(key, plaintext):
    nonce = secrets.token_bytes(12)
    ciphertext = nonce + AESGCM(key).encrypt(nonce, plaintext, b'')
    return ciphertext


def generate_sym_key():
    key = secrets.token_bytes(32)
    return key


def generate_private_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private_key


def get_public_key(private_key):
    public_key = private_key.public_key()
    return public_key


def import_private_key(path, passphrase: bytes):
    with open(path, 'rb') as pem_file:
        private_key = serialization.load_pem_private_key(pem_file.read(), password=passphrase)
    return private_key


def import_public_key(pem):
    public_key = serialization.load_pem_public_key(pem)
    return public_key


def export_private_key(private_key, passphrase: bytes):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase)
    )
    return pem


def export_public_key(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem


def encrypt(plaintext, public_key):
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


def hash(bin_data):
    shake256 = hashlib.shake_256()
    shake256.update(bin_data)
    return shake256.hexdigest(64).encode()