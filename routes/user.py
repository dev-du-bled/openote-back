from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db import get_db_connection

class GetUserData(BaseModel):
  token: str

class UpdateUserData(BaseModel):
  token: str
  email: str
  profile_picture: str

router = APIRouter()

@router.get("/user", name="Get user data")
async def get_user_endp(user_data: GetUserData):
  conn = get_db_connection()
  with conn.cursor() as c:
    c.execute(
      """SELECT email,profile_picture FROM "user" WHERE id=(SELECT associated_user FROM sessions WHERE token=%s);""",
      (user_data.token,)
    )
    res = c.fetchone()
    if res is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
      )
    return {"email": res[0], "profile_picture": res[1]}

@router.patch("/user", name="Update user data")
async def update_user_endp(user_data: UpdateUserData):
  conn = get_db_connection()
  with conn.cursor() as c:
    c.execute(
      """SELECT associated_user FROM sessions WHERE token=%s;""",
      (user_data.token,)
    )
    res = c.fetchone()
    if res is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
      )
    c.execute(
      """UPDATE "user" SET email=%s,profile_picture=%s WHERE id=%s;""",
      (user_data.email, user_data.profile_picture, res[0])
    )
    conn.commit()
    return {"status": "success"}