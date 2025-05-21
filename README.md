# DSE ITCH SaaS App

This project is a microservices-based application for connecting to DSE (Dhaka Stock Exchange) market data feeds, handling multiple client types (marketfeed, index, news), and exposing a REST API for server management and monitoring.

## Features

- **Socket Connection Management**: Robust connection and failover logic for primary/failover DSE servers.
- **Login/Logout Protocol**: Handles binary protocol login and logout with DSE servers.
- **Packet Decoding**: Strategy pattern for decoding various packet types (LoginAck, LoginReject, Heartbeat, Sequenced, UnSequenced, Debug, EndOfSession, etc.).
- **Client-Type Processing**: Strategy pattern for processing packets differently for marketfeed, index, and news clients.
- **REST API**: FastAPI endpoints for connecting/disconnecting servers, listing connections, and monitoring.
- **Background Data Processing**: Each socket connection runs in a background thread, decoding and processing packets in real time.
- **MongoDB Integration**: Stores and updates connection status and statistics.
- **Extensible**: Easily add new packet types or client processing strategies.

## Project Structure

```
app/
  api/v1/endpoints/server_router.py      # REST API endpoints for server management
  services/
    connection_manager.py                # Manages socket connections and background threads
    packet_decoder.py                    # Packet decoding strategies
    client_processor.py                  # Client-type-based processing strategies
    process_socket_data.py               # Background data processing loop
    socket_protocol.py                   # Protocol helpers (login, logout, packet reading)
    socket_debug_utils.py                # (Optional) Debug helpers for socket data
  models/
    server_config.py                     # SQLAlchemy models for server configs
  db/
    base_class.py, config.py             # Database setup and settings
  test/
    test_packet_decoder.py               # Unit tests for packet decoding
README.md
```

## How It Works

1. **Startup**: The app connects to all configured DSE servers (marketfeed, index, news) using `ConnectionManager`.
2. **Login**: Sends a binary login packet and waits for a login response.
3. **Data Loop**: On successful login, starts a background thread to continuously read, decode, and process packets.
4. **REST API**: Use FastAPI endpoints to connect/disconnect servers and monitor status.

## Key Code Patterns

- **Packet Decoding**: Uses the Strategy pattern for clean, extensible decoding.
- **Client Processing**: Uses the Strategy pattern to process packets differently for each client type.
- **Robust Socket Handling**: Handles disconnects, protocol errors, and failover gracefully.

## Example Usage

### Start All Connections on FastAPI Startup

```python
from fastapi import FastAPI
from app.services.connection_manager import ConnectionManager

app = FastAPI()
connection_manager = ConnectionManager()

@app.on_event("startup")
def start_connections():
    connection_manager.start()
```

### Connect/Disconnect via REST API

- `POST /servers/{server_id}/connect?is_primary=true|false`
- `POST /servers/{server_id}/disconnect?is_primary=true|false`
- `GET /servers/connections`

### Packet Decoding Example

```python
from app.services.packet_decoder import PacketDecoder

decoder = PacketDecoder()
packet = ... # bytes from socket
decoded = decoder.decode(packet)
print(decoded)
```

## Development & Testing

- Run unit tests:  
  ```bash
  python -m unittest app/test/test_packet_decoder.py
  ```
- Run the FastAPI server:  
  ```bash
  uvicorn main:app --reload
  ```

## Troubleshooting

- If you see `Socket closed before full packet received`, check your protocol and login handling.
- Use `socket_debug_utils.py` for detailed packet read debugging.
- Ensure MongoDB and PostgreSQL are running and accessible.

## Extending

- Add new packet types: Implement a new `PacketDecodeStrategy` and register it in `PacketDecoder`.
- Add new client types: Implement a new `ClientProcessStrategy` and register it in `ClientPacketProcessor`.

---

**For more details, see the code comments and docstrings in each module.**
