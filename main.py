from fastapi import FastAPI
from log.log import log_requests
from api.v1.routes import router as v1_router

app = FastAPI()
app.middleware("http")(log_requests)
app.include_router(v1_router, prefix="/v1", tags=["v1"])