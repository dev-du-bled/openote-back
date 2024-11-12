from enum import Enum

from fastapi import HTTPException, status


class UserRole(Enum):
    parent = 0
    student = 1
    teacher = 2
    admin = 3


def get_user_col_from_token(c, col: str, Authorization: str) -> str:
    c.execute(
        f"""SELECT {col} FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
        (Authorization,),
    )
    res = c.fetchone()
    if res is not None:
        return res.get(col)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such session")


def get_role_from_token(c, Authorization: str) -> UserRole:
    return UserRole[get_user_col_from_token(c, "role", Authorization)]


def ensure_is_id_provided(c, id: int | None) -> None:
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No user id provided"
        )


def ensure_user_is_role(role: UserRole, required_role: UserRole) -> None:
    if role.value < required_role.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to access this resource",
        )


def ensure_user_is_admin(role: UserRole) -> None:
    ensure_user_is_role(role, UserRole.admin)


def ensure_given_id_is_student(c, id: int | None) -> None:
    if id is None:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user provided",
        )

    c.execute(
        """SELECT role FROM "user" WHERE id=%s;""",
        (id,),
    )

    res = c.fetchone()

    if UserRole[res.get("role")] != UserRole.student:
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
