from fastapi import APIRouter
import random

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Hello World",
        "random_number": random.randint(1, 1000),
        "timestamp": "2023-09-15T12:00:00Z"  # Фиксированная дата для уникальности
    }
