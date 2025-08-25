from api.v1.head import AddDevice_IdToHeaderMiddleware
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from log.log import log_requests
from api.v1.routes import router as v1_router

app = FastAPI()
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Todo API",
        version="1.0.0",
        description="Todo API with global device-id header",
        routes=app.routes,
    )
    for path in openapi_schema["paths"].values():
        for method in path.values():
            parameters = method.get("parameters", [])
            if not any(p["name"] == "Device-Id" for p in parameters):
                parameters.append({
                    "name": "Device-Id",
                    "in": "header",
                    "required": True,
                    "schema": {
                        "type": "string",
                        "default": "example-device-id"
                    },
                    
                })
            method["parameters"] = parameters

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.add_middleware(AddDevice_IdToHeaderMiddleware)
app.middleware("http")(log_requests)
app.include_router(v1_router, prefix="/v1", tags=["v1"])