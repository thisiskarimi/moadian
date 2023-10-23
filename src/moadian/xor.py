import binascii
import json


class XOR:
    def do_xor(self, b1, b2):
        b1 = self.to_bytes(b1)
        b2 = self.to_bytes(b2)
        one_and_two = self.xor_blocks(b1, b2) if len(
            b1) < len(b2) else self.xor_blocks(b2, b1)
        length = len(one_and_two)
        while length > 0 and one_and_two[length - 1] == 0:
            length -= 1
        if length < len(one_and_two):
            return bytes(one_and_two[:length])
        return bytes(one_and_two)

    @staticmethod
    def to_bytes(data):
        if isinstance(data, dict):
            data = json.dumps(data).encode()
        elif isinstance(data, int):
            data = data.to_bytes((data.bit_length() + 7) // 8, "big")
        elif isinstance(data, str):
            data = data.encode()
        elif isinstance(data, bytearray):
            data = bytes(data)
        elif not isinstance(data, bytes):
            raise TypeError(
                "Invalid data type. Supported types are hex, bytes, bytearray, and string.")
        return data

    @staticmethod
    def xor_blocks(smaller_array, bigger_array):
        one_and_two = bytearray(bigger_array)
        block_size = (len(bigger_array) + len(smaller_array) -
                      1) // len(smaller_array)
        for i in range(block_size):
            for j in range(len(smaller_array)):
                if (i * len(smaller_array)) + j >= len(bigger_array):
                    break
                one_and_two[(i * len(smaller_array)) + j] = (
                    smaller_array[j] ^ bigger_array[(
                        i * len(smaller_array)) + j]
                )
        return bytes(one_and_two)

    @staticmethod
    def to_hex(data):
        return binascii.hexlify(data).decode()
