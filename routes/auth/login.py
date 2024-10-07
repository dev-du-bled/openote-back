import hashlib as hs
from datetime import datetime as dt, timedelta as td
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db import get_db_connection


class LoginCred(BaseModel):
    email: str
    password: str


router = APIRouter()


@router.post("/login", name="Create a new session", status_code=status.HTTP_201_CREATED)
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
        expiration = now + td(days=3)

        # TODO: support extended time
        c.execute(
            """INSERT INTO sessions VALUES (%s, %s, %s, %s);""",
            (session_token, res[0], expiration, False),
        )
        conn.commit()

        c.execute("""SELECT role FROM "user" WHERE id=%s;""", (res[0],))
        role = c.fetchone()[0]

        return {
            "session_token": session_token,
            "expires_at": int(expiration.timestamp()),
            "role": role,
        }
