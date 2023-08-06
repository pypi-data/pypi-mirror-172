import json
import symbolhkdf
import time
import binascii
import base64
import hashlib

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

def publicKey_to_addr(publicKey, networkType = 152):
    if len(publicKey)!= 64:
        raise ValueError("Invalid publicKey")
    part_one_hash_builder = hashlib.sha3_256()
    part_one_hash_builder.update(binascii.unhexlify(publicKey))
    part_one_hash = part_one_hash_builder.digest()

    part_two_hash_builder = hashlib.new('ripemd160')
    part_two_hash_builder.update(part_one_hash)
    part_two_hash = part_two_hash_builder.digest()

    version = bytes([networkType]) + part_two_hash

    part_three_hash_builder = hashlib.sha3_256()
    part_three_hash_builder.update(version)
    checksum = part_three_hash_builder.digest()[0:3]
    address_encode = base64.b32encode(version+checksum).decode('utf-8')[:-1]
    return address_encode

def recover_to_addr(payload):
    sender_publickey = payload[:64]
    encrypted_message = payload[64:]
    decode = json.loads(symbolhkdf.decode(settings.SERVER_SECRET, sender_publickey, encrypted_message))#復号
    print("addr:", publicKey_to_addr(sender_publickey,settings.NETWORK_TYPE))
    iat = decode["iat"] 
    signer = decode["signerAddress"]
    verifier = decode["verifierAddress"]
    if verifier != settings.OWNER:
        raise ValueError("Invalid verifier")
    if time.time()*1000 - int(iat) - settings.EXPIRATION_DATE > 0:
        raise ValueError("iat expired")
    return signer


def validate_xym_address(value):# サインアップ時のアドレス検証
    if not len(value) == 39:
        raise forms.ValidationError(
            _('%(value)s is not a valid Symbol address'),
            params={'value': value},
        )
    decode = base64.b32decode(value+"=")
    checksum = decode[21:]
    hasher = hashlib.sha3_256()
    calculate_chk = hasher.update(decode[:21])
    calculate_chk = hasher.digest()[:len(checksum)]
    print("decode:",decode,"chk:",checksum,"calc:",calculate_chk)
    if checksum != calculate_chk:
        raise forms.ValidationError(
            _('%(value)s is not a valid Symbol address'),
            params={'value': value},
        )

