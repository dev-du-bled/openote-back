from fastapi import APIRouter, HTTPException, status, Header
from db import get_db_connection

router = APIRouter()


@router.post("/logout", name="End a session", status_code=status.HTTP_204_NO_CONTENT)
async def logout_endp(Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor() as c:
        c.execute("""SELECT token FROM sessions WHERE token=%s;""", (Authorization,))
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )

        c.execute("""DELETE FROM sessions WHERE token=%s;""", (Authorization,))
        conn.commit()
