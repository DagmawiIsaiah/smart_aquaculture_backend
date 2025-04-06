from fastapi import APIRouter, status, Body, HTTPException
from backend.models import PHCollections, PHModel
from backend.database import ph_collection

router = APIRouter(prefix="/ph", tags=["PH"])


@router.post("/", response_description="Add PH",
          response_model=PHModel,
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False,)
async def add_ph(ph: PHModel = Body(...)):
    new_ph = await ph_collection.insert_one(
        ph.model_dump(by_alias=True, exclude=["id"])
    )
    created_ph = await ph_collection.find_one(
        {"_id": new_ph.inserted_id}
    )
    return created_ph


@router.get("/")
async def get_phs():
    try:
        return PHCollections(
            phs=await ph_collection.find().to_list(10)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
