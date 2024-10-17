from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Late(BaseModel):
    class_id: int | None
    student_id: int | None
    late: bool | None


@router.get("/lates", name="Get lates")
async def get_lates_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        fields = gen.get_obj_fields(Late)
        selected_fields = gen.format_fields_to_select_sql(fields)

        if id is None:
            c.execute(f"""SELECT {selected_fields} FROM attendance WHERE late=True;""")
            res = c.fetchall()

        else:
            c.execute(
                f"""SELECT {selected_fields} FROM attendance WHERE class_id=%s AND late=True;""",
                (id,),
            )
            res = c.fetchall()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such attendance or no attendances",
            )

        return res


@router.post("/lates", name="Mark as late", status_code=status.HTTP_204_NO_CONTENT)
async def post_lates_endp(late: Late, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        c.execute(
            """SELECT * FROM attendance WHERE class_id=%s AND student_id=%s;""",
            (late.class_id, late.student_id),
        )

        if c.fetchone() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such attendance or no attendances",
            )

        c.execute(
            """UPDATE attendance SET late=%s WHERE class_id=%s AND student_id=%s;""",
            (late.late, late.class_id, late.student_id),
        )

        conn.commit()
