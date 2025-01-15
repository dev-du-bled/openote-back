from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import Database

router = APIRouter()
db = Database()


class Homework(BaseModel):
    title: str
    due_date: str
    details: str | None
    assigned_class: int


@router.post("/manage", name="Create a homework", status_code=status.HTTP_201_CREATED)
async def add_homework_endp(homework: Homework, Authorization: str = Header(...)):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        role_id = ens.get_user_col_from_token(c, "id", Authorization)

        QUERY = """
        INSERT INTO
          assigned_homework (title, due_date, author, details, assigned_class)
        VALUES
          (%s, %s, %s, %s, %s)
        RETURNING id;
        """

        try:
            c.execute(QUERY,
                (
                    homework.title,
                    homework.due_date,
                    role_id,
                    homework.details,
                    homework.assigned_class if role == ens.UserRole.teacher else None,
                ),
            )

            row = c.fetchone()
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Failed to create homework",
                )

            created_id = row["id"]

            c.execute(
                """
                INSERT INTO
                  homework_status (homework, student, is_done)
                VALUES
                  (%s, %s, false);
                """,
                (created_id, role_id),
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
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role_id = ens.get_user_col_from_token(c, "id", Authorization)

        c.execute(
            """
        DELETE FROM
          assigned_homework
        WHERE
          id=%s AND author=%s;
        """,
            (id, role_id),
        )

        conn.commit()


@router.patch(
    "/manage", name="Update a homework", status_code=status.HTTP_204_NO_CONTENT
)
async def edit_homework_endp(
    id: int, homework: Homework, Authorization: str = Header(...)
):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role_id = ens.get_user_col_from_token(c, "id", Authorization)

        fields = gen.get_obj_fields(Homework)
        c.execute(
            f"SELECT {gen.format_fields_to_select_sql(fields)} FROM assigned_homework WHERE id=%s AND author=%s;",
            (id, role_id),
        )

        old_data = c.fetchone()
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such homework"
            )

        new_data = gen.merge_data(Homework, old_data, homework)

        c.execute(
            f"""UPDATE assigned_homework SET {gen.format_fields_to_update_sql(fields)} WHERE id=%s AND author=%s;""",
            (new_data + (id, role_id)),
        )

        conn.commit()
