from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


@router.get("/", name="Get homeworks")
async def get_homework_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        query = """
        SELECT
          h.title as homework_title,
          h.due_date as homework_due_date,
          h.details as homework_details,
          u.firstname as author_first_name,
          u.lastname as author_last_name
        FROM assigned_homework h
        JOIN "user" u ON h.author = u.id
        """

        if id is None:
            query += f"WHERE h.id = {id}"

        query += ";"

        c.execute(query)
        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such homework",
            )

        return res
