from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import config
import urllib

config = config.get_settings()

if config.db_backend == 'SQLITE':
    engine = create_engine(config.sqlite, connect_args={"check_same_thread": False})
else:
    CONNECTION_STRING = f"Driver={config.azure_db_driver};Server=tcp:{config.azure_db_host},1433;Database={config.azure_db_name};UID={config.azure_db_user};PWD={config.azure_db_pwd}"
    params = urllib.parse.quote(CONNECTION_STRING)
    url = "mssql+pyodbc:///?odbc_connect={0}&charset=UTF8".format(params)
    engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]
