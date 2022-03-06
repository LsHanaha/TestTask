from pydantic import BaseSettings
from functools import lru_cache


class _Settings(BaseSettings):

    postgres_user: str = "username"
    postgres_password: str = "password"
    postgres_port: str = "5432"
    postgres_host: str = "localhost"
    postgres_database: str = "AlarTask"

    debug: bool = False

    oauth_key: str = "super_secret_key_you_even_cant_see_this"

    json_server1_port: str = "3001"
    json_server2_port: str = "3002"

    json_server_host = 'http://172.17.0.1'

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return _Settings()


settings = get_settings()
