import fnmatch
import os

import keystream_gen

BYTE = 8

def write_encrypted_file(file_name, encrypted_text):
    try:
        with open(file_name+".enc", "wb") as binary_file:
                for encrypted_bytes in encrypted_text:
                    binary_file.write(encrypted_bytes)
    except IOError:
        print(f"error: failed to write {file_name}")

def read_plain_file(file_name):
    try:
        plain_text = []
        with open(file_name, "rb") as file:
            while (byte := file.read(1)):
                plain_text.append(byte) 
            return plain_text
    except IOError:
            print(f"error: failed to read {file_name}")

def encrypt(file_name, stream_cipher):
    encrypted_text = []
    plain_text = read_plain_file(file_name)
    for plain_byte in plain_text:
        keystream = stream_cipher.generate_key_stream(BYTE)
        keystream_byte = str.encode(keystream)
        encrypted_text.append(bytes(a ^ b for a, b in zip(keystream_byte, plain_byte)))
    
    write_encrypted_file(file_name, encrypted_text)

def get_session_key():
    try:
        # session key can be used as hard coded input
        # session_key = "0100111000101111010011010111110000011110101110001000101100111010"
        # return session_key

        # session key can be taken as input from the user through the command line
        session_key = input("Enter session key: ")
        return session_key

        # session key can be taken as input by reading from session_key.txt file
        # session_key_file_name = "session_key.txt"
        # with open(session_key_file_name, "r") as file:
        #     session_key = file.readline()
        #     return session_key
    except (KeyboardInterrupt, IOError):
            print("error: failed to get the session key")
            return ""

def encrypt_file():
    stream_cipher = keystream_gen.A5_1()
    session_key = get_session_key()
    stream_cipher.initialize(session_key)
    
    for file_name in os.listdir('.'):
        if fnmatch.fnmatch(file_name, 'input.*'):
            encrypt(file_name, stream_cipher)
            return
    raise Exception("error: failed to find the input file")

if __name__ == "__main__":
    try:
        encrypt_file()
    except Exception as exception:
        print(exception)
