from cryptoauthlib import (
        atcab_init,
        cfg_ateccx08a_i2c_default,
        atcab_info,
        get_device_name as actab_get_device_name,
        atcab_release,
        atcab_sign,
        atcab_read_serial_number,
        atcab_get_pubkey,
    )
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode
import json
import base64
import binascii

ATCA_SUCCESS = 0x00

def init():
    cfg = cfg_ateccx08a_i2c_default()
    cfg.cfg.atcai2c.bus = 1
    cfg.cfg.atcai2c.address = int("6a", 16)

    if atcab_init(cfg) != ATCA_SUCCESS:
        cfg.cfg.atcai2c.address = int("c0", 16)
        return atcab_init(cfg) == ATCA_SUCCESS
    return True

def release():
    return atcab_release() == ATCA_SUCCESS


def get_device_name():
    info = bytearray(4)
    atcab_info(info)
    return actab_get_device_name(info)

def get_serial_number():
    serial_number = bytearray(12)
    atcab_read_serial_number(serial_number)
    return serial_number

def public_key_2_pem(public_key: bytearray) -> str:
    der = bytearray.fromhex("3059301306072A8648CE3D020106082A8648CE3D03010703420004")
    public_key_b64 = base64.b64encode(der + public_key).decode("ascii")
    return public_key_b64

def get_public_key():
    public_key = bytearray(64)
    atcab_get_pubkey(0, public_key)

    return public_key


def get_signature(data_to_sign):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(str.encode(data_to_sign))
    message = digest.finalize()

    signature = bytearray(64)
    atcab_sign(0, message, signature)

    return signature

def base64_url_encode(data):
    return urlsafe_b64encode(data).rstrip(b"=")


def hexlify(data):
    return binascii.hexlify(data)


init()

print("Device Name:", get_device_name())
print("Device SN:", hexlify(get_serial_number()))
print("Device PubKey:", hexlify(get_public_key()))
# print("Signature:", hexlify(get_signature("Hello World")))
