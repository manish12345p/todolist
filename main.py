from fastapi import FastAPI
from api.v1.routes import router as v1_router


app = FastAPI()

app.include_router(v1_router, prefix="/v1", tags=["v1"])
