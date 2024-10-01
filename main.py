from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.auth import router as auth_router

api = FastAPI()

api.include_router(auth_router)

@api.get("/")
async def read_root():
    return RedirectResponse("https://youtu.be/LDU_Txk06tM")