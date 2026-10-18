from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserProfileCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str


class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserProfileOut(BaseModel):
    id: int
    full_name: str
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class ResponseSchema(BaseModel):
    message: str = Field(description="Ответ пользователю")
    category: str = Field(description="Категория запроса: profile, knowledge_base, text или other")
    status: bool


class ChatSchema(BaseModel):
    question: str






