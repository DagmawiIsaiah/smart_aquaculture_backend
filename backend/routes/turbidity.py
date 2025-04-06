from fastapi import APIRouter, status, Body, HTTPException
from backend.models import TurbidityCollection, TurbidityModel
from backend.database import turbidity_collection

router = APIRouter(prefix="/turbidity", tags=["Turbidity"])


@router.post("/", response_description="Add Turbidity",
          response_model=TurbidityModel,
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False,)
async def add_turbidity(turbidity: TurbidityModel = Body(...)):
    new_turbidity = await turbidity_collection.insert_one(
        turbidity.model_dump(by_alias=True, exclude=["id"])
    )
    created_turbidity = await turbidity_collection.find_one(
        {"_id": new_turbidity.inserted_id}
    )
    return created_turbidity


@router.get("/")
async def get_turbidities():
    try:
        return TurbidityCollection(
            turbidities=await turbidity_collection.find().to_list(10)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
