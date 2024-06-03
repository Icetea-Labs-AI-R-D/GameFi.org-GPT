from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.conversation import NewConversation
from fastapi.requests import Request

route = FastAPI()

@route.post('/new')
async def new(request: Request):
    pass