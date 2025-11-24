from fastapi import FastAPI
from api.v1.routers import parser_router, health_router

def create_app():
    app = FastAPI(title="ProtocolIQ Parser Service (Hexagonal)")
    app.include_router(health_router.router, prefix="/health")
    app.include_router(parser_router.router, prefix="/v1/parser")
    return app

app = create_app()
