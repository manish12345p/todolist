from fastapi import  Request
from http import HTTPStatus
import logging
logging.basicConfig(level=logging.INFO, format='Time : %(asctime)s | Level : %(levelname)s | %(message)s ')
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    try:
        if response.status_code >=200 and response.status_code < 300:
            logging.info(f"Method: {request.method} | Url : {request.url} | Status : {response.status_code} {HTTPStatus(response.status_code).phrase}")
        elif response.status_code >=300 and response.status_code < 400:
            logging.warning(f"Method: {request.method} | Url : {request.url} | Status : {response.status_code} {HTTPStatus(response.status_code).phrase}")  
        elif response.status_code >=400 and response.status_code < 500:
            logging.error(f"Method: {request.method} | Url : {request.url} | Status : {response.status_code} {HTTPStatus(response.status_code).phrase}")
    except Exception as e:
        logging.error(f"Method:{request.method} | Url : {request.url} | Status:{response.status_code} {HTTPStatus(response.status_code).phrase} | Error logging request: {e}")
    return response