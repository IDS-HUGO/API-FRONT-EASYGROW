from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes.auth_routes import router as auth_router
from app.api.v1.routes.device_routes import router as device_router
from app.api.v1.routes.user_routes import router as user_router
from app.api.v1.routes.plant_routes import router as plant_router
from app.api.v1.routes.catalog_routes import router as catalog_router
from app.api.v1.routes.sensor_routes import router as sensor_router

from app.infrastructure.database.db import create_database

app = FastAPI(title="API FRONT EASYGROW")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    create_database()

# Incluir rutas
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(device_router, prefix="/api/v1/devices", tags=["Devices"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(plant_router, prefix="/api/v1/plants", tags=["Plants"])
app.include_router(catalog_router, prefix="/api/v1/catalog", tags=["Catalog"])
app.include_router(sensor_router, prefix="/api/v1/sensors", tags=["Sensors"])