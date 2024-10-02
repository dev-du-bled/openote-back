from fastapi import APIRouter, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from db import get_db_connection


class GetUserData(BaseModel):
    token: str


class UpdateUserData(BaseModel):
    token: str
    lastname: str | None
    firstname: str | None
    pronouns: str | None
    email: str | None


router = APIRouter()


@router.get("/user", name="Get user data")
async def get_user_endp(user_data: GetUserData):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        c.execute(
            """SELECT lastname, firstname, pronouns, email,role,profile_picture FROM "user" WHERE id=(SELECT associated_user FROM sessions WHERE token=%s);""",
            (user_data.token,),
        )
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
            )
        return res


@router.patch("/user", name="Update user data", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_endp(user_data: UpdateUserData):
    conn = get_db_connection()
    with conn.cursor() as c:
        print(user_data)
        c.execute(
            """SELECT associated_user FROM sessions WHERE token=%s;""",
            (user_data.token,),
        )
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failure !",
            )

        c.execute(
            """SELECT lastname,firstname,pronouns,email FROM "user" WHERE id=%s;""",
            (res[0],),
        )
        old_data = c.fetchone()

        c.execute(
            """UPDATE "user" SET lastname=%s,firstname=%s,pronouns=%s,email=%s WHERE id=%s;""",
            (
                user_data.lastname or old_data[0],
                user_data.firstname or old_data[1],
                user_data.pronouns or old_data[2],
                user_data.email or old_data[3],
                res[0],
            ),
        )

        conn.commit()
