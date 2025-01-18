from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.ensurances as ens
from db import Database

router = APIRouter()
db = Database()


@router.get("/{type}", name="Get collection")
async def get_collection_endp(
    Authorization: str = Header(...), type: str = None, id: int | None = None
):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type != "class" and type != "group":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No such collection: '{type}'",
            )

        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_role(role, ens.UserRole.student)

        if id is None:
            c.execute(f"""SELECT * FROM "{type}";""")
            res = c.fetchall()
        else:
            c.execute(f"""SELECT * FROM "{type}" WHERE id=%s;""", (id,))
            res = c.fetchone()

        return res
