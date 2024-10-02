from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Auth routes
from routes.auth.login import router as auth_login_router
from routes.auth.logout import router as auth_logout_router

# Manage routes
from routes.user import router as user_router

api = FastAPI()

api.include_router(auth_login_router, prefix="/auth")
api.include_router(auth_logout_router, prefix="/auth")
api.include_router(user_router)


@api.get("/")
async def read_root():
    return RedirectResponse("https://youtu.be/LDU_Txk06tM")
