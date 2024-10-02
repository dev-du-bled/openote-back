from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from db import get_db_connection


class CreateElement(BaseModel):
    name: str | None


router = APIRouter()


@router.get("/{type}")
async def get_collection_endp(
    authentification: str = Header(...), type: str = None, id: int | None = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type == "class" or type == "group":
            c.execute(
                """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
                (authentification,),
            )
            res = c.fetchone()
            if res.get("role") == "admin" or res.get("role") == "teacher":
                c.execute(f"""SELECT * FROM "{type}";""", (id,))

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
    ce: CreateElement, authentification: str = Header(...), type: str = None
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        if type == "class" or type == "group":
            c.execute(
                """SELECT role FROM "user" WHERE id=(SELECT associated_user FROM "sessions" WHERE token=%s);""",
                (authentification,),
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
