from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from db import get_db_connection
import utils.ensurances as ens
import utils.autogen as gen

router = APIRouter()


class Attendance(BaseModel):
    class_id: int | None
    student_id: int | None
    present: bool | None
    expelled: bool | None
    expel_reason: str | None
    late: bool | None


@router.get("", name="Get attendance")
async def get_attendance_endp(Authorization: str = Header(...), id: str | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        if id is None:
            c.execute("""SELECT * FROM attendance;""")
            res = c.fetchall()

        else:
            c.execute("""SELECT * FROM attendance WHERE class_id=%s;""", (id,))
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

        c.execute(
            f"""INSERT INTO attendance ({selected_fields}) VALUES (%s, %s, %s, %s, %s, %s);""",
            (
                att.class_id,
                att.student_id,
                att.present,
                att.expelled,
                att.expel_reason,
                att.late,
            ),
        )

        conn.commit()
