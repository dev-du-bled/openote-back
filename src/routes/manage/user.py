import hashlib as hs

from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import Database

router = APIRouter()
db = Database()


class UpdateUserData(BaseModel):
    lastname: str | None
    firstname: str | None
    group: int | None
    class_: int | None
    student_number: int | None


class AddUserData(BaseModel):
    lastname: str | None
    firstname: str | None
    pronouns: str | None
    email: str | None
    password: str | None
    role: str | None
    profile_picture: str | None
    group: int | None = None
    class_: int | None = None
    student_number: int | None = None


@router.get("/user", name="Get users data")
async def get_user_endp(Authorization: str = Header(...), id: int | None = None):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

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


@router.post("/user", name="Add user", status_code=status.HTTP_201_CREATED)
async def add_user_endp(ud: AddUserData, Authorization: str = Header(...)):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_admin(role)

        try:
            query = """
            INSERT INTO
              "user" (lastname, firstname, pronouns, email, password_hash, role, profile_picture)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """

            values = [
                ud.lastname,
                ud.firstname,
                ud.pronouns,
                ud.email,
                hs.sha256(ud.password.encode()).hexdigest(),
                ud.role,
                ud.profile_picture,
            ]
            c.execute(query, values)

            user_id = c.fetchone()["id"]

            if ud.role == "student":
                student_query = """
                INSERT INTO
                  "student_info" (user_id, student_number, class, "group")
                VALUES
                  (%s, %s, %s, %s);
                """

                student_values = [user_id, ud.student_number, ud.class_, ud.group]

                c.execute(student_query, student_values)

            conn.commit()

        except errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )

        except errors.ForeignKeyViolation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such class or group",
            )


@router.delete("/user", name="Delete user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endp(Authorization: str = Header(...), id: int = None):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        ens.ensure_is_id_provided(c, id)

        c.execute("""SELECT * FROM "user" WHERE id=%s;""", (id,))
        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such user",
            )

        c.execute("""DELETE FROM "user" WHERE id=%s;""", (id,))
        conn.commit()


@router.patch("/user", name="Edit user", status_code=status.HTTP_204_NO_CONTENT)
async def edit_usr_endp(
    user_data: UpdateUserData, Authorization: str = Header(...), id: int = None
):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)
        ens.ensure_is_id_provided(c, id)

        fields = gen.get_obj_fields(UpdateUserData)
        selected_fields = gen.format_fields_to_select_sql(fields)

        c.execute(
            f"""
            SELECT
              {selected_fields}
            FROM
              "user"
            LEFT OUTER JOIN
              student_info ON student_info.user_id="user".id
            WHERE
              "user".id=%s;
            """,
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such group or class",
            )
