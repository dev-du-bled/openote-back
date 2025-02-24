from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import Database

router = APIRouter()
db = Database()


class Attendance(BaseModel):
    class_id: int | None
    student_id: int | None
    present: bool | None


@router.get("", name="Get attendance")
async def get_attendance_endp(Authorization: str = Header(...), id: str | None = None):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        fields = gen.get_obj_fields(Attendance)
        selected_fields = gen.format_fields_to_select_sql(fields)

        if role == ens.UserRole.student:
            c.execute(
                """
                SELECT
                  class_id,
                  present
                FROM
                  attendance
                WHERE
                  student_id=%s;
                """,
                (ens.get_user_col_from_token(c, "id", Authorization),),
            )
            res = c.fetchall()
        else:
            if id is None:
                c.execute(
                    f"""SELECT {selected_fields} FROM attendance WHERE present=True;"""
                )
                res = c.fetchall()

            else:
                c.execute(
                    f"""SELECT {selected_fields} FROM attendance WHERE class_id=%s AND present=True;""",
                    (id,),
                )
                res = c.fetchall()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such attendance or no attendances",
            )

        return res


@router.post("", name="Add attendance", status_code=status.HTTP_204_NO_CONTENT)
async def add_attendance_endp(att: Attendance, Authorization: str = Header(...)):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        fields = gen.get_obj_fields(Attendance)
        selected_fields = gen.format_fields_to_select_sql(fields)

        try:
            _ = ens.ensure_given_id_is_student(c, att.student_id)

            c.execute(
                f"""INSERT INTO attendance ({selected_fields}) VALUES (%s, %s, %s);""",
                (
                    att.class_id,
                    att.student_id,
                    att.present,
                ),
            )

            conn.commit()

        except errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This attendance already exists",
            )
