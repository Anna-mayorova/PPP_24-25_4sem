from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.db.database import engine, Base
from app.api.auth import auth_router, router as ws_router
#Для запуска программы команда uvicorn app.main:app --reload (выполняем из lab2_fastapi!!!!!!

app = FastAPI()

# обработчк ошибок в ноорм формате
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(ws_router)
@app.get("/")
def root():
    return {
        "message": "Доступные команды для выаолнения ( в /docs)",
        "endpoints": {
            "signup": "/sign-up/",
            "docs": "/docs",
            "healthcheck": "/"},
            "TODO": {
                '1 - сделано ': '/login',
                '2- cделано': '/user/me/',
                '3 - сделано':'"/shortest-path/", response_model=PathResult'
                    },
        }

print()

