from io import BytesIO

from fastapi import APIRouter, Header, Request, UploadFile, status
from PIL import Image
from psycopg2.extras import RealDictCursor

import utils.ensurances as ens
from db import Database, S3Client

router = APIRouter()
db = Database()
s3c = S3Client()

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
        buffer = BytesIO()
        img.save(buffer, filename)
        s3c.client.upload_file(filename, "user-logos", filename) # pyright:ignore

        await file.close()



        return {"url": s3c.client.generate_presigned_url(ClientMethod='get_object',Params={'Bucket': "user-logos", 'Key': filename},ExpiresIn=3600)}  #pyright:ignore
