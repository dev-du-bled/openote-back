from fastapi import APIRouter, Header, HTTPException, status
import utils.ensurances as ens
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
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

        if role != "admin" and role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )

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

        if role != "admin" and role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )

        c.execute(
            f"""INSERT INTO "{type}" (name) VALUES ( %s);""",
            (ce.name,),
        )
        conn.commit()


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
        if role != "admin" and role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
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
        if role != "admin" and "role" != "teacher":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not allowed to access this resource",
            )

        c.execute(
            f"""UPDATE "{type}" SET name=%s WHERE id=%s;""",
            (pe.name, id),
        )
        conn.commit()
