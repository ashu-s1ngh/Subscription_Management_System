from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = "https://placeholder.supabase.co"
    SUPABASE_KEY: str = "placeholder-anon-key"
    SUPABASE_SERVICE_ROLE_KEY: str = "placeholder-service-key"
    SUPABASE_JWT_SECRET: str = "placeholder-jwt-secret"
    ENVIRONMENT: str = "development"
    FRONTEND_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
