from fastapi import APIRouter, Header, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Homework(BaseModel):
    homework_id: int
    is_done: bool

@router.patch(
    "/status", name="Mark given homework as done", status_code=status.HTTP_204_NO_CONTENT
)
async def edit_homeworks_status_endp(homework: Homework, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        user_id = ens.get_user_col_from_token(c, "id", Authorization)

        ens.ensure_user_is_role(role, ens.UserRole.student)

        query = """
        UPDATE
          homework_status
        SET
          is_done = %s
        WHERE
          student = %s AND homework = %s;
        """

        c.execute(query, (homework.is_done, user_id, homework.homework_id))

        if c.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Homework")

        conn.commit()
