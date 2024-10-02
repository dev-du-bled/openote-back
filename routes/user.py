from fastapi import APIRouter, HTTPException, status, Header
from psycopg2.extras import RealDictCursor
from db import get_db_connection

router = APIRouter()


@router.get("/user", name="Get user data")
async def get_user_endp(authentification: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        c.execute(
            """SELECT lastname, firstname, pronouns, email,role,profile_picture FROM "user" WHERE id=(SELECT associated_user FROM sessions WHERE token=%s);""",
            (authentification,),
        )
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
            )
        return res


@router.patch("/user", name="Update user data", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_endp(
    authentification: str = Header(...),
    email: str = None,
    profile_picture: str = None,
):
    conn = get_db_connection()
    with conn.cursor() as c:
        c.execute(
            """SELECT associated_user FROM sessions WHERE token=%s;""",
            (authentification,),
        )
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )
        c.execute(
            """UPDATE "user" SET email=%s,profile_picture=%s WHERE id=%s;""",
            (email, profile_picture, res[0]),
        )
        conn.commit()


@router.get("/user/icon", name="Get icon data")
async def get_icon_endp(authentification: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if id is not None:
            c.execute(
                """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
                (authentification,),
            )
            res = c.fetchone()
            if res.get("role") == "admin" or res.get("role") == "teacher":
                c.execute(
                    """SELECT profile_picture FROM "user" WHERE id=%s;""",
                    (id,),
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not allowed to access this resource",
                )
        else:
            c.execute(
                """SELECT profile_picture FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
                (authentification,),
            )

        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
            )
        return res
