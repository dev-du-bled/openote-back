from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Homework(BaseModel):
    title: str
    due_date: str
    details: str | None
    assigned_class: int


@router.post("/manage", name="Create a homework", status_code=status.HTTP_201_CREATED)
async def get_homework_endp(homework: Homework, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        role_id = ens.get_user_col_from_token(c, "id", Authorization)

        ens.ensure_user_is_role(role, ens.UserRole.teacher)

        try:
            c.execute(
                """INSERT INTO assigned_homework (title, due_date, author, details, assigned_class) VALUES (%s, %s, %s, %s, %s);""",
                (
                    homework.title,
                    homework.due_date,
                    role_id,
                    homework.details,
                    homework.assigned_class,
                ),
            )

            conn.commit()

        except errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Homework already exists"
            )


@router.delete(
    "/manage", name="Delete a homework", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_homework_endp(id: int, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_role(role, ens.UserRole.teacher)

        c.execute("DELETE FROM homework_status WHERE homework=%s;", (id,))

        c.execute("DELETE FROM assigned_homework WHERE id=%s;", (id,))

        conn.commit()
