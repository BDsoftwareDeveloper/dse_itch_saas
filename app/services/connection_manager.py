import socket
import threading
from app.models.server_config import Server
from sqlalchemy.orm import Session
from app.db.base_class import SessionLocal
from app.db.config import settings
from app.services.packet_decoder import PacketDecoder
from app.services.client_processor import ClientPacketProcessor
import struct
import time

RETRY_COUNT = 5

class ConnectionManager:

    def __init__(self):
        self.connections = {}

    def connect_server(self, server: Server):
        primary_ip = server.primary_ip
        port = server.port

        for attempt in range(RETRY_COUNT):
            try:
                print(f"Connecting to primary {primary_ip}:{port}, attempt {attempt+1}")
                sock = socket.create_connection((primary_ip, port), timeout=5)
                print(f"Connected to primary {primary_ip}:{port}")
                self.connections[server.server_type] = sock
                self.login(sock)
                self.start_packet_loop(sock, server.server_type)
                return
            except Exception as e:
                print(f"Primary connection attempt {attempt+1} failed: {e}")
                time.sleep(2)  # backoff

        # Primary failed, try failover
        failover_ip = server.failover_ip
        port = server.port

        for attempt in range(RETRY_COUNT):
            try:
                print(f"Connecting to failover {failover_ip}:{port}, attempt {attempt+1}")
                sock = socket.create_connection((failover_ip, port), timeout=5)
                print(f"Connected to failover {failover_ip}:{port}")
                self.connections[server.server_type] = sock
                self.login(sock)
                self.start_packet_loop(sock, server.server_type)
                return
            except Exception as e:
                print(f"Failover connection attempt {attempt+1} failed: {e}")
                time.sleep(2)

        print(f"Failed to connect to {server.server_type} server after retries.")

    def login(self, sock):
        """Login after connecting to DSE server (binary protocol example)."""
        username = settings.DSE_USERNAME
        password = settings.DSE_PASSWORD
        session_id = ' ' * 10
        payload_format = '!Hc6s10s10s20s'
        payload = struct.pack(
            payload_format,
            47,
            b'L',
            username.encode(),
            password.encode(),
            session_id.rjust(10).encode(),
            str(1).rjust(20).encode()
        )
        print(f"Sending binary login packet")
        sock.sendall(payload)

    def start_packet_loop(self, sock, client_type):
        """Start a background thread to read and process packets."""
        decoder = PacketDecoder()
        processor = ClientPacketProcessor()
        def loop():
            try:
                while True:
                    packet = self.read_packet_by_length(sock)
                    decoded = decoder.decode(packet)
                    processor.process(decoded, client_type)
            except Exception as e:
                print(f"[{client_type}] Connection closed or error: {e}")
        thread = threading.Thread(target=loop, daemon=True)
        thread.start()

    def read_packet_by_length(self, sock):
        header = sock.recv(2)
        if len(header) < 2:
            raise Exception("Failed to read packet length header")
        packet_length = struct.unpack('!H', header)[0]
        remaining = packet_length - 2
        data = b''
        while remaining > 0:
            chunk = sock.recv(remaining)
            if not chunk:
                raise Exception("Socket closed before full packet received")
            data += chunk
            remaining -= len(chunk)
        return header + data

    def start(self):
        """Start connecting to all configured servers."""
        db: Session = SessionLocal()
        servers = db.query(Server).all()
        for server in servers:
            print(f"Starting connection for server: {server.name}")
            threading.Thread(target=self.connect_server, args=(server,), daemon=True).start()
