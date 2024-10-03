from fastapi import APIRouter, Header, HTTPException, status
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
        if type == "class" or type == "group":
            c.execute(
                """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
                (Authorization,),
            )
            res = c.fetchone()

            if res is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No such session"
                )

            if res.get("role") == "admin" or res.get("role") == "teacher":
                if id is None:
                    c.execute(f"""SELECT * FROM "{type}";""")
                    res = c.fetchall()
                else:
                    c.execute(f"""SELECT * FROM "{type}" WHERE id=%s;""", (id,))
                    res = c.fetchone()

                if res is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail=f"No such {type}"
                    )

                return res
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not allowed to access this resource",
                )


@router.post("/{type}", status_code=status.HTTP_201_CREATED)
async def post_collection_endp(
    ce: Element, Authorization: str = Header(...), type: str = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type == "class" or type == "group":
            c.execute(
                """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
                (Authorization,),
            )
            res = c.fetchone()
            if res.get("role") == "admin" or res.get("role") == "teacher":
                c.execute(
                    f"""INSERT INTO "{type}" (name) VALUES ( %s);""",
                    (ce.name,),
                )
                conn.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not allowed to access this resource",
                )


@router.delete("/{type}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_endp(
    Authorization: str = Header(...), type: str = None, id: int = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type == "class" or type == "group":
            c.execute(
                """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
                (Authorization,),
            )
            res = c.fetchone()
            if res.get("role") == "admin" or res.get("role") == "teacher":
                c.execute(f"""DELETE FROM "{type}" WHERE id=%s;""", (id,))
                conn.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not allowed to access this resource",
                )


@router.patch("/{type}", status_code=status.HTTP_204_NO_CONTENT)
async def update_collection_endp(
    pe: Element, Authorization: str = Header(...), type: str = None, id: int = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type == "class" or type == "group":
            c.execute(
                """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
                (Authorization,),
            )
            res = c.fetchone()
            if res.get("role") == "admin" or res.get("role") == "teacher":
                c.execute(
                    f"""UPDATE "{type}" SET name=%s WHERE id=%s;""",
                    (pe.name, id),
                )
                conn.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You are not allowed to access this resource",
                )
