from fastapi import FastAPI

from api.server.routes.users import router as UsersRouter
from api.server.routes.chatbot import router as chatbot_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://itwi.me"],  # Adjust this to your Angular application URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
#app.include_router(UsersRouter, tags=["Users"], prefix="/user")

app.include_router(chatbot_router, tags=["Ai"], prefix="/chat")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
