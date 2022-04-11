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


class LFSR:
    def __init__(self, size, clocking_bit, tapped_bits):
        self.size = size
        self.clocking_bit = clocking_bit
        self.tapped_bits = tapped_bits
        self.register = [0] * size
    
    def initialize(self, bits):
        if len(bits) == self.size:
            if isinstance(bits, str):
                self.register = list(map(int, list(bits)))

    def get_clocking_bit(self):
        return self.register[self.clocking_bit]

    def get_feedback(self):
        feedback = self.register[self.tapped_bits[0]]
        for tapped_bit in self.tapped_bits[1:]:
            feedback = feedback ^ self.register[tapped_bit]
        return feedback

    def shift(self, majority_bit):
        output = self.register[-1]
        if self.register[self.clocking_bit] == majority_bit:
            feedback = self.get_feedback()
            self.register.pop(-1)
            self.register.insert(0, feedback)
        return output
