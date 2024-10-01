from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.auth.login import router as auth_login_router
from routes.auth.logout import router as auth_logout_router

api = FastAPI()

api.include_router(auth_login_router, prefix="/auth")
api.include_router(auth_logout_router, prefix="/auth")

@api.get("/")
async def read_root():
    return RedirectResponse("https://youtu.be/LDU_Txk06tM")