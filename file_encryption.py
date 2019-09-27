#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
AES加密解密工具类
"""
import sys
from Crypto.Cipher import AES

def padding(origin_data):
    bs = AES.block_size  # 16
    length = len(origin_data)
    padding_size = length
    padding = bs - padding_size % bs
    print(padding_size)
    padding_data = bytes(chr(padding), encoding="ASCII") * padding
    return origin_data + padding_data

def unpadding(origin_data):
    padding_size = origin_data[-1]
    return origin_data[:-padding_size]

def myencript(key, data):
    key_bytes = key.encode()
    key_bytes = key_bytes + (16 - len(key_bytes)) * b'\0'
    iv = bytes(reversed(key_bytes))
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    # 处理明文
    data_padding = padding(data)
    # 加密
    encrypt_bytes = cipher.encrypt(data_padding)
    return encrypt_bytes

def mydecript(key, data):
    key_bytes = key.encode()
    key_bytes = key_bytes + (16 - len(key_bytes)) * b'\0'
    iv = bytes(reversed(key_bytes))
    
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)

    decrypt_bytes = cipher.decrypt(data)

    result = unpadding(decrypt_bytes)
    return result

def main():
    op = sys.argv[1]
    key = sys.argv[2]
    file_path = sys.argv[3]

    with open(file_path, "rb") as f:
        if op == "-e":
            encrypted_data = myencript(key, f.read())
            dst_file_path = file_path + ".wh"
        elif op == "-d":
            encrypted_data = mydecript(key, f.read())

            if file_path[-3:] == ".wh":
                dst_file_path = file_path[0:-3]
            else:
                dst_file_path = file_path + ".wh"
    
    with open(dst_file_path, "wb") as f:
        f.write(encrypted_data)


if __name__ == "__main__":
    main()