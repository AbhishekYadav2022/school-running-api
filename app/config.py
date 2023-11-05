from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    HOSTNAME: str
    PASSWORD: str
    DATABASE: str
    USERNAME: str

    class Config:
        env_file = ".env"

settings = Setting()