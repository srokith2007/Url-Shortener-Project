from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    mail_username : str
    mail_password : str
    mail_from : str
    mail_port : int
    mail_server : str
    mail_starttls : bool
    mail_ssl_tls : bool
    mail_from_name : str
    base_url : str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()