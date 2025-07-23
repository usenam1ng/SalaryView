from pydantic import BaseModel
from datetime import date

class SUserAdd(BaseModel):
    username: str
    password: str
    salary: int
    update_salary_at: date

class SUser(BaseModel):
    id: int
    username: str
    salary: int
    update_salary_at: date

class SUserId(BaseModel):
    ok: bool = True
    user_id: int

class SToken(BaseModel):
    access_token: str
    token_type: str = "bearer"