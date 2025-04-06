from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import user, temperature, ph, turbidity, feeding, auth

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(feeding.router)
app.include_router(ph.router)
app.include_router(user.router)
app.include_router(temperature.router)
app.include_router(turbidity.router)
