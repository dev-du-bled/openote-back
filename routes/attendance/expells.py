from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from db import get_db_connection
import utils.ensurances as ens

router = APIRouter()


@router.get("/expells", name="Get attendance")
async def get_attendance_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        if id is None:
            c.execute("""SELECT * FROM attendance WHERE expelled=True;""")
            res = c.fetchall()

        else:
            c.execute(
                """SELECT * FROM attendance WHERE class_id=%s AND expelled=True;""",
                (id,),
            )
            res = c.fetchall()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such attendance or no attendances",
            )

        return res
