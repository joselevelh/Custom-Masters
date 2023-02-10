from fastapi import APIRouter

pins_router = APIRouter(
    prefix="/pins",
    tags=["pins"],
    responses={404: {"description": "Pin not found"}},
    )
