from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from db import get_db_connection


class Event(BaseModel):
    start: str | None
    end: str | None


router = APIRouter()


@router.get("/planning", name="Get all events")
async def get_planning_endp(event: Event, Authorization: str = Header(...)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented"
    )
