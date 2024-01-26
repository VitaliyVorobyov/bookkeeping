from dataclasses import dataclass

from environs import Env


@dataclass
class Database:
    host: str
    port: int
    username: str
    password: str
    database_name: str


@dataclass
class Redis:
    url: str


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    user_id_1: int
    user_id_2: int


@dataclass
class Settings:
    bots: Bots
    database: Database
    redis: Redis


def get_settings(path: str) -> Settings:
    env = Env()
    env.read_env(path)

    try:
        bot_token = env.str('TOKEN')
        admin_id = env.int('ADMIN_ID')
        user_id_1 = env.int('USER_ID_1')
        user_id_2 = env.int('USER_ID_2')
        db_host = env.str('DB_HOST')
        db_port = env.int('DB_PORT')
        db_username = env.str('DB_USERNAME')
        db_password = env.str('DB_PASSWORD')
        db_name = env.str('DB_NAME')

        redis_url = env.str('REDIS_URL')
    except Exception as e:
        raise ValueError("Ошибка при чтении переменных окружения: " + str(e))

    return Settings(
        bots=Bots(
            bot_token=bot_token,
            admin_id=admin_id,
            user_id_1=user_id_1,
            user_id_2=user_id_2
        ),
        database=Database(
            host=db_host,
            port=db_port,
            username=db_username,
            password=db_password,
            database_name=db_name
        ),
        redis=Redis(
            url=redis_url
        )
    )


settings = get_settings('.env')
