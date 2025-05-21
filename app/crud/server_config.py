from sqlalchemy.orm import Session
from app.models.server_config import Server
from app.schemas import server_schema




def create_or_update_server(db: Session, server_data: server_schema.ServerCreateSchema):
    server = db.query(Server).filter(Server.name == server_data.name).first()

    if server:
        # Update existing
        for field, value in server_data.model_dump().items():
            setattr(server, field, value)
    else:
        # Create new
        server = Server(**server_data.model_dump())
        db.add(server)

    db.commit()
    db.refresh(server)
    return server



def create_server(db: Session, server: server_schema.ServerCreateSchema):
    db_server = Server(**server.dict())
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

def get_server(db: Session, server_id: int):
    return db.query(Server).filter(Server.id == server_id).first()

def get_servers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Server).offset(skip).limit(limit).all()

# def update_server(db: Session, server_id: int, updates: server_schema.ServerConfigUpdate):
#     db_server = get_server(db, server_id)
#     if not db_server:
#         return None
#     update_data = updates.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_server, key, value)
#     db.commit()
#     db.refresh(db_server)
#     return db_server

def update_server(db: Session, server_id: int, updates:server_schema.ServerUpdateSchema):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        return None

    for field, value in updates.items():
        setattr(server, field, value)

    db.commit()
    db.refresh(server)
    return server
def delete_server(db: Session, server_id: int):
    db_server = get_server(db, server_id)
    if not db_server:
        return None
    db.delete(db_server)
    db.commit()
    return db_server
