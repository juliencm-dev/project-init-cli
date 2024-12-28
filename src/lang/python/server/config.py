from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    FASTAPI_ENV: str 
    DEV_DATABASE_URL: str
    PROD_DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings() 


