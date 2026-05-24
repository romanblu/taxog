from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    aws_region: str
    aws_profile: str | None = None
    knowledge_base_id: str
    model_arn: str
    log_level: str = "INFO"
    bedrock_max_retries: int = 5
    bedrock_timeout_s: int = 120
    
settings = Settings()