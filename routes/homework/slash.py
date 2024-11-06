from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor

import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


@router.get("/", name="Get homeworks")
async def get_homework_endp(
    Authorization: str = Header(...),
    id: int | None = None,
    max_homework: int | None = None,
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        role_id = ens.get_user_col_from_token(c, "id", Authorization)

        if id is not None and max_homework:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot provide both id and max_homework",
            )

        if role == ens.UserRole.teacher:
            query = """
            SELECT
              h.title as homework_title,
              h.due_date as homework_due_date,
              h.details as homework_details,
              u.firstname || ' ' || u.lastname AS author_name,
              c.name as class_name,
              COUNT(CASE WHEN s.is_done = true THEN 1 END) AS completed_count
            FROM assigned_homework h
            JOIN "user" u ON h.author = u.id
            JOIN class c ON h.assigned_class = c.id
            LEFT JOIN homework_status s ON s.homework = h.id
            GROUP BY h.id, u.firstname, u.lastname, c.name
            """

        elif role == ens.UserRole.student:
            query = """
            SELECT DISTINCT ON (h.id)
                h.title as homework_title,
                h.due_date as homework_due_date,
                h.details as homework_details,
                u.firstname || ' ' || u.lastname AS author_name,
                s.is_done as is_done
            FROM assigned_homework h
            JOIN "user" u ON h.author = u.id
            JOIN homework_status s ON s.homework = h.id
            WHERE s.student = %s
              AND h.assigned_class = (SELECT class FROM student_info WHERE user_id = %s)
            """

        if id is not None:
            query += f"AND h.id = {id}"
        else:
            if max_homework is not None:
                query += "ORDER BY h.id, h.due_date ASC "
                query += f"LIMIT {max_homework}"

        query += ";"

        c.execute(query) if id is not None else c.execute(query, (role_id, role_id))

        res = c.fetchone() if id is not None else c.fetchall()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such homework",
            )

        return res
