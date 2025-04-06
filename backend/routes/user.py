from fastapi import APIRouter, HTTPException, status, Body
from backend.models import UserModel, UserCollection
from backend.database import user_collection
from backend.utils import get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_description="Create new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: UserModel = Body(...)):
    user.password = get_password_hash(user.password)
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


@router.get(
    "/"
)
async def list_users():
    """
    List all of the users data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    try:
        return UserCollection(
            users=await user_collection.find().to_list(10)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
