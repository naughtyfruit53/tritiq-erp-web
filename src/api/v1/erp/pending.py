from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["pending"])

@router.get("/")
async def read_pending():
    return {"message": "Placeholder for pending items"}