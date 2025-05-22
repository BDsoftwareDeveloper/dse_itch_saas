# # app/main.py
# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# # from app.api.v1.endpoints import tenant_router
# # from lifespan import lifespan
# from app.api.v1.endpoints import auth_router, tenant_router,server_router, user_router

# from app.services.connection_manager import ConnectionManager

# # Define the lifespan function
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Lifespan function to manage application startup and shutdown events.
#     """
#     connection_manager = ConnectionManager()
#     # Startup event
#     print("Starting the Scheduler Service...")
#     # init_db()  # Initialize the database
#     print("Database initialized successfully.")
#     await connection_manager.start()  # connect to configured servers

#     yield  # Yield control to the application

#     # Shutdown event
#     print("Shutting down the Scheduler Service...")


# app = FastAPI(
#     title="DSE Feed SaaS Platform",
#     description="SaaS platform to connect and manage DSE server feeds securely.",
#     version="1.0.0",
#     lifespan=lifespan,
# )





# @app.get("/")
# def root():
#     return {"message": "DSE SaaS App is running 🚀"}



# app.include_router(auth_router.router)
# app.include_router(user_router.router)
# app.include_router(server_router.router)
# app.include_router(tenant_router.router)




# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# from fastapi.openapi.utils import get_openapi

# from app.api.v1.endpoints import auth_router, tenant_router, server_router, user_router
# from app.services.connection_manager import ConnectionManager


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Lifespan function to manage application startup and shutdown events.
#     """
#     connection_manager = ConnectionManager()
#     print("Starting the Scheduler Service...")
#     # init_db()  # If you have DB initialization, call it here
#     print("Database initialized successfully.")
#     await connection_manager.start()
#     yield
#     print("Shutting down the Scheduler Service...")


# app = FastAPI(
#     title="DSE Feed SaaS Platform",
#     description="SaaS platform to connect and manage DSE server feeds securely.",
#     version="1.0.0",
#     lifespan=lifespan,
# )

# # Optional root endpoint
# @app.get("/")
# def root():
#     return {"message": "DSE SaaS App is running 🚀"}


# # Include routers
# app.include_router(auth_router.router)
# app.include_router(user_router.router)
# app.include_router(server_router.router)
# app.include_router(tenant_router.router)


# # Add JWT Bearer auth to Swagger UI
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title=app.title,
#         version=app.version,
#         description=app.description,
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT"
#         }
#     }
#     for path in openapi_schema["paths"].values():
#         for method in path.values():
#             method.setdefault("security", [{"BearerAuth": []}])
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi



from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi.openapi.utils import get_openapi

from app.api.v1.endpoints import auth_router, tenant_router, server_router, user_router
from app.auth.dependencies import get_current_user
from app.services.connection_manager import ConnectionManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # connection_manager = ConnectionManager()
    print("Starting the Scheduler Service...")
    # await connection_manager.start()
    print("Database initialized successfully.")
    yield
    print("Shutting down the Scheduler Service...")


app = FastAPI(
    title="DSE Feed SaaS Platform",
    description="SaaS platform to connect and manage DSE server feeds securely.",
    version="1.0.0",
    lifespan=lifespan,
    # dependencies=[Depends(get_current_user)],  # optional boost to make it register in docs
)


@app.get("/")
def root():
    return {"message": "DSE SaaS App is running 🚀"}


# Include all routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(server_router.router)
app.include_router(tenant_router.router)


# Custom OpenAPI schema with JWT bearer token support
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply security globally to all endpoints
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
