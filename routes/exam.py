from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Exam(BaseModel):
    title: str | None
    max_mark: int | None
    coefficient: float | None
    date: str | None


@router.get("", name="List exams")
async def get_exam_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        _ = ens.get_role_from_token(c, Authorization)

        fields = gen.get_obj_fields(Exam)
        selected_fields = gen.format_fields_to_select_sql(fields)

        if id is None:
            c.execute(f"""SELECT {selected_fields} FROM exams;""")
            res = c.fetchall()

        else:
            c.execute(
                f"""SELECT {selected_fields} FROM exams WHERE id=%s;""",
                (id,),
            )
            res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such exam",
            )

        return res


@router.delete("/manage", name="Delete an exam", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam_endp(id: int, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_role(role, "teacher")

        c.execute("DELETE FROM exams WHERE id=%s;", (id,))

        conn.commit()


@router.patch("/manage", name="Edit an exam", status_code=status.HTTP_204_NO_CONTENT)
async def edit_exam_endp(id: int | None, exam: Exam, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_role(role, "teacher")

        fields = gen.get_obj_fields(Exam)
        c.execute(
            f"SELECT {gen.format_fields_to_select_sql(fields)} FROM exams WHERE id=%s;",
            (id,),
        )
        old_data = c.fetchone()
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such exam",
            )

        new_data = gen.merge_data(Exam, old_data, exam)
        print(new_data)

        c.execute(
            f"""UPDATE "exams" SET {gen.format_fields_to_update_sql(fields)} WHERE id=%s""",
            (new_data + (id,)),
        )
        conn.commit()


@router.post("/manage", name="Create an exam", status_code=status.HTTP_204_NO_CONTENT)
async def create_exam_endp(exam: Exam, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_role(role, "teacher")
        ens.ensure_fields_nonnull(exam)

        c.execute(
            f"""INSERT INTO exams ({gen.format_fields_to_select_sql(gen.get_obj_fields(Exam))}) VALUES (%s, %s, %s, %s)""",
            (exam.title, exam.max_mark, exam.coefficient, exam.date),
        )
        conn.commit()
