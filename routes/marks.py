from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Marks(BaseModel):
    user_id: int | None
    exam_id: int | None
    value: int | None


@router.get("", name="List marks")
async def get_marks_endp(
    Authorization: str = Header(...),
    user_id: int | None = None,
    exam_id: int | None = None,
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        _ = ens.get_role_from_token(c, Authorization)

        fields = gen.get_obj_fields(Marks)
        selected_fields = gen.format_fields_to_select_sql(fields)

        if user_id is None and exam_id is None:
            c.execute(f"""SELECT {selected_fields} FROM marks;""")
            res = c.fetchall()

        elif user_id is not None and exam_id is not None:
            ens.ensure_given_id_is_student(c, user_id)

            c.execute(
                f"""SELECT {selected_fields} FROM marks WHERE user_id=%s AND exam_id=%s;""",
                (user_id, exam_id),
            )
            res = c.fetchone()

        elif user_id is not None:
            ens.ensure_given_id_is_student(c, user_id)

            c.execute(
                f"""SELECT {selected_fields} FROM marks WHERE user_id=%s;""",
                (user_id,),
            )
            res = c.fetchall()

        elif exam_id is not None:
            c.execute(
                f"""SELECT {selected_fields} FROM marks WHERE exam_id=%s;""",
                (exam_id,),
            )
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


@router.delete("/manage", name="Delete a mark", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mark_endp(
    user_id: int, exam_id: int, Authorization: str = Header(...)
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_role(role, ens.UserRole.teacher)

        c.execute(
            "DELETE FROM marks WHERE user_id=%s AND exam_id=%s;", (user_id, exam_id)
        )

        conn.commit()


@router.patch("/manage", name="Edit a mark", status_code=status.HTTP_204_NO_CONTENT)
async def edit_mark_endp(
    user_id: int, exam_id: int, mark: Marks, Authorization: str = Header(...)
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_role(role, ens.UserRole.teacher)

        fields = gen.get_obj_fields(Marks)
        c.execute(
            f"SELECT {gen.format_fields_to_select_sql(fields)} FROM marks WHERE user_id=%s AND exam_id=%s;",
            (user_id, exam_id),
        )
        old_data = c.fetchone()
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such exam",
            )

        new_data = gen.merge_objects(old_data, mark)
        print(new_data)

        c.execute(
            f"""UPDATE "marks" SET {gen.format_fields_to_update_sql(fields)} WHERE user_id=%s AND exam_id=%s;""",
            (new_data["user_id"], new_data["exam_id"], new_data["value"]),
        )
        conn.commit()


@router.post("/manage", name="Create a mark", status_code=status.HTTP_204_NO_CONTENT)
async def create_mark_endp(mark: Marks, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_role(role, "teacher")
        ens.ensure_given_id_is_student(c, mark.user_id)
        ens.ensure_fields_nonnull(mark)

        c.execute(
            f"""INSERT INTO marks ({gen.format_fields_to_select_sql(gen.get_obj_fields(mark))}) VALUES (%s, %s, %s);""",
            (mark.user_id, mark.exam_id, mark.value),
        )
        conn.commit()
