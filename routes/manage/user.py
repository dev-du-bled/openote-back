from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from db import get_db_connection

router = APIRouter()


@router.get("/user")
async def get_user_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        c.execute(
            """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
            (Authorization,),
        )
        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )

        if res.get("role") == "admin":
            if id is None:
                c.execute("""SELECT * FROM "user";""")
                res = c.fetchall()
            else:
                c.execute("""SELECT * FROM "user" WHERE id=%s;""", (id,))
                res = c.fetchone()

            if res is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
                )

            return res
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )
