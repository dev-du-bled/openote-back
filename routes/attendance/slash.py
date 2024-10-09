from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Attendance(BaseModel):
    class_id: int | None
    student_id: int | None
    present: bool | None


@router.get("", name="Get attendance")
async def get_attendance_endp(Authorization: str = Header(...), id: str | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        fields = gen.get_obj_fields(Attendance)
        selected_fields = gen.format_fields_to_select_sql(fields)

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


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def post_attendance_endp(att: Attendance, Authorization: str = Header(...)):
    print(att)
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        fields = gen.get_obj_fields(Attendance)
        selected_fields = gen.format_fields_to_select_sql(fields)

        try:
            c.execute(
                """SELECT * FROM student_info WHERE user_id=%s;""", (att.student_id,)
            )

            if c.fetchone() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No such student",
                )

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
