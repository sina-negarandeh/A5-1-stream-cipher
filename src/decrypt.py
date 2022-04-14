import fnmatch
import os

import keystream_gen

BYTE = 8

def write_decrypted_file(file_name, decrypted_text):
    original_file_name, _ = os.path.splitext(file_name)
    _, file_extension = os.path.splitext(original_file_name)
    try:
        with open("output"+file_extension, "wb") as binary_file:
                for decrypted_bytes in decrypted_text:
                    binary_file.write(decrypted_bytes)
    except IOError:
        print(f"error: failed to write output{file_extension}")

def read_encrypted_file(file_name):
    try:
        encrypted_text = []
        with open(file_name, "rb") as file:
            while (byte := file.read(1)):
                encrypted_text.append(byte) 
            return encrypted_text
    except IOError:
            print(f"error: failed to read {file_name}")

def decrypt(file_name, stream_cipher):
    decrypted_text = []
    encrypted_text = read_encrypted_file(file_name)
    for encrypted_byte in encrypted_text:
        keystream = stream_cipher.generate_key_stream(BYTE)
        keystream_byte = str.encode(keystream)
        decrypted_text.append(bytes(a ^ b for a, b in zip(keystream_byte, encrypted_byte)))
    
    write_decrypted_file(file_name, decrypted_text)

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

def decrypt_file():
    stream_cipher = keystream_gen.A5_1()
    session_key = get_session_key()
    stream_cipher.initialize(session_key)
    
    for file_name in os.listdir('.'):
        if fnmatch.fnmatch(file_name, 'input.*.enc'):
            decrypt(file_name, stream_cipher)
            return
    raise Exception("error: failed to find the encrypted file")

if __name__ == "__main__":
    try:
        decrypt_file()
    except Exception as exception:
        print(exception)
