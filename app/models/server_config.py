from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


from sqlalchemy import Column, Integer, String, ForeignKey


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    primary_ip = Column(String, nullable=False)
    failover_ip = Column(String, nullable=True)
    port = Column(Integer, nullable=False)
    # failover_port = Column(Integer, nullable=True)  # Optional
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    description = Column(String)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    tenant = relationship("Tenant", back_populates="servers")