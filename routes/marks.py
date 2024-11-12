from fastapi import APIRouter, Header, HTTPException, status
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

import utils.autogen as gen
import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


class Marks(BaseModel):
    user_id: int | None
    exam_id: int | None
    value: int | None
    unit: str | None


@router.get("", name="List marks")
async def get_mark_endp(
    Authorization: str = Header(...),
    user_id: int | None = None,
    exam_id: int | None = None,
    max_mark: int | None = None,
    start_index: int | None = None,
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        if user_id is None and exam_id is None:
            ens.ensure_user_is_role(role, ens.UserRole.student)
            role_id = ens.get_user_col_from_token(c, "id", Authorization)

            query = """
            SELECT
              m.id AS mark_id,
              m.value AS mark_value,
              e.title AS exam_title,
              e.max_mark AS exam_max_mark,
              e.coefficient AS exam_coefficient,
              e.date AS exam_date,
              e.unit AS exam_unit
            FROM
              marks m
            JOIN
              exams e ON m.exam_id = e.id
            """

            if ens.get_user_col_from_token(c, "role", Authorization) == "student":
                query += f"WHERE m.user_id = {role_id} "

            if max_mark is not None:
                query += "ORDER BY e.date ASC "
                query += f"LIMIT {max_mark} "

            if start_index is not None:
                query += f"OFFSET {start_index} "

            query += ";"

            c.execute(query)

            res = c.fetchall()

        elif user_id is not None and exam_id is not None:
            ens.ensure_user_is_role(role, ens.UserRole.teacher)
            ens.ensure_given_id_is_student(c, user_id)

            c.execute(
                """
                SELECT
                  m.id AS mark_id,
                  m.value AS mark_value,
                  e.title AS exam_title,
                  e.max_mark AS exam_max_mark,
                  e.coefficient AS exam_coefficient,
                  e.date AS exam_date,
                  e.unit AS exam_unit
                FROM
                  marks m
                JOIN
                  exams e ON m.exam_id = e.id
                WHERE
                  m.user_id = %s AND m.exam_id = %s;
                """,
                (user_id, exam_id),
            )
            res = c.fetchone()

        elif user_id is not None:
            ens.ensure_user_is_role(role, ens.UserRole.teacher)
            ens.ensure_given_id_is_student(c, user_id)

            query = """
            SELECT
              m.id AS mark_id,
              m.value AS mark_value,
              e.title AS exam_title,
              e.max_mark AS exam_max_mark,
              e.coefficient AS exam_coefficient,
              e.date AS exam_date,
              e.unit AS exam_unit
            FROM
              marks m JOIN exams e ON m.exam_id = e.id
            WHERE
              m.user_id = %s
            """

            if max_mark is not None:
                query += "ORDER BY e.date ASC "
                query += f"LIMIT {max_mark} "

            if start_index is not None:
                query += f"OFFSET {start_index} "

            query += ";"

            c.execute(query, (user_id,))

            res = c.fetchall()

        elif exam_id is not None:
            query = """
            SELECT
              m.id AS mark_id,
              m.value AS mark_value,
              e.title AS exam_title,
              e.max_mark AS exam_max_mark,
              e.coefficient AS exam_coefficient,
              e.date AS exam_date,
              e.unit AS exam_unit,
              u.firstname AS user_firstname,
              u.lastname AS user_lastname,
              s.class AS student_class,
              s.group AS student_group
            FROM
                marks m
            JOIN
                exams e ON m.exam_id = e.id
            JOIN
                student_info s ON m.user_id = s.user_id
            JOIN
                "user" u ON s.user_id = u.id
            WHERE
                m.exam_id = %s
            """

            if ens.get_role_from_token(c, Authorization) == ens.UserRole.student:
                role_id = ens.get_user_col_from_token(c, "id", Authorization)
                query += f"AND m.user_id = {role_id} "

            if max_mark is not None:
                query += "ORDER BY e.date ASC "
                query += f"LIMIT {max_mark} "

            if start_index is not None:
                query += f"OFFSET {start_index} "

            query += ";"

            c.execute(query, (exam_id,))
            res = c.fetchall()

        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such exam",
            )

        return res


@router.delete("/manage", name="Delete a mark", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mark_endp(
    user_id: int, exam_id: int, Authorization: str = Header(...)
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_role(role, ens.UserRole.teacher)

        c.execute(
            "DELETE FROM marks WHERE user_id=%s AND exam_id=%s;", (user_id, exam_id)
        )

        conn.commit()


@router.patch("/manage", name="Edit a mark", status_code=status.HTTP_204_NO_CONTENT)
async def edit_mark_endp(
    user_id: int, exam_id: int, mark: Marks, Authorization: str = Header(...)
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)

        ens.ensure_user_is_role(role, ens.UserRole.teacher)

        fields = gen.get_obj_fields(Marks)
        c.execute(
            f"""
            SELECT
              {gen.format_fields_to_select_sql(fields)}
            FROM
              marks
            WHERE
              user_id=%s AND exam_id=%s;""",
            (user_id, exam_id),
        )
        old_data = c.fetchone()
        if old_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such exam",
            )

        new_data = gen.merge_data(Marks, old_data, mark)
        print(new_data)

        c.execute(
            f"""
            UPDATE
              "marks"
            SET
              {gen.format_fields_to_update_sql(fields)}
            WHERE
              user_id=%s AND exam_id=%s;""",
            (new_data + (user_id, exam_id)),
        )
        conn.commit()


@router.post("/manage", name="Create a mark", status_code=status.HTTP_204_NO_CONTENT)
async def add_mark_endp(mark: Marks, Authorization: str = Header(...)):
    conn = get_db_connection()
    ens.ensure_fields_nonnull(mark)

    with conn.cursor(cursor_factory=RealDictCursor) as c:
        role = ens.get_role_from_token(c, Authorization)
        ens.ensure_user_is_role(role, ens.UserRole.teacher)
        ens.ensure_given_id_is_student(c, mark.user_id)  # pyright: ignore

        try:
            c.execute(
                f"""
                INSERT INTO
                  marks ({gen.format_fields_to_select_sql(gen.get_obj_fields(mark))})
                VALUES
                  (%s, %s, %s);""",
                (mark.user_id, mark.exam_id, mark.value),
            )
            conn.commit()

        except errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Mark already exists"
            )
