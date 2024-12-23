import hashlib as hs
from datetime import datetime as dt
from datetime import timedelta as td

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from db import Database


class LoginCred(BaseModel):
    email: str
    password: str
    extended_period: bool


router = APIRouter()
db = Database()


@router.post("/login", name="Login", status_code=status.HTTP_201_CREATED)
async def login_endp(creds: LoginCred):
    conn = db.get_connection()
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
        expiration = now + td(days=1 + 5 * int(creds.extended_period))

        c.execute(
            """INSERT INTO sessions VALUES (%s, %s, %s, %s);""",
            (session_token, res[0], expiration, creds.extended_period),
        )
        conn.commit()

        c.execute("""SELECT role FROM "user" WHERE id=%s;""", (res[0],))
        role = c.fetchone()[0]

        return {
            "session_token": session_token,
            "expires_at": int(expiration.timestamp()),
            "role": role,
        }
