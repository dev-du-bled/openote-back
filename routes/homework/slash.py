from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Homework(BaseModel):
    title: str | None
    due_date: str | None
    author: int | None
    details: str | None


@router.get("/", name="Get homeworks")
async def get_homework_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        fields = gen.get_obj_fields(Homework)
        selected_fields = gen.format_fields_to_select_sql(fields)

        c.execute(
            f"""SELECT {selected_fields} FROM homework WHERE id=%s;""",
            (id,),
        )
        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such homework",
            )

        return res
