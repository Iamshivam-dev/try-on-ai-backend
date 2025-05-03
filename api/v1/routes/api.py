
# app/api/v1/routes/api.py

from fastapi import APIRouter
from api.v1.controllers import file_controller

router = APIRouter()

router.include_router(file_controller.router)