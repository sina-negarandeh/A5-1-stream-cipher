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


class A5_1:
    _19_bits_register_size = 19
    _22_bits_register_size = 22
    _23_bits_register_size = 23

    _19_bits_register_clocking_bit = 8
    _22_bits_register_clocking_bit = 10
    _23_bits_register_clocking_bit = 10

    _19_bits_register_tapped_bits = [18, 17, 16, 13]
    _22_bits_register_tapped_bits = [21, 20]
    _23_bits_register_tapped_bits = [22, 21, 20, 7]

    def __init__(self):
        self._19_bits_register = LFSR(self._19_bits_register_size, self._19_bits_register_clocking_bit, self._19_bits_register_tapped_bits)
        self._22_bits_register = LFSR(self._22_bits_register_size, self._22_bits_register_clocking_bit, self._22_bits_register_tapped_bits)
        self._23_bits_register = LFSR(self._23_bits_register_size, self._23_bits_register_clocking_bit, self._23_bits_register_tapped_bits)
    
    def initialize_registers(self, session_key):
        self._19_bits_register.initialize(session_key[0:19])
        self._22_bits_register.initialize(session_key[19:41])
        self._23_bits_register.initialize(session_key[41:64])
    
    def cal_majority_bit(self):
        sum = 0
        sum += self._19_bits_register.get_clocking_bit()
        sum += self._22_bits_register.get_clocking_bit()
        sum += self._23_bits_register.get_clocking_bit()

        if sum > 1:
            return 1
        else:
            return 0
    
    def clock(self):
        output = 0
        majority_bit = self.cal_majority_bit()

        output = output ^ self._19_bits_register.shift(majority_bit)
        output = output ^ self._22_bits_register.shift(majority_bit)
        output = output ^ self._23_bits_register.shift(majority_bit)

        return output

    def initialize(self, session_key):
        Validator.validate_session_key(session_key)
        self.initialize_registers(session_key)

    def generate_key_stream(self, text_length):
        key_stream = ""        

        for _ in range(text_length):
            key_stream += str(self.clock())
        return key_stream
