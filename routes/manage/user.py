from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import hashlib as hs

from db import get_db_connection

router = APIRouter()


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


@router.get("/user")
async def get_user_endp(Authorization: str = Header(...), id: int | None = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        c.execute(
            """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
            (Authorization,),
        )
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )

        if res.get("role") == "admin":
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
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def post_user_endp(ud: AddUserData, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        c.execute(
            """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
            (Authorization,),
        )
        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )

        if res.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )

        try:
            query = """INSERT INTO "user" (lastname, firstname, pronouns, email, password_hash, role, profile_picture) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
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
                student_query = """INSERT INTO "student_info" (user_id, student_number, class, "group") VALUES (%s, %s, %s, %s);"""
                student_values = [user_id, ud.student_number, ud.class_, ud.group]
                c.execute(student_query, student_values)

            conn.commit()
        except errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )


@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endp(Authorization: str = Header(...), id: int = None):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        c.execute(
            """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
            (Authorization,),
        )
        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )

        if id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No user id provided"
            )

        if res.get("role") == "admin":
            c.execute("""DELETE FROM "user" WHERE id=%s;""", (id,))
            conn.commit()
            return

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )


@router.patch(
    "/user", name="Change a user info", status_code=status.HTTP_204_NO_CONTENT
)
async def update_usr_endp(
    user_data: UpdateUserData, Authorization: str = Header(...), id: int = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        print(user_data)
        c.execute(
            """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
            (Authorization,),
        )
        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
            )

        if id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No user id provided"
            )

        if res.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )

        fields = map(
            lambda n: '"' + (n[0:-1] if n[-1] == "_" else n) + '"',
            list(UpdateUserData.__fields__.keys()),
        )

        fields = list(fields)
        print(fields)

        selected_fields = ",".join(list(fields))

        # Would have been usefull if postgres allowed to edit multiple tables in one go

        # edit_fields = ",".join(
        #     list(
        #         map(
        #             lambda n: n + '"=%s',
        #             fields,
        #         )
        #     )
        # )

        c.execute(
            f"""SELECT {selected_fields} FROM "user" LEFT OUTER JOIN student_info ON student_info.user_id="user".id  WHERE "user".id=%s;""",
            (id,),
        )

        old_data = c.fetchone()

        new_data = list()

        for i, field_name in enumerate(list(fields)):
            f_name = field_name.replace('"', "")
            field_value = (
                dict(user_data)[list(UpdateUserData.__fields__.keys())[i]]
                or old_data[f_name]
            )
            new_data.append(field_value)

        new_data = tuple(new_data)
        # Thanks postgres for ruining my fun by nyot allowing me to update accross multiple table in one row
        print((new_data[2:] + (id,)))
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
