from io import BytesIO

from fastapi import APIRouter, Header, Request, UploadFile, status
from PIL import Image
from psycopg2.extras import RealDictCursor

import utils.ensurances as ens
from db import Database
from globals import Environ
from os import getenv, path

import base64

router = APIRouter()
db = Database()
env = Environ()

@router.post("/logo", name="Upload logo", status_code=status.HTTP_201_CREATED)
async def upload_logo_endp(
    file: UploadFile, rq: Request, Authorization: str = Header(...)
):
    conn = db.get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as c:
        _ = ens.get_role_from_token(c, Authorization)
        userid = ens.get_user_col_from_token(c, "id", Authorization)

        filename = f"{userid}.webp"
        byte_file = await file.read()

        img = Image.open(BytesIO(byte_file))
        img = img.resize((512, 512))

        img.save(path.join(env.logos_dir, filename))

        url = base64.b64encode(img.tobytes()).decode("utf-8")
        url = "data:image/webp;base64, " + url

        await file.close()

        return {
            "url": url
        }  # pyright:ignore
