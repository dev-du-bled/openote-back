from typing_extensions import NoReturn, NotRequired
import psycopg2 as pg
from fastapi import HTTPException, status


def get_user_col_from_token(c,col:str, Authorization: str)-> str:
    c.execute(
        f"""SELECT {col} FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
        (Authorization,),
    )
    res = c.fetchone()
    if res is not None:
        return res.get(col)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such session")

def get_role_from_token(c, Authorization: str)-> str:
   return get_user_col_from_token(c, "role", Authorization)


def ensure_is_id_provided(c, id: int | None) -> None:
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No user id provided"
        )



def ensure_user_is_role(role: str, required_role: str) -> None:
    if role != required_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to access this resource",
        )


def ensure_user_is_admin(role: str) -> None:
    ensure_user_is_role(role, "admin")


def ensure_fields_nonnull(obj_instance) -> None:
    obj_dict = dict(obj_instance)
    for key in obj_dict.keys():
        if obj_dict[key] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field '{key}' cannot be null",
            )
