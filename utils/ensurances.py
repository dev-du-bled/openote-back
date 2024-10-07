import psycopg2 as pg
from fastapi import HTTPException, status


def get_role_from_token(c, Authorization: str):
    c.execute(
        """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
        (Authorization,),
    )
    res = c.fetchone()
    if res is not None:
        return res.get("role")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such session")


def ensure_is_id_provided(c, id: int | None):
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No user id provided"
        )


def ensure_user_is_admin(role: str):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to access this resource",
        )
