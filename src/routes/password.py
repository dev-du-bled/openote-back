import hashlib as hs

from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.ensurances as ens
from db import Database


class UpdatePassword(BaseModel):
  old_password: str
  new_password: str

router = APIRouter()
db = Database()

@router.patch("/password", name="Update user password")
async def update_password_endp(data: UpdatePassword, Authorization: str = Header(...)):
  conn = db.get_connection()
  with conn.cursor(cursor_factory=RealDictCursor) as c:
    user_id = ens.get_user_col_from_token(c, "id", Authorization)

    c.execute(
      """SELECT password_hash FROM "user" WHERE id=%s;""",
      (user_id,)
    )
    res = c.fetchone()

    if res is None:
      raise HTTPException(status_code=404, detail="No such user !")

    if hs.sha256(data.old_password.encode()).hexdigest() != res["password_hash"]:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong password !",
      )

    c.execute(
      """UPDATE "user" SET password_hash=%s WHERE id=%s;""",
      (hs.sha256(data.new_password.encode()).hexdigest(), user_id)
    )
    conn.commit()