from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
class AddDevice_IdToHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        query_params = dict(request.query_params)

        user_id = query_params.pop("Device-Id", None)
        if user_id:
            request.scope["headers"].append((b"Device-id", user_id.encode()))
            scope = request.scope
            scope["query_string"] = b"&".join(
                f"{k}={v}".encode() for k, v in query_params.items()
            )

        response = await call_next(request)
        return response