from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db import Database


class Event(BaseModel):
    start: str | None
    end: str | None


router = APIRouter()
db = Database()


@router.get("/planning", name="Get events")
async def get_planning_endp():
    print(globals()["API_PORT"])

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented"
    )
