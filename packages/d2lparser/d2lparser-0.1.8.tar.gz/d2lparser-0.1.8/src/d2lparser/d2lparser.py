import json
from enum import Enum
from os import error
from typing import Any
from bitstring import ConstBitStream, ReadError

from .encryption import decrypt

OFFSET_ENCRYPTED = 16
OFFSET_PAYLOAD = 38

##
#  Enumerations
##


class TypePayload(Enum):
    GET_FIRMWARE = 1
    PUSH_JSON = 3
    GET_HORLOGE = 5

##
 #  Classes
 ##


class Packet:
    def __init__(self) -> None:
        self.header = {}
        self.payload = {}

    def set_header_value(self, key, value):
        self.header[key] = value

    def get_header_value(self, key):
        return self.header[key]

    def get_payload_size(self):
        return self.header["taillePayload"]


class D2LParser:
    last_packet = None
    prev_packet = None

    def __init__(self, d2l_key: str, d2l_iv: str) -> None:
        self.d2l_key = bytes.fromhex(d2l_key)
        self.d2l_iv = bytes.fromhex(d2l_iv)

    def get_last_packet(self) -> Packet:
        return self.last_packet

    def get_previous_packet(self) -> Packet:
        return self.prev_packet

    def parse_request(self, msg_encrypted: bytes) -> Packet:
        '''
        Return a Packet which contains a header and payload dict with all data
        '''
        self.prev_packet = self.last_packet
        self.last_packet = Packet()
        msg_decrypted = self._decrypt(msg_encrypted)
        self.last_packet.header = self.parse_header(msg_decrypted)
        self.last_packet.payload = self.parse_payload(msg_decrypted)

        # if len(msg_decrypted) < (self.last_packet.header_size + self.last_packet.payload_size):
        #     raise IndexError("Message contents longer than message buffer")

        return self.last_packet

    def parse_header(self, message: bytes):
        self.last_packet = Packet()
        bitstream = ConstBitStream(message)

        packet = self.last_packet
        try:
            packet.set_header_value("versionProtocole", bitstream.read('uint:8'))
            bitstream.read(8)           # Unused
            packet.set_header_value("tailleTrame", bitstream.read('uintle:16'))
            packet.set_header_value("idD2L", bitstream.read('uintle:64'))
            bitstream.read('bits:5')    # Unused
            packet.set_header_value("clef", bitstream.read('bits:3').uint)
            bitstream.read(24)          # Unused
            packet.set_header_value("nombreAleatoire", bitstream.read('uintle:128'))
            packet.set_header_value("CRC16", bitstream.read('uintle:16'))
            packet.set_header_value("taillePayload", bitstream.read('uintle:16'))
            packet.set_header_value("isRequeteOuReponse", bitstream.read('bool:1'))
            packet.set_header_value("typePayload", bitstream.read('bits:7').uint)
            packet.set_header_value("isErreurTraitement", bitstream.read('bool:1'))
            packet.set_header_value("commandeSuivante", bitstream.read('bits:7').uint)
        except ReadError:
            print(f"Failed to parse header: {bitstream}")
        return packet.header

    def parse_payload(self, message: bytes) -> Any:
        packet = self.last_packet
        packet.payload = None

        payload_size = packet.get_payload_size()
        if payload_size <= 0:
            print("No payload available for this message")
        else:
            payload = message[OFFSET_PAYLOAD:payload_size]
            try:
                payload_string = payload.decode('utf-8')
                print(payload_size, payload_string)
                packet.payload = json.loads(payload_string)
            except (UnicodeDecodeError, json.JSONDecodeError) as error_msg:
                error(error_msg)

        return packet.payload

        # Append end of JSON if omitted
        # if "}" != str_payload[-1]:
        #     if "\"" not in str_payload[-2:]:
        #         str_payload += '"'
        #     if "}" not in str_payload[-2:]:
        #         str_payload += ' }'

    def _decrypt(self, msg_encrypted: bytes):
        message_done = msg_encrypted[:OFFSET_ENCRYPTED]
        message_todo = msg_encrypted[OFFSET_ENCRYPTED:]
        message_todo = decrypt(message_todo, self.d2l_key, self.d2l_iv)
        return message_done + message_todo
