from fastapi import FastAPI
from .routers import dog, dog_history, ws

app = FastAPI()

app.include_router(dog.router)
app.include_router(dog_history.router)
app.include_router(ws.router)
