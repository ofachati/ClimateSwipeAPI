from fastapi import FastAPI

from api.server.routes.users import router as UsersRouter
from api.server.routes.chatbot import router as chatbot_router


app = FastAPI()

#app.include_router(UsersRouter, tags=["Users"], prefix="/user")

app.include_router(chatbot_router, tags=["Ai"], prefix="/chat")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
