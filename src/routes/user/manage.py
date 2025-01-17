from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import Database


class UpdateUserData(BaseModel):
    lastname: str | None
    firstname: str | None
    pronouns: str | None
    email: str | None


router = APIRouter()
db = Database()


@router.get("/", name="Get user data")
async def get_user_endp(Authorization: str = Header(...)):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        if role == "student":
            c.execute(
                """
                SELECT
                  u.lastname,
                  u.firstname,
                  u.pronouns,
                  u.email,
                  u.role,
                  u.profile_picture,
                  s.group,
                  s.class
                FROM
                  "user" u
                LEFT JOIN
                  student_info s ON u.id = s.user_id
                WHERE
                  u.id = (SELECT associated_user FROM sessions WHERE token = %s);
                """,
                (Authorization,),
            )
        else:
            c.execute(
                """
                SELECT
                  lastname, firstname, pronouns, email, role, profile_picture
                FROM
                  "user"
                WHERE
                  id=(SELECT associated_user FROM sessions WHERE token=%s);
                """,
                (Authorization,),
            )

        res = c.fetchone()
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
            )
        return res


@router.patch("/", name="Update user data", status_code=status.HTTP_204_NO_CONTENT)
async def edit_user_endp(user_data: UpdateUserData, Authorization: str = Header(...)):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        _ = ens.get_role_from_token(c, Authorization)

        fields = gen.get_obj_fields(UpdateUserData)
        selected_fields = gen.format_fields_to_select_sql(fields)

        c.execute(
            f"""
            SELECT
              {selected_fields}
            FROM
              "user"
            WHERE
              id=(SELECT associated_user FROM sessions WHERE token=%s);
            """,
            (Authorization,),
        )
        old_data = c.fetchone()
        new_data = gen.merge_data(UpdateUserData, old_data, user_data)

        c.execute(
            f"""
            UPDATE
              "user"
            SET
              {gen.format_fields_to_update_sql(fields)}
            WHERE
              id=(SELECT associated_user FROM sessions WHERE token=%s);
            """,
            (
                new_data[0],
                new_data[1],
                new_data[2],
                new_data[3],
                new_data[4],
                Authorization,
            ),
        )

        conn.commit()
