from psycopg2 import pool, extensions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional
from database.postgres.config import (
    POSTGRESQL_DATABASE,
    POSTGRESQL_USER,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_HOST,
    POSTGRESQL_PORT,
    DATABASE_URL,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

class PostgresDatabase:
    _instance: Optional["PostgresDatabase"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PostgresDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        dbname: Optional[str] = POSTGRESQL_DATABASE,
        user: Optional[str] = POSTGRESQL_USER,
        password: Optional[str] = POSTGRESQL_PASSWORD,
        host: Optional[str] = POSTGRESQL_HOST,
        port: Optional[str] = POSTGRESQL_PORT,
    ) -> None:
        if not hasattr(self, "initialized"):  # Ensure __init__ is only called once
            self.dbname = dbname
            self.user = user
            self.password = password
            self.host = host
            self.port = port
            self.connection_pool: pool.SimpleConnectionPool = self.initialize_pool(
                minconn=5, maxconn=1000
            )
            self.initialized = True

    def initialize_pool(self, minconn: int, maxconn: int) -> pool.SimpleConnectionPool:
        return pool.SimpleConnectionPool(
            minconn,
            maxconn,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def get_connection(self) -> extensions.connection:
        if self.connection_pool:
            return self.connection_pool.getconn()
        else:
            raise Exception("Connection pool is not initialized")

    def return_connection(self, connection) -> None:
        if self.connection_pool:
            self.connection_pool.putconn(connection)
        else:
            raise Exception("Connection pool is not initialized")

    def close_all_connections(self) -> None:
        if self.connection_pool:
            self.connection_pool.closeall()
        else:
            raise Exception("Connection pool is not initialized")
    
    @staticmethod
    def get_session():
        return session
