from fastapi import FastAPI
from app.api.v1.routes.auth_routes import router as auth_router
from app.infrastructure.database.db import create_database

app = FastAPI(title="API FRONT EASYGROW")

@app.on_event("startup")
async def startup():
    create_database()

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])