import os
from dotenv import load_dotenv

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# 環境変数のロード
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# mysqlのDBの設定
DATABASE = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(**dict(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    name=os.getenv('DB_NAME'),
))
ENGINE = create_engine(
    DATABASE,
    encoding = 'utf-8',
)

# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するなど。
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

# modelで使用する
Base = declarative_base()
