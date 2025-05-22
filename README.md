# DSE ITCH SaaS App

Project Name: DSE_ITCH_SAAS_APPLICATION || Designed on Microservice Architecture 

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






# README: Running DSE ITCH SaaS Docker Image in Production

## Overview

This guide explains how to run the `saifulweb2023/dse_itch_saas:main-latest` Docker image in a production-like environment using Docker CLI or Docker Compose.

---

## Prerequisites

- Docker installed on your production server  
- Docker Compose (optional but recommended)  
- `.env` file with database credentials and configuration  
- Docker network for service communication  
- Persistent volume for Postgres data  

---

## Environment Variables (.env)

Create a `.env` file with the following variables:

```env
POSTGRES_USER=saiful
POSTGRES_PASSWORD=saiful123
POSTGRES_DB=saas_dse_db
DATABASE_URL=postgresql://saiful:saiful123@dse_postgres:5432/saas_dse_db
```

Make sure these match your PostgreSQL configuration.

---

## Running the PostgreSQL Container

Use the official Postgres image with data persisted on a volume:

```bash
docker volume create dse_pgdata

docker run -d \
  --name dse_postgres \
  --network dse_network \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  -v dse_pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:latest
```

---

## Creating Docker Network

Create a user-defined bridge network to allow containers to resolve each other by name:

```bash
docker network create dse_network
```

---

## Running the FastAPI Application Container

Run your FastAPI app container on the same network:

```bash
docker run -d \
  --name dse_fastapi \
  --network dse_network \
  --env-file .env \
  -p 8000:8000 \
  saifulweb2023/dse_itch_saas:main-latest
```

---

## Using Docker Compose (Recommended)

Create a `docker-compose.yml`:

```yaml
version: '3.9'

services:
  dse_postgres:
    image: postgres:latest
    environment:
      POSTGRES_USER: saiful
      POSTGRES_PASSWORD: saiful123
      POSTGRES_DB: saas_dse_db
    volumes:
      - dse_pgdata:/var/lib/postgresql/data
    networks:
      - dse_network
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U saiful -d saas_dse_db"]
      interval: 5s
      retries: 5
      timeout: 5s

  dse_fastapi:
    image: saifulweb2023/dse_itch_saas:main-latest
    depends_on:
      dse_postgres:
        condition: service_healthy
    networks:
      - dse_network
    env_file:
      - .env
    ports:
      - "8000:8000"

networks:
  dse_network:

volumes:
  dse_pgdata:
```

Run with:

```bash
docker-compose up -d
```

---

## Production Recommendations

- Use a secure and complex password for your database user.  
- Do **not** expose PostgreSQL port (5432) publicly unless absolutely necessary.  
- Configure HTTPS for the FastAPI app using a reverse proxy (e.g., Nginx or Traefik).  
- Enable logging and monitoring for both containers.  
- Use environment variables or Docker secrets for sensitive data.  
- Regularly backup your database volume.  

---

## Troubleshooting

- **Cannot resolve `dse_postgres` hostname**: Ensure both containers are on the same Docker network.  
- **Database connection errors**: Check environment variables and network connectivity.  
- **Alembic migration failures**: Verify database readiness and credentials.  

---

## Summary

This setup provides a containerized environment to run your DSE ITCH SaaS application with a PostgreSQL database in production. Use Docker Compose for easier management and automatic dependency handling.

---






## Git push issue
```
bdtask@py-saiful2 MINGW64 ~/microservices/dse_itch_saas_app/dse_itch_saas (feature/new-api)
$ eval "$(ssh-agent -s)"
ssh-add -l
Agent pid 502
The agent has no identities.

bdtask@py-saiful2 MINGW64 ~/microservices/dse_itch_saas_app/dse_itch_saas (feature/new-api)
$ ^C

bdtask@py-saiful2 MINGW64 ~/microservices/dse_itch_saas_app/dse_itch_saas (feature/new-api)
$ ssh-add ~/git_access_key
Identity added: /c/Users/bdtask/git_access_key (saifulrubd@gmail.com)

bdtask@py-saiful2 MINGW64 ~/microservices/dse_itch_saas_app/dse_itch_saas (feature/new-api)
$ ssh-add -l
4096 SHA256:XAN2MT8BMYbH8YYQXYnb5gFR/bFlZFu8Z6x37Qp5HpI saifulrubd@gmail.com (RSA)

bdtask@py-saiful2 MINGW64 ~/microservices/dse_itch_saas_app/dse_itch_saas (feature/new-api)
$ ssh -T git@github.com
Hi BDsoftwareDeveloper! You've successfully authenticated, but GitHub does not provide shell access.

bdtask@py-saiful2 MINGW64 ~/microservices/dse_itch_saas_app/dse_itch_saas (feature/new-api)
$ git push origin feature/new-api
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 12 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 368 bytes | 368.00 KiB/s, done.
Total 4 (delta 3), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To github.com:BDsoftwareDeveloper/dse_itch_saas.git
   242873e..f8928a3  feature/new-api -> feature/new-api

bdtask@py-saiful2 MINGW64 ~/microservices/dse_itch_saas_app/dse_itch_saas (feature/new-api)
```
