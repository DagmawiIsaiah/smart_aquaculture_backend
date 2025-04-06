from fastapi import APIRouter, status, Body, HTTPException
from backend.models import FeedingCollections, FeedingModel
from backend.database import feeding_collection

router = APIRouter(prefix="/feeding", tags=["Feeding"])


@router.post("/", response_description="Add feeding",
          response_model=FeedingModel,
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False,)
async def add_feeding(feeding: FeedingModel = Body(...)):
    new_feeding = await feeding_collection.insert_one(
        feeding.model_dump(by_alias=True, exclude=["id"])
    )
    created_feeding = await feeding_collection.find_one(
        {"_id": new_feeding.inserted_id}
    )
    return created_feeding


@router.get("/")
async def get_feeding():
    try:
        return FeedingCollections(
            feedings=await feeding_collection.find().to_list(10)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
