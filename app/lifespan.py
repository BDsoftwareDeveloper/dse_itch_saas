# app/lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.connection_manager import connection_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏫ App startup: initializing connection manager")
    await connection_manager.start()  # connect to configured servers

    yield  # <- app runs here

    print("⏬ App shutdown: closing all connections")
    await connection_manager.shutdown_all()
