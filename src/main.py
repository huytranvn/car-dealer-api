import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configs.database import Base, engine
from configs.settings import settings
from components.cars.endpoints.create import router as cars_create_router
from components.cars.endpoints.list import router as cars_list_router
from components.cars.endpoints.update import router as cars_update_router
from components.cars.models import Car  # Import to register the model
from components.users.endpoints.auth import router as auth_router
from components.users.models import User  # Import to register the model

# create tickets db
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ticket system api",
              description="Rest api for create, query and process tickets.",
              version="0.1.0",
              openapi_url="/openapi.json",
              docs_url="/docs",  # swagger UI
              redoc_url="/redoc")  # ReDoc

# Configure CORS
cors_origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Configurable via CORS_ORIGINS environment variable
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(cars_list_router)
app.include_router(cars_create_router)
app.include_router(cars_update_router)
app.include_router(auth_router)


@app.get("/ping")
def root_ping():
    """
    Server liveness check.
    """
    return {"status": "ok", "message": "I'm up!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)