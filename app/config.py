
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str = "postgresql://postgres:OmLokhande2004@db:5432/postgres"
    SECRET_KEY: str = "CHANGE_THIS_TO_A_RANDOM_SECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    MODEL_PATH: str = "./model/model.pkl"
    class Config:
        env_file = ".env"
        
settings = Settings()