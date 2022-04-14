import fnmatch
import os

import keystream_gen

def write_decrypted_file(file_name, decrypted_text):
    original_file_name, _ = os.path.splitext(file_name)
    _, file_extension = os.path.splitext(original_file_name)
    with open("output"+file_extension, "wb") as binary_file:
            for decrypted_bytes in decrypted_text:
                binary_file.write(decrypted_bytes)

def read_plain_file(file_name):
    try:
        plain_text = []
        with open(file_name, "rb") as file:
            while (byte := file.read(1)):
                plain_text.append(byte) 
            return plain_text
    except IOError:
            print("error: file could not be opened")

def decrypt(file_name, stream_cipher):
    decrypted_text = []
    plain_text = read_plain_file(file_name)
    for plain_byte in plain_text:
        keystream = stream_cipher.generate_key_stream(8)
        keystream_as_bytes = str.encode(keystream)
        decrypted_text.append(bytes(a ^ b for a, b in zip(keystream_as_bytes, plain_byte)))
    
    write_decrypted_file(file_name, decrypted_text)

def decrypt_file():
    stream_cipher = keystream_gen.A5_1()
    session_key = "0100111000101111010011010111110000011110101110001000101100111010"
    stream_cipher.initialize(session_key)
    
    for file_name in os.listdir('.'):
        if fnmatch.fnmatch(file_name, 'input.*.enc'):
            decrypt(file_name, stream_cipher)

if __name__ == "__main__":
    try:
        decrypt_file()
    except Exception as exception:
        print(exception)
