from io import BytesIO

from fastapi import APIRouter, Header, Request, UploadFile, status
from PIL import Image
from psycopg2.extras import RealDictCursor

import utils.ensurances as ens
from db import Database

router = APIRouter()
db = Database()


@router.post("/logo", name="Upload logo", status_code=status.HTTP_201_CREATED)
async def upload_logo_endp(
    file: UploadFile, rq: Request, Authorization: str = Header(...)
):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        _ = ens.get_role_from_token(c, Authorization)
        userid = ens.get_user_col_from_token(c, "id", Authorization)

        # TODO: Replace local file storage with s3, probably minio?
        filename = f"/app/storage/logos/{userid}.webp"
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
