from fastapi import FastAPI
from .routers import dog, cat, ws
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import dog as dog_model, cat as cat_model

# konfiguracja i inicjalizacja bazy danych
Base.metadata.create_all(bind=engine)

# Inicjalizacja aplikacji FastAPI
app = FastAPI(
    title="Animal Shelter Manager API",
    description="REST API do zarządzania psami i kotami w schronisku",
    version="1.0.0"
)

# Lista dozwolonych origins dla CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost",
    "http://127.0.0.1",
]

# Konfiguracja middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rejestracja routerów
app.include_router(dog.router)
app.include_router(cat.router)
app.include_router(ws.router)

