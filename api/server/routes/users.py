from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from api.server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)
from api.server.models.users import (
    ErrorResponseModel,
    ResponseModel,
    UserCreate,
    UserUpdate,
    UserResponse,
)

router = APIRouter()

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserCreate = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{username}", response_description="User data retrieved")
async def get_user_data(username: str):
    user = await retrieve_user(username)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.put("/{username}")
async def update_user_data(username: str, req: UserUpdate = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(username, req)
    if updated_user:
        return ResponseModel(
            "User with username: {} update is successful".format(username),
            "User updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )

@router.delete("/{username}", response_description="User data deleted from the database")
async def delete_user_data(username: str):
    deleted_user = await delete_user(username)
    if deleted_user:
        return ResponseModel(
            "User with username: {} removed".format(username), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with username {0} doesn't exist".format(username)
    )
