# connection_registry.py
import socket
from typing import Dict, Tuple

# DO NOT MODIFY THIS DIRECTLY OUTSIDE THIS MODULE
_active_connections: Dict[Tuple[int, bool], socket.socket] = {}

def get_active_connection(server_id: int, is_primary: bool) -> socket.socket | None:
    return _active_connections.get((server_id, is_primary))

def set_active_connection(server_id: int, is_primary: bool, conn: socket.socket):
    _active_connections[(server_id, is_primary)] = conn

def has_active_connection(server_id: int, is_primary: bool) -> bool:
    return (server_id, is_primary) in _active_connections

def remove_connection(server_id: int, is_primary: bool):
    _active_connections.pop((server_id, is_primary), None)

def all_connections() -> Dict[Tuple[int, bool], socket.socket]:
    return _active_connections.copy()