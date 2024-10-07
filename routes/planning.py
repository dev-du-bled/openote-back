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
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        c.execute("""SELECT token FROM sessions WHERE token=%s;""", (Authorization,))
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )

        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented"
        )
