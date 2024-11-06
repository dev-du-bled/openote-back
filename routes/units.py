from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.ensurances as ens
from db import get_db_connection


class UpdateUnit(BaseModel):
    title: str
    new_title: str


class Unit(BaseModel):
    title: str


router = APIRouter()


@router.get("/", name="List units")
async def get_units_endp(Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        _ = ens.get_role_from_token(c, Authorization)

        c.execute("SELECT * FROM units")

        res = c.fetchall()

        return res


@router.patch("/", name="Update unit", status_code=status.HTTP_204_NO_CONTENT)
async def update_unit_endp(update_data: UpdateUnit, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        c.execute(
            """UPDATE "unit" SET title=%s WHERE title=%""",
            (update_data.new_title, update_data.title),
        )

        if c.rowcount != 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such unit",
            )

        conn.commit()


@router.post("/", name="Create unit", status_code=status.HTTP_204_NO_CONTENT)
async def create_unit_endp(update_data: Unit, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        try:
            c.execute("""INSERT INTO "unit" VALUES (%s)""", (update_data.title,))
        except errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A unit with that name already exists",
            )

    conn.commit()


@router.delete("/", name="Delete unit", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit_endp(data: Unit, Authorization: str = Header(...)):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        c.execute("""DELETE FROM "unit" WHERE title=%s""", (data.title,))

    conn.commit()
