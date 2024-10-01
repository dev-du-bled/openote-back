from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db import get_db_connection

class LogoutData(BaseModel):
    token: str

router = APIRouter()

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