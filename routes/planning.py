from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel


class Event(BaseModel):
    start: str | None
    end: str | None


router = APIRouter()


@router.get("/planning", name="Get all events")
async def get_planning_endp(event: Event, Authorization: str = Header(...)):
    if event.start is None or event.end is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both start and end must be provided",
        )

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented"
    )
