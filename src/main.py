import os
import logging

from globals import Environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


from routes.attendance.expells import router as attendance_expells_router
from routes.attendance.lates import router as attendance_lates_router

# Attendance routes
from routes.attendance.slash import router as attendance_main_router

# Auth routes
from routes.auth.login import router as auth_login_router
from routes.auth.logout import router as auth_logout_router

# Exam route
from routes.exam import router as exam_router
from routes.manage.collection import router as manage_collection_router

# Marks route
from routes.marks import router as marks_router

# Manage routes
from routes.manage.user import router as manage_user_router

# Homework routes
from routes.homework.slash import router as homework_main_router

from routes.homework.manage import router as homework_manage_router
from routes.homework.status import router as homework_status_router

# Planning route
from routes.planning import router as planning_router

# User route
from routes.user.manage import router as user_router
from routes.user.email import router as email_router
from routes.user.password import router as password_router

from routes.collection import router as collection_router

# Units route
from routes.units import router as units_router

# Upload route
from routes.upload import router as upload_router

log = logging.getLogger("uvicorn.error")
log.setLevel(logging.DEBUG)
env = Environ()

if not os.path.exists(env.logos_dir):
    os.makedirs(env.logos_dir, 766)
    log.info("Created logo storage")

api = FastAPI(root_path="/api/v1")


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

api.include_router(user_router, prefix="/user")
api.include_router(email_router, prefix="/user")
api.include_router(password_router, prefix="/user")

api.include_router(planning_router)

api.include_router(exam_router, prefix="/exam")

api.include_router(marks_router, prefix="/marks")

api.include_router(units_router, prefix="/units")

api.include_router(collection_router, prefix="/collection")

api.include_router(homework_main_router, prefix="/homework")
api.include_router(homework_manage_router, prefix="/homework")
api.include_router(homework_status_router, prefix="/homework")

api.include_router(upload_router, prefix="/upload")


@api.get("/")
async def read_root():
    return RedirectResponse("https://youtu.be/LDU_Txk06tM")
