import hashlib as hs
from datetime import datetime as dt, timedelta as td
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db import get_db_connection

class LoginCred(BaseModel):
    email: str
    password: str


class LogoutData(BaseModel):
    token: str

router = APIRouter()

@router.post("/login", name="Create a new session")
async def login_endp(creds: LoginCred):
    conn = get_db_connection()
    with conn.cursor() as c:
        c.execute(
            """SELECT id,password_hash FROM "user" WHERE email=%s;""", (creds.email,)
        )
        res = c.fetchone()
        if res is None:
            raise HTTPException(status_code=404, detail="No such user !")

        if hs.sha256(creds.password.encode()).hexdigest() != res[1]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed !",
            )

        now = dt.now()
        session_token = hs.md5((res[1] + str(now)).encode()).hexdigest()

        # TODO: support extended time
        c.execute(
            """INSERT INTO sessions VALUES (%s, %s, %s, %s);""",
            (session_token, res[0], now + td(days=3), False),
        )
        conn.commit()

        return {"session_token": session_token}


@router.post("/logout", name="End a session", status_code=status.HTTP_204_NO_CONTENT)
async def logout_endp(logout_data: LogoutData):
    conn = get_db_connection()
    with conn.cursor() as c:
        c.execute(
            """SELECT token FROM sessions WHERE token=%s;""", (logout_data.token,)
        )
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )

        c.execute("""DELETE FROM sessions WHERE token=%s;""", (logout_data.token,))
        conn.commit()