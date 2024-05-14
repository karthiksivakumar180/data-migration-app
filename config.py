from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str
    CLIENT_ID: str
    GRANT_TYPE: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    USERNAME: str
    PASSWORD: str
    DB_USER:str
    DB_NAME:str
    DB_HOST:str
    DB_PORT:str
    DB_PASSWORD:str
    # DB_PORT:str

    class Config:
        env_file = "./.env"
settings = Settings()