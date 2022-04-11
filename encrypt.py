import fnmatch
import os

import keystream_gen

def write_encrypted_file(file_name, encrypted_text):
    with open(file_name+".enc", "wb") as binary_file:
            for encrypted_bytes in encrypted_text:
                binary_file.write(encrypted_bytes)

def read_plain_file(file_name):
    try:
        plain_text = []
        with open(file_name, "rb") as file:
            while (byte := file.read(1)):
                plain_text.append(byte) 
            return plain_text
    except IOError:
            print('Error While Opening the file!')

def encrypt(file_name, stream_cipher):
    encrypted_text = []
    plain_text = read_plain_file(file_name)
    for plain_byte in plain_text:
        keystream = stream_cipher.generate_key_stream(8)
        keystream_as_bytes = str.encode(keystream)
        encrypted_text.append(bytes(a ^ b for a, b in zip(keystream_as_bytes, plain_byte)))
    
    write_encrypted_file(file_name, encrypted_text)

def encrypt_file():
    stream_cipher = keystream_gen.A5_1()
    session_key = "0100111000101111010011010111110000011110101110001000101100111010"
    stream_cipher.initialize(session_key)
    
    for file_name in os.listdir('.'):
        if fnmatch.fnmatch(file_name, 'input.*'):
            encrypt(file_name, stream_cipher)

if __name__ == "__main__":
    encrypt_file()
