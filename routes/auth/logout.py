from fastapi import APIRouter, Header, status
from psycopg2.extras import RealDictCursor

import utils.ensurances as ens
from db import Database

router = APIRouter()
db = Database()


@router.post("/logout", name="Logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_endp(Authorization: str = Header(...)):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        _ = ens.get_role_from_token(c, Authorization)

        c.execute("""DELETE FROM sessions WHERE token=%s;""", (Authorization,))
        conn.commit()
