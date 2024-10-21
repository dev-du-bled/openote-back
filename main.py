import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from routes.attendance.expells import router as attendance_expells_router
from routes.attendance.lates import router as attendance_lates_router

# Attendance routes
from routes.attendance.slash import router as attendance_main_router

# Auth routes
from routes import upload
from routes.auth.login import router as auth_login_router
from routes.auth.logout import router as auth_logout_router

# Exam route
from routes.exam import router as exam_router
from routes.manage.collection import router as manage_collection_router

# Manage routes
from routes.manage.user import router as manage_user_router

# Marks route
from routes.marks import router as marks_router

# Planning route
from routes.planning import router as planning_router

# User route
from routes.user import router as user_router

# Upload route
from routes.upload import router as upload_router

# Static storage
from fastapi.staticfiles import StaticFiles

if not os.path.exists("storage/logos/"):
    os.mkdir("storage")
    os.mkdir("storage/logos")

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(auth_login_router, prefix="/auth")
api.include_router(auth_logout_router, prefix="/auth")

api.include_router(manage_user_router, prefix="/manage")
api.include_router(manage_collection_router, prefix="/manage")

api.include_router(attendance_main_router, prefix="/attendance")
api.include_router(attendance_expells_router, prefix="/attendance")
api.include_router(attendance_lates_router, prefix="/attendance")

api.include_router(user_router)

api.include_router(planning_router)

api.include_router(exam_router, prefix="/exam")

api.include_router(marks_router, prefix="/marks")


api.mount("/images/logos", StaticFiles(directory="storage/logos"), name="Static file storage")
api.include_router(upload_router, prefix="/upload")


@api.get("/")
async def read_root():
    return RedirectResponse("https://youtu.be/LDU_Txk06tM")
