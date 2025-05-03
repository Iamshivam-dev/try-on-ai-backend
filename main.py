from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.v1.routes import api as api_v1_router
import logging

app = FastAPI(debug=True)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return "not found"

app.include_router(api_v1_router.router, prefix="/api/v1")



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def unicorn_exception_handler(request, exc):
    logger.error(f"Error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )