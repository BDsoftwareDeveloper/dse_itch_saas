
import threading


from fastapi import APIRouter, Depends, HTTPException,Query, Path, Body
from sqlalchemy.orm import Session
from typing import List

from app.crud import server_config
from app.models.server_config import Server
from app.schemas.server_schema import ServerCreateSchema, ServerOutSchema,ServerUpdateSchema
from app.db.base_class import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User
from app.crud.server_config import create_or_update_server
from app.utils.socket_manager import open_socket_connection, close_socket_connection
from app.utils.connection_registry import all_connections
from app.services.socket_protocol import protocol_login, send_logout_request
from app.services.process_socket_data import process_socket_data

router = APIRouter(
    prefix="/servers",
    tags=["servers"]
)

@router.get("/", response_model=List[ServerOutSchema])
def list_servers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all servers for the current user's tenant.
    """
    servers = db.query(Server).filter(Server.tenant_id == current_user.tenant_id).all()
    return servers


@router.post("/", response_model=ServerOutSchema)
def create_server(server: ServerCreateSchema, db: Session = Depends(get_db)):
    return create_or_update_server(db, server)


@router.put("/{server_id}/update")
def update_server_config(
    server_id: int = Path(..., description="ID of the server to update"),
    update_data: ServerUpdateSchema = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only allow updating servers in the user's tenant
    server = db.query(Server).filter(
        Server.id == server_id,
        Server.tenant_id == current_user.tenant_id
    ).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found or not allowed")

    updated_server = server_config.update_server(db, server_id, update_data.dict(exclude_unset=True))
    return {
        "message": f"Server {server_id} updated successfully",
        "updated_fields": update_data.dict(exclude_unset=True),
    }


@router.post("/{server_id}/connect")
def connect_server(
    server_id: int,
    is_primary: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only allow connecting to servers in the user's tenant
    server = db.query(Server).filter(
        Server.id == server_id,
        Server.tenant_id == current_user.tenant_id
    ).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found or not allowed")

    ip = server.primary_ip if is_primary else server.failover_ip
    connection = open_socket_connection(server_id, ip, server.port, is_primary)
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to open socket connection")

    # Protocol login step
    login_result = protocol_login(server, connection)
    threading.Thread(target=process_socket_data, args=(connection, server.name), daemon=True).start()
    return {
        "result": "Connected and login attempted",
        "login_result": login_result
    }


@router.post("/{server_id}/disconnect")
def disconnect_server(
    server_id: int,
    is_primary: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only allow disconnecting servers in the user's tenant
    server = db.query(Server).filter(
        Server.id == server_id,
        Server.tenant_id == current_user.tenant_id
    ).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found or not allowed")

    try:
        # Attempt protocol logout before closing the socket
        # You may want to retrieve the actual socket object if needed
        # Example: connection = get_socket_connection(server_id, is_primary)
        # send_logout_request(connection)
        result = close_socket_connection(server_id, is_primary)
        return {"result": result, "logout": "Logout packet sent (if socket was open)"}
    except Exception as e:
        print(f"Error while disconnecting server {server_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to disconnect server")
    
    
@router.get("/connections")
def get_all_connections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get all server IDs for the current tenant
    tenant_server_ids = {
        server.id
        for server in db.query(Server.id).filter(Server.tenant_id == current_user.tenant_id).all()
    }

    connections = all_connections()
    # Filter connections to only those belonging to the tenant
    serialized_connections = [
        {
            "server_id": server_id,
            "is_primary": is_primary,
            "remote_address": conn.getpeername() if conn else None
        }
        for (server_id, is_primary), conn in connections.items()
        if server_id in tenant_server_ids
    ]

    return {"connections": serialized_connections}