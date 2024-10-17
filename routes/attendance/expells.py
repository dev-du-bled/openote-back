from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Expell(BaseModel):
    class_id: int | None
    student_id: int | None
    expell_reason: str | None


@router.get("/expells", name="Get expells")
async def get_expells_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        fields = gen.get_obj_fields(Expell)
        selected_fields = gen.format_fields_to_select_sql(fields)

        if id is None:
            c.execute(
                f"""SELECT {selected_fields} FROM attendance WHERE expelled=True;"""
            )
            res = c.fetchall()

        else:
            c.execute(
                f"""SELECT {selected_fields} FROM attendance WHERE class_id=%s AND expelled=True;""",
                (id,),
            )
            res = c.fetchall()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such attendance or no attendances",
            )

        return res


@router.post("/expells", status_code=status.HTTP_204_NO_CONTENT)
async def post_expells_endp(exp: Expell, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        c.execute(
            """SELECT * FROM attendance WHERE class_id=%s AND student_id=%s;""",
            (exp.class_id, exp.student_id),
        )

        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such attendance or no attendances",
            )

        if res["expelled"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Student already expelled",
            )

        c.execute(
            """UPDATE attendance SET expelled=True, expel_reason=%s WHERE class_id=%s AND student_id=%s;""",
            (exp.expel_reason, exp.class_id, exp.student_id),
        )

        conn.commit()
