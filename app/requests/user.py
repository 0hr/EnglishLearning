from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    level: str

    class ConfigDict:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "Password123!",
                "level": "b1"
            }
        }

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_fields

    @classmethod
    def validate_fields(cls, values):
        for field, value in values.items():
            if not value:
                raise ValueError(f"{field} is required")
        return values

class ForgotPassword(BaseModel):
    email: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_fields

    @classmethod
    def validate_fields(cls, values):
        for field, value in values.items():
            if not value:
                raise ValueError(f"{field} is required")
        return values

class UserLogin(BaseModel):
    email: str
    password: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_fields

    @classmethod
    def validate_fields(cls, values):
        for field, value in values.items():
            if not value:
                raise ValueError(f"{field} is required")
        return values

class PasswordReset(BaseModel):
    reset_password_token: str
    password: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_fields

    @classmethod
    def validate_fields(cls, values):
        for field, value in values.items():
            if not value:
                raise ValueError(f"{field} is required")
        return values

class TokenModel(BaseModel):
    token: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_fields

    @classmethod
    def validate_fields(cls, values):
        for field, value in values.items():
            if not value:
                raise ValueError(f"{field} is required")
        return values