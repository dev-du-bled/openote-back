from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.ensurances as ens
from db import get_db_connection


class Element(BaseModel):
    name: str | None


router = APIRouter()


@router.get("/{type}")
async def get_collection_endp(
    Authorization: str = Header(...), type: str = None, id: int | None = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type != "class" and type != "group":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No such collection: '{type}'",
            )

        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        if id is None:
            c.execute(f"""SELECT * FROM "{type}";""")
            res = c.fetchall()
        else:
            c.execute(f"""SELECT * FROM "{type}" WHERE id=%s;""", (id,))
            res = c.fetchone()

        return res


@router.post("/{type}", status_code=status.HTTP_204_NO_CONTENT)
async def post_collection_endp(
    ce: Element, Authorization: str = Header(...), type: str = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type != "class" and type != "group":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No such collection: '{type}'",
            )

        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        try:
            c.execute(
                f"""INSERT INTO "{type}" (name) VALUES ( %s);""",
                (ce.name,),
            )
            conn.commit()

        except errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Element with name '{ce.name}' already exists",
            )


@router.delete("/{type}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_endp(
    Authorization: str = Header(...), type: str = None, id: int = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type != "class" and type != "group":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No such collection: '{type}'",
            )

        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        c.execute(f"""SELECT * FROM "{type}" WHERE id=%s;""", (id,))
        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No such element with id {id} in collection {type}",
            )

        c.execute(f"""DELETE FROM "{type}" WHERE id=%s;""", (id,))
        conn.commit()


@router.patch("/{type}", status_code=status.HTTP_204_NO_CONTENT)
async def update_collection_endp(
    pe: Element, Authorization: str = Header(...), type: str = None, id: int = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type != "class" and type != "group":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No such collection: '{type}'",
            )

        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_admin(role)

        c.execute(f"""SELECT * FROM "{type}" WHERE id=%s;""", (id,))
        res = c.fetchone()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No such element with id {id} in collection {type}",
            )

        c.execute(
            f"""UPDATE "{type}" SET name=%s WHERE id=%s;""",
            (pe.name, id),
        )
        conn.commit()
