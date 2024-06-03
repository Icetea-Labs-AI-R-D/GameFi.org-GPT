from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.conf import settings
from fastapi.middleware.cors import CORSMiddleware
from openai_queue import openai_queue
@asynccontextmanager
async def register_init(app: FastAPI):
    
    openai_queue.init_queue()
    
    yield
    
    openai_queue.close_queue()

def register_app():
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        openapi_url=settings.OPENAPI_URL,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        lifespan=register_init,
    )
    register_middleware(app)
    register_router(app)
    return app

def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
def register_router(app: FastAPI):
    app.include_router(router)