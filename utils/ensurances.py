import psycopg2 as pg
from fastapi import HTTPException, status


def get_role_from_token(c, Authorization: str) -> str:
    c.execute(
        """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
        (Authorization,),
    )
    res = c.fetchone()
    if res is not None:
        return res.get("role")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such session")


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


def ensure_given_id_is_student(c, id: int) -> None:
    c.execute(
        """SELECT role FROM "user" WHERE id=%s;""",
        (id,),
    )

    res = c.fetchone()

    if res.get("role") != "student":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with given ID is not a student",
        )


def ensure_fields_nonnull(obj_instance) -> None:
    obj_dict = dict(obj_instance)
    for key in obj_dict.keys():
        if obj_dict[key] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Field '{key}' cannot be null",
            )
