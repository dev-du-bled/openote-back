from fastapi import APIRouter, Header, HTTPException, status
from psycopg2.extras import RealDictCursor

from datetime import date
import utils.ensurances as ens
from db import Database

router = APIRouter()
db = Database()


BASE_STUDENT_QUERY = """
SELECT DISTINCT ON (h.id)
  h.id as homework_id,
  h.title as homework_title,
  h.due_date as homework_due_date,
  h.details as homework_details,
  u.firstname || ' ' || u.lastname AS author_name,
  s.is_done as is_done,
  (h.author = s.student) as is_author
FROM
  assigned_homework h
JOIN
  "user" u ON h.author = u.id
JOIN
  homework_status s ON s.homework = h.id
WHERE
  s.student = %s
"""

BASE_TEACHER_QUERY = """
SELECT
  h.id as homework_id,
  h.title as homework_title,
  h.due_date as homework_due_date,
  h.details as homework_details,
  u.firstname || ' ' || u.lastname AS author_name,
  c.name as class_name,
  COUNT(CASE WHEN s.is_done = true THEN 1 END) AS completed_count
FROM
  assigned_homework h
JOIN
  "user" u ON h.author = u.id
JOIN
  class c ON h.assigned_class = c.id
LEFT JOIN
  homework_status s ON s.homework = h.id
WHERE
  h.author = %s
GROUP BY
  h.id, u.firstname, u.lastname, c.name
"""


@router.get("/", name="Get homeworks")
async def get_homework_endp(
    Authorization: str = Header(...),
    id: int | None = None,
    max_homework: int | None = None,
    show_not_completed_only: bool | None = False,
    show_done_and_past_only: bool | None = False,
):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        role_id = ens.get_user_col_from_token(c, "id", Authorization)

        if id is not None and max_homework:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot provide both id and max_homework",
            )

        query = (
            BASE_STUDENT_QUERY if role == ens.UserRole.student else BASE_TEACHER_QUERY
        )

        if role == ens.UserRole.student:
            if show_not_completed_only:
                query += " AND s.is_done = false "
            if show_done_and_past_only:
                query += f" AND s.is_done = true AND h.due_date < '{date.today()}' "

        if id is not None:
            query += f"AND h.id = {id}"
        else:
            if max_homework is not None:
                query += "ORDER BY h.id, h.due_date ASC "
                query += f"LIMIT {max_homework} "

        query += ";"

        c.execute(query, (role_id,)) if role == ens.UserRole.student else c.execute(
            query, (role_id,)
        )

        res = c.fetchone() if id is not None else c.fetchall()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such homework",
            )

        return res
