from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).parents[2] / ".env"

class Settings(BaseSettings):
    llm_api_key:str
    llm_model:str
    llm_base_url:str

    database_url:str

    commerce_api_base_url:str

    app_host:str
    app_port:int

    model_config  = SettingsConfigDict(env_file=ENV_FILE)

settings = Settings()

if __name__ == '__main__':
    print(settings.llm_base_url)

