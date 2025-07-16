from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes.auth_routes import router as auth_router
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

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])