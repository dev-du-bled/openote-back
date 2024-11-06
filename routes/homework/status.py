from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Homework(BaseModel):
    is_done: bool | None
    student: int | None


@router.patch("/status", name="Mark as done homeworks")
async def get_homeworks_endp(
    homework: Homework, id: int | None = None, Authorization: str = Header(...)
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        role_id = ens.get_user_col_from_token(c, "id", Authorization)

        if role == ens.UserRole.student:
            c.execute(
                """
                UPDATE homework_status
                SET is_done = %s
                WHERE student = %s AND homework = %s;
                """,
                (homework.is_done, role_id, id),
            )

        elif role == ens.UserRole.teacher:
            ens.ensure_given_id_is_student(c, homework.student)

            c.execute(
                """
                UPDATE homework_status
                SET is_done = %s
                WHERE student = %s AND homework = %s;
                """,
                (homework.is_done, homework.student, id),
            )

        conn.commit()
