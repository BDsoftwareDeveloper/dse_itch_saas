import struct

class PacketDecodeStrategy:
    def decode(self, packet: bytes, packet_length: int):
        raise NotImplementedError

class LoginAckDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        session_id = packet[3:13].decode(errors='ignore').strip()
        message = packet[13:].decode(errors='ignore').strip()
        return {
            "type": "LoginAck",
            "packet_length": packet_length,
            "session_id": session_id,
            "message": message
        }

class HeartbeatDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        return {
            "type": "Heartbeat",
            "packet_length": packet_length
        }

class LogoutAckDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        return {
            "type": "LogoutAck",
            "packet_length": packet_length
        }

class SequencedPacketDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        # Implement your actual decoding logic for SequencedPacket here
        return {
            "type": "SequencedPacket",
            "packet_length": packet_length,
            "raw": packet.hex()
        }

class UnSequencedPacketDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        # Implement your actual decoding logic for UnSequencedPacket here
        return {
            "type": "UnSequencedPacket",
            "packet_length": packet_length,
            "raw": packet.hex()
        }

class DebugPacketDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        # Implement your actual decoding logic for DebugPacket here
        return {
            "type": "DebugPacket",
            "packet_length": packet_length,
            "raw": packet.hex()
        }

class EndOfSessionPacketDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        # Implement your actual decoding logic for EndOfSessionPacket here
        return {
            "type": "EndOfSessionPacket",
            "packet_length": packet_length,
            "raw": packet.hex()
        }

class LoginRejectPacketDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        # Adjust the decoding logic as per your protocol for login reject packets
        # Here, we'll just show the raw message after the type byte
        message = packet[3:].decode(errors='ignore').strip()
        return {
            "type": "LoginRejectPacket",
            "packet_length": packet_length,
            "message": message
        }

class UnknownDecodeStrategy(PacketDecodeStrategy):
    def decode(self, packet: bytes, packet_length: int):
        packet_type = packet[2:3].decode()
        return {
            "type": f"Unknown({packet_type})",
            "packet_length": packet_length,
            "raw": packet.hex()
        }

class PacketDecoder:
    def __init__(self):
        self.strategies = {
            'A': LoginAckDecodeStrategy(),
            'J': LoginRejectPacketDecodeStrategy(),  # <-- Added here
            'R': HeartbeatDecodeStrategy(),
            'O': LogoutAckDecodeStrategy(),
            'S': SequencedPacketDecodeStrategy(),
            'U': UnSequencedPacketDecodeStrategy(),
            '+': DebugPacketDecodeStrategy(),
            'Z': EndOfSessionPacketDecodeStrategy(),
        }
        self.unknown_strategy = UnknownDecodeStrategy()

    def decode(self, packet: bytes):
        if len(packet) < 3:
            return {"error": "Packet too short"}
        packet_length = struct.unpack('!H', packet[:2])[0]
        packet_type = packet[2:3].decode()
        strategy = self.strategies.get(packet_type, self.unknown_strategy)
        return strategy.decode(packet, packet_length)

if __name__ == "__main__":
    decoder = PacketDecoder()

    # Example: LoginAck packet (type 'A')
    # Packet: [length=20][type='A'][session_id='SESSION01 '][message='OK']
    packet = struct.pack('!Hc10s8s', 20, b'A', b'SESSION01 ', b'OK      ')
    print("LoginAck:", decoder.decode(packet))

    # Example: Heartbeat packet (type 'R')
    packet = struct.pack('!Hc', 3, b'R')
    print("Heartbeat:", decoder.decode(packet))

    # Example: LogoutAck packet (type 'O')
    packet = struct.pack('!Hc', 3, b'O')
    print("LogoutAck:", decoder.decode(packet))

    # Example: SequencedPacket (type 'S')
    packet = struct.pack('!Hc5s', 8, b'S', b'data1')
    print("SequencedPacket:", decoder.decode(packet))

    # Example: UnSequencedPacket (type 'U')
    packet = struct.pack('!Hc5s', 8, b'U', b'data2')
    print("UnSequencedPacket:", decoder.decode(packet))

    # Example: DebugPacket (type '+')
    packet = struct.pack('!Hc5s', 8, b'+', b'debug')
    print("DebugPacket:", decoder.decode(packet))

    # Example: EndOfSessionPacket (type 'Z')
    packet = struct.pack('!Hc5s', 8, b'Z', b'end  ')
    print("EndOfSessionPacket:", decoder.decode(packet))

    # Example: LoginReject packet (type 'J')
    packet = struct.pack('!Hc8s', 11, b'J', b'REJECTED')
    print("LoginRejectPacket:", decoder.decode(packet))

    # Example: Unknown packet type
    packet = struct.pack('!Hc5s', 8, b'X', b'unknw')
    print("Unknown:", decoder.decode(packet))