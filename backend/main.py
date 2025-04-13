from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import user, temperature, ph, turbidity, feeding, auth, real_time_stats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
app.include_router(real_time_stats.router)
