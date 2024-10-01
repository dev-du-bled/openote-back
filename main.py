import hashlib as hs
import sys
from datetime import datetime as dt
from datetime import timedelta as td

import psycopg2 as pg
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel


class LoginCred(BaseModel):
    email: str
    password: str


class LogoutData(BaseModel):
    token: str


api = FastAPI()

try:
    conn = pg.connect(
        "dbname='openote' user='openuser' host='localhost' password='openpass'"
    )
except:
    print("Unable to start API, connecting to the DB failed !")
    sys.exit(1)


@api.get("/")
async def read_root():
    return RedirectResponse("https://youtu.be/LDU_Txk06tM")


@api.post("/login", name="Create a new session")
async def login_endp(creds: LoginCred):
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


@api.post("/logout", name="End a session", status_code=status.HTTP_204_NO_CONTENT)
async def logout_endp(logout_data: LogoutData):
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
