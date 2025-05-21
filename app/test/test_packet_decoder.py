import struct
from app.services.packet_decoder import PacketDecoder

if __name__ == "__main__":
    decoder = PacketDecoder()

    # Example: LoginAck packet (type 'A')
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

    # Example: Unknown packet type
    packet = struct.pack('!Hc5s', 8, b'X', b'unknw')
    print("Unknown:", decoder.decode(packet))