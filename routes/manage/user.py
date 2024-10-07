from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from db import get_db_connection
import utils.ensurances as ens
import utils.autogen as gen

router = APIRouter()


class UpdateUserData(BaseModel):
    lastname: str | None
    firstname: str | None
    group: int | None
    class_: int | None
    student_number: int | None


@router.get("/user")
async def get_user_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)  # noqa: F405

        if role != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )

        if id is None:
            c.execute("""SELECT * FROM "user";""")
            res = c.fetchall()

        else:
            c.execute("""SELECT * FROM "user" WHERE id=%s;""", (id,))
            res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such user or no users",
            )

        return res


@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endp(Authorization: str = Header(...), id: int = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        ens.ensure_is_id_provided(c, id)

        c.execute("""DELETE FROM "user" WHERE id=%s;""", (id,))
        conn.commit()
        return


@router.patch(
    "/user", name="Change a user info", status_code=status.HTTP_204_NO_CONTENT
)
async def update_usr_endp(
    user_data: UpdateUserData, Authorization: str = Header(...), id: int = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)
        ens.ensure_is_id_provided(c, id)

        fields = gen.get_obj_fields(UpdateUserData)
        selected_fields = gen.format_fields_to_select_sql(fields)

        c.execute(
            f"""SELECT {selected_fields} FROM "user" LEFT OUTER JOIN student_info ON student_info.user_id="user".id  WHERE "user".id=%s;""",
            (id,),
        )

        old_data = c.fetchone()
        new_data = gen.merge_data(UpdateUserData, old_data, user_data)

        # Thanks postgres for ruining my fun by nyot allowing me to update accross multiple table in one row
        # print((new_data[2:] + (id,)))
        try:
            c.execute(
                """UPDATE "user" SET lastname=%s,firstname=%s WHERE id=%s;""",
                (new_data[0:2] + (id,)),
            )
            c.execute(
                """UPDATE "student_info" SET "group"=%s,"class"=%s,"student_number"=%s WHERE user_id=%s;""",
                (new_data[2:] + (id,)),
            )

            conn.commit()

        except errors.ForeignKeyViolation:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="No such group or class",
            )
