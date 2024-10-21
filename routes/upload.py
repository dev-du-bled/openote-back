from fastapi import APIRouter, Header, status, UploadFile, Request
from psycopg2.extras import RealDictCursor
from PIL import Image
from io import BytesIO

import utils.ensurances as ens
from db import get_db_connection

router = APIRouter()


@router.post("/logo", name="Upload logo", status_code=status.HTTP_201_CREATED)
async def upload_logo_endp(
    file: UploadFile, rq: Request, Authorization: str = Header(...)
):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        _ = ens.get_role_from_token(c, Authorization)
        userid = ens.get_user_col_from_token(c, "id", Authorization)

        filename = f"storage/logos/{userid}.webp"
        byte_file = await file.read()

        img = Image.open(BytesIO(byte_file))
        img = img.resize((512, 512))
        img.save(filename)
        await file.close()

        url = f"{rq.base_url}images/logos/{userid}.webp"

        c.execute(
            """UPDATE "user" SET profile_picture=%s WHERE id=%s;""", (url, userid)
        )
        conn.commit()

        return {"url": url}
