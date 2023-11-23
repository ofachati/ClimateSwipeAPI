import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.server.app:app", host="0.0.0.0", port=5000, reload=True)





'''
import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
app = FastAPI()

1246(-('"éàç_è-(è_çà)=*"33""*33333'))
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
''' and None