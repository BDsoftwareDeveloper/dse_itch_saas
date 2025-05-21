from app.services.packet_decoder import PacketDecoder
from app.services.client_processor import ClientPacketProcessor
from app.services.socket_protocol import read_packet_by_length
import logging

def process_socket_data(connection, client_type):
    decoder = PacketDecoder()
    processor = ClientPacketProcessor()
    try:
        print(f"[{client_type}] Starting data processing loop...")
        while True:
            try:
                packet = read_packet_by_length(connection)
                if not packet:
                    print(f"[{client_type}] No packet received, socket may be closed.")
                    break
                print(f"[{client_type}] Raw packet: {packet.hex()}")
                decoded = decoder.decode(packet)
                print(f"[{client_type}] Decoded packet: {decoded}")
                processor.process(decoded, client_type)
            except Exception as inner_e:
                print(f"[{client_type}] Error in packet loop: {inner_e}")
                logging.error(f"[{client_type}] Error in packet loop: {inner_e}")
                break
    except Exception as e:
        if str(e) == "Failed to read packet length header":
            logging.info(f"[{client_type}] Socket closed normally.")
        else:
            logging.error(f"[{client_type}] Socket processing error: {e}")