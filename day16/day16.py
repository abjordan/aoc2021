#!/usr/bin/env python3

from enum import Enum
from functools import reduce
from operator import mul
import sys

bits_from_hex = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

class PktType(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATERTHAN = 5
    LESSTHAN = 6
    EQUAL = 7

class Packet:
    def __init__(self, version, pkt_type):
        self.literal = None
        self.sub_pkts = []
        self.bit_count = 6
        self.version = version
        self.kind = PktType(pkt_type)

    def __str__(self) -> str:
        ret = f'VER:{self.version} KIND:{self.kind}'
        if self.literal is None:
            ret += f' SUBPKT:{len(self.sub_pkts)}'
        else:
            ret += f' LITERAL:{self.literal}'
        return ret

    def pretty(self, depth=0):
        ret = f'ver:{self.version}  kind:{self.kind}  size:{self.bit_count}'
        if len(self.sub_pkts) != 0:
            for subp in self.sub_pkts:
                ret += '\n' + '\t'*(depth+1) + subp.pretty(depth+1)
        else:
            ret += f'  literal:{self.literal}'
        return ret

    def version_sum(self):
        return self.version + sum([x.version_sum() for x in self.sub_pkts])

    def evaluate(self):
        if self.kind == PktType.LITERAL:
            return self.literal
        elif self.kind == PktType.SUM:
            return sum([x.evaluate() for x in self.sub_pkts])
        elif self.kind == PktType.PRODUCT:
            return reduce(mul, [x.evaluate() for x in self.sub_pkts], 1)
        elif self.kind == PktType.MINIMUM:
            return min([x.evaluate() for x in self.sub_pkts])
        elif self.kind == PktType.MAXIMUM:
            return max([x.evaluate() for x in self.sub_pkts])
        elif self.kind == PktType.GREATERTHAN:
            return 1 if self.sub_pkts[0].evaluate() > self.sub_pkts[1].evaluate() else 0
        elif self.kind == PktType.LESSTHAN:
            return 1 if self.sub_pkts[0].evaluate() < self.sub_pkts[1].evaluate() else 0
        elif self.kind == PktType.EQUAL:
            return 1 if self.sub_pkts[0].evaluate() == self.sub_pkts[1].evaluate() else 0
        else:
            raise RuntimeError("Invalid operator: " + str(self.kind))

def read_int(raw_bits, bit_len):
    num = int(raw_bits[0:bit_len], 2)
    rest = raw_bits[bit_len:]
    return num, rest

def read_literal(raw_bits):
    # Read 5 bits at a time: first bit is "non-terminal", 1-5 are the value
    offset = 0
    value_bits = ''
    more = raw_bits[offset]
    while more != '0':
        value_bits += raw_bits[offset+1:offset+5]
        offset += 5
        more = raw_bits[offset]
    value_bits += raw_bits[offset+1:offset+5]
    value = int(value_bits, 2)
    return value, offset+5, raw_bits[offset+5:]

def read_packet(raw_bits):
    version, raw_bits = read_int(raw_bits, 3)
    pkt_type, raw_bits = read_int(raw_bits, 3)

    pkt = Packet(version, pkt_type)

    #print(f'Version {version}')
    #print(f'Type    {pkt_type}')

    if pkt.kind == PktType.LITERAL:
        # Literal Value Packet
        literal, bits_read, raw_bits = read_literal(raw_bits)
        pkt.literal = literal
        pkt.bit_count += bits_read
    else:
        # Operator Packet
        pkt.length_type, raw_bits = read_int(raw_bits, 1)
        pkt.bit_count += 1
        if pkt.length_type == 0:
            # Total Length Type (15 bits)
            #print('Total Length Type')
            total_len, raw_bits = read_int(raw_bits, 15)
            pkt.bit_count += 15

            sub_pkt_bits = 0
            while sub_pkt_bits < total_len:
                sub_pkt, raw_bits = read_packet(raw_bits)
                pkt.sub_pkts.append(sub_pkt)
            
                pkt.bit_count += sub_pkt.bit_count
                sub_pkt_bits += sub_pkt.bit_count
                #print(f'{sub_pkt_bits} / {total_len}')
            #print(f'Found {len(pkt.sub_pkts)} sub-packets; size {sub_pkt_bits}')
        else:
            #print('Packet Count Type')
            num_sub_pkts, raw_bits = read_int(raw_bits, 11)
            pkt.bit_count += 11
            for i in range(0, num_sub_pkts):
                sub_pkt, raw_bits = read_packet(raw_bits)
                pkt.sub_pkts.append(sub_pkt)
                pkt.bit_count += sub_pkt.bit_count

    return pkt, raw_bits


if __name__=='__main__':
    hex_data = [x.strip() for x in open(sys.argv[1], 'r').readlines()]

    # Reverse it so we can use pop without having to import deque
    hex_data = list(reversed(hex_data))

    line = hex_data.pop()
    while line != '':
        if line.startswith('#'):
            continue
        
        print(line)
        offset = 0
        raw_bits = ''
        for ch in line:
            try:
                raw_bits += bits_from_hex[ch]
                offset += 1
            except KeyError as ke:
                print(f'BAD CHAR AT {offset}: {ch}')

        # print('0b' + raw_bits)
        pkt, raw_bits = read_packet(raw_bits)
        #print(pkt.pretty())
        version_sum = pkt.version_sum()
        print(f'    Version sum: {version_sum}')
        result = pkt.evaluate()
        print(f'    Packet evaluation result: {result}')

        if len(hex_data) == 0:
            break
        line = hex_data.pop()