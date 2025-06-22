from pydantic import BaseModel

class UserPydanticModel(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"