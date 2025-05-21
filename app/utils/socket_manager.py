# utils/socket_manager.py
from app.utils.connection_registry import get_active_connection,set_active_connection,remove_connection,has_active_connection
import socket

# def open_socket_connection(server_id: int, ip: str, port: int, is_primary: bool, timeout=5) -> str:
#     active_connections= get_active_connection(server_id, is_primary)
#     if active_connections is None:
#         active_connections = {}
        
#     key = (server_id, is_primary)
    
#     if key in active_connections:
#         return "Already connected"

#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.settimeout(timeout)
#         s.connect((ip, port))
#         # active_connections[key] = s
#         set_active_connection(server_id, is_primary, s)
#         print(f"Connected to {ip}:{port}")
#         return f"Connected:{ip}:{port} connection established{s}"
#     except Exception as e:
#         return f"Connection failed: {str(e)}"

def open_socket_connection(server_id: int, ip: str, port: int, is_primary: bool) -> str:
    if has_active_connection(server_id, is_primary):
        return "Already connected"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    set_active_connection(server_id, is_primary, s)
    return s


# def close_socket_connection(server_id: int, is_primary: bool) -> str:
#     active_connections= get_active_connection(server_id, is_primary)
    
#     key = (server_id, is_primary)
#     s = active_connections.get(key)
#     print(f"Closing connection for {key}")
#     print(f"Active connections: {active_connections}")
#     if s:
#         try:
#             s.shutdown(socket.SHUT_RDWR)
#             s.close()
#             del active_connections[key]
#             return "Connection closed"
#         except Exception as e:
#             return f"Error closing connection: {str(e)}"
#     return "No active connection"


def close_socket_connection(server_id: int, is_primary: bool) -> str:
    conn = get_active_connection(server_id, is_primary)
    if conn is None:
        return f"No active connection found for server {server_id} (is_primary={is_primary})"
    
    try:
        conn.shutdown(socket.SHUT_RDWR)  # Gracefully close
    except Exception as e:
        # You may ignore shutdown failure (e.g., already closed)
        print(f"Warning: shutdown failed for server {server_id}: {e}")

    try:
        conn.close()
        remove_connection(server_id, is_primary)
        return f"Connection closed for server {server_id} (is_primary={is_primary})"
    except Exception as e:
        return f"Error closing connection for server {server_id} (is_primary={is_primary}): {e}"