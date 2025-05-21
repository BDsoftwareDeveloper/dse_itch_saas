import struct
class ClientProcessStrategy:
    def process(self, decoded_packet):
        raise NotImplementedError

class MarketFeedProcessStrategy(ClientProcessStrategy):
    def process(self, decoded_packet):
        print(f"[MarketFeed] {decoded_packet}")
        # Add marketfeed-specific logic here

class IndexProcessStrategy(ClientProcessStrategy):
    def process(self, decoded_packet):
        print(f"[Index] {decoded_packet}")
        # Add index-specific logic here

class NewsProcessStrategy(ClientProcessStrategy):
    def process(self, decoded_packet):
        print(f"[News] {decoded_packet}")
        # Add news-specific logic here

class DefaultProcessStrategy(ClientProcessStrategy):
    def process(self, decoded_packet):
        print(f"[Unknown Client] {decoded_packet}")

class ClientPacketProcessor:
    def __init__(self):
        self.strategies = {
            "market": MarketFeedProcessStrategy(),
            "index": IndexProcessStrategy(),
            "news": NewsProcessStrategy(),
        }
        self.default_strategy = DefaultProcessStrategy()

    def process(self, decoded_packet, client_type):
        strategy = self.strategies.get(client_type, self.default_strategy)
        strategy.process(decoded_packet)

# Usage example:
if __name__ == "__main__":
    from packet_decoder import PacketDecoder

    decoder = PacketDecoder()
    processor = ClientPacketProcessor()

    # Simulate receiving a packet for each client type
    packet = struct.pack('!Hc10s8s', 20, b'A', b'SESSION01 ', b'OK      ')
    decoded = decoder.decode(packet)
    processor.process(decoded, "market")
    processor.process(decoded, "index")
    processor.process(decoded, "news")
    processor.process(decoded, "unknown")