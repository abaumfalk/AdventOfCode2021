import math
from pathlib import Path


class Packet:
    TYPE_SUM = 0
    TYPE_PRODUCT = 1
    TYPE_MINIMUM = 2
    TYPE_MAXIMUM = 3
    TYPE_LITERAL = 4
    TYPE_GREATER_THAN = 5
    TYPE_LESS_THAN = 6
    TYPE_EQUAL_TO = 7

    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id

        self.sub_packets = []
        self.value = None

    def type_id_to_str(self, type_id):
        return {
            self.TYPE_SUM: 'sum',
            self.TYPE_PRODUCT: 'product',
            self.TYPE_MINIMUM: 'minimum',
            self.TYPE_MAXIMUM: 'maximum',
            self.TYPE_LITERAL: 'literal',
            self.TYPE_GREATER_THAN: 'greater than',
            self.TYPE_LESS_THAN: 'less than',
            self.TYPE_EQUAL_TO: 'equal to',
        }[type_id]

    def __repr__(self):
        return f"{__class__} of type '{self.type_id_to_str(self.type_id)}'"

    def evaluate(self):
        if self.value is None:
            sub_packet_results = [p.evaluate() for p in self.sub_packets]

            if self.type_id == self.TYPE_SUM:
                self.value = sum(sub_packet_results)
            elif self.type_id == self.TYPE_PRODUCT:
                self.value = math.prod(sub_packet_results)
            elif self.type_id == self.TYPE_MINIMUM:
                self.value = min(sub_packet_results)
            elif self.type_id == self.TYPE_MAXIMUM:
                self.value = max(sub_packet_results)
            elif self.type_id == self.TYPE_GREATER_THAN:
                assert len(sub_packet_results) == 2, f"Expected 2 packets, found {len(sub_packet_results)}"
                self.value = 1 if sub_packet_results[0] > sub_packet_results[1] else 0
            elif self.type_id == self.TYPE_LESS_THAN:
                assert len(sub_packet_results) == 2, f"Expected 2 packets, found {len(sub_packet_results)}"
                self.value = 1 if sub_packet_results[0] < sub_packet_results[1] else 0
            elif self.type_id == self.TYPE_EQUAL_TO:
                assert len(sub_packet_results) == 2, f"Expected 2 packets, found {len(sub_packet_results)}"
                self.value = 1 if sub_packet_results[0] == sub_packet_results[1] else 0
            else:
                assert False, f"unknown type_id {self.type_id}"

        return self.value


class PacketDecoder:

    LENGTH_TYPE_BITS = 0
    LENGTH_TYPE_PACKETS = 1

    def __init__(self, hex_string):
        self.bits = format(int(hex_string, 16), f'0{len(hex_string) * 4}b')
        self.packets = []

        self.version_sum = 0

    @staticmethod
    def read_bits(bits, num):
        return bits[:num], bits[num:]

    def decode(self):
        self._decode(self.bits, self.packets)

    def _decode(self, bits, packets):
        while len(bits) > 8:
            bits = self.decode_packet(bits, packets)

        assert not bits or int(bits, 2) == 0

    def decode_packet(self, bits, packets):
        version, type_id, bits = self.decode_header(bits)
        packet = Packet(version, type_id)
        if type_id == Packet.TYPE_LITERAL:
            bits = self.decode_literal_packet(packet, bits)
        else:
            bits = self.decode_operator_packet(packet, bits)

        packets.append(packet)
        return bits

    def decode_literal_packet(self, packet, bits):
        packet.value, bits = self.get_literal(bits)
        return bits

    def decode_operator_packet(self, packet, bits):
        length_type_id, bits = self.read_bits(bits, 1)
        length_type_id = int(length_type_id, 2)

        if length_type_id == self.LENGTH_TYPE_BITS:
            length, bits = self.read_bits(bits, 15)
            length = int(length, 2)
            self._decode(bits[:length], packet.sub_packets)
            return bits[length:]

        if length_type_id == self.LENGTH_TYPE_PACKETS:
            packets, bits = self.read_bits(bits, 11)
            packets = int(packets, 2)
            for _ in range(packets):
                bits = self.decode_packet(bits, packet.sub_packets)
            return bits

        assert False, f"unexpected length type id {length_type_id}"

    def decode_header(self, bits):
        version, bits = self.read_bits(bits, 3)
        type_id, bits = self.read_bits(bits, 3)

        version = int(version, 2)
        type_id = int(type_id, 2)

        self.version_sum += version

        return version, type_id, bits

    def get_literal(self, bits):
        literal_str, bits = self._get_literal(bits)
        return int(literal_str, 2), bits

    def _get_literal(self, bits):
        cont, bits = self.read_bits(bits, 1)
        value, bits = self.read_bits(bits, 4)
        if cont == '1':
            next_value, bits = self._get_literal(bits)
            value += next_value

        return value, bits

    def get_version_sum(self):
        if not self.packets:
            self.decode()

        return self.version_sum

    def evaluate(self):
        if not self.packets:
            self.decode()

        return self.packets[0].evaluate()


if __name__ == "__main__":
    hex_string = Path('input').read_text().strip()
    packet_decoder = PacketDecoder(hex_string)
    packet_decoder.decode()

    print(f"sum of versions: {packet_decoder.get_version_sum()}")
    print(f"result: {packet_decoder.evaluate()}")
