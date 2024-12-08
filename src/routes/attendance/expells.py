from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import Database

router = APIRouter()
db = Database()


class Expell(BaseModel):
    class_id: int | None
    student_id: int | None
    expell_reason: str | None


@router.get("/expells", name="Get expells")
async def get_expell_endp(Authorization: str = Header(...), id: int | None = None):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        fields = gen.get_obj_fields(Expell)
        selected_fields = gen.format_fields_to_select_sql(fields)

        if role == ens.UserRole.student:
            c.execute(
                """
                SELECT
                  class_id,
                  expell_reason
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


@router.post("/expells", name="Add expell", status_code=status.HTTP_204_NO_CONTENT)
async def add_expell_endp(exp: Expell, Authorization: str = Header(...)):
    conn = db.get_connection()
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
            """
            UPDATE
              attendance
            SET
              expelled=True, expel_reason=%s
            WHERE
              class_id=%s AND student_id=%s;""",
            (exp.expell_reason, exp.class_id, exp.student_id),
        )

        conn.commit()
