from fastapi import FastAPI
from auth.base_config import auth_backend, fastapi_users
from auth.router import router as auth_router

from auth.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware

from user_profile.router import router as profile_router

app = FastAPI(
    title="Employee Salary App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(auth_router)
app.include_router(profile_router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT","PATCH","DELETE", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Origin", "Content-Type",
                   "Authorization", "Set-Cookie", "API-Key", "If-Modified-Since"],

)



