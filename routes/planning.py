from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


class Event(BaseModel):
    start: str | None
    end: str | None


router = APIRouter()


@router.get("/planning", name="Get all events")
async def get_planning_endp(event: Event):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented"
    )
