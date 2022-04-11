ALLOWED_CHARACTERS = {'0', '1'}
SESSION_KEY_LENGHT = 64

class Validator:
    @staticmethod
    def validate_session_key_characters(session_key):
        session_key_characters = set(session_key)
        if session_key_characters != ALLOWED_CHARACTERS:
            raise Exception("session key should be made up of characters 0 and 1")

    @staticmethod
    def validate_session_key_size(session_key):
        if len(session_key) != SESSION_KEY_LENGHT:
            raise Exception("session key should be 64 bits")

    @staticmethod
    def validate_session_key(session_key):
        Validator.validate_session_key_size(session_key)
        Validator.validate_session_key_characters(session_key)
