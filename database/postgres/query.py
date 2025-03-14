from typing import Optional, List, Any
from database.postgres.database import PostgresDatabase

class QueryExecutor:
    db = PostgresDatabase()
    
    @staticmethod
    def fetch_all(query: str, params: Optional[List[Any]] = None) -> Optional[List[Any]]:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return QueryExecutor.__parse_results_many(cursor, result)

    @staticmethod
    def fetch_many(query: str, size: int, params: Optional[List[Any]] = None) -> Optional[List[Any]]:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchmany(size)
                return QueryExecutor.__parse_results_many(cursor, result)

    @staticmethod
    def fetch_one(
        query: str, params: Optional[List[Any]] = None
    ) -> Optional[Any]:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return QueryExecutor.__parse_result(cursor, result)

    @staticmethod       
    def insert_one(
        query: str, params: Optional[List[Any]] = None
    ) -> Optional[Any]:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description is not None:
                    result = cursor.fetchone()
                else:
                    result = None
                return QueryExecutor.__parse_result(cursor, result)

    def insert_many(
        query: str, params: Optional[List[Any]] = None
    ) -> Optional[List[Any]]:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return QueryExecutor.__parse_results_many(cursor, result)

    def update_one(
        query: str, params: Optional[List[Any]] = None
    ) -> Optional[List[Any]]:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return QueryExecutor.__parse_result(cursor, result)

    def update_many(
        query: str, params: Optional[List[Any]] = None
    ) -> Optional[List[Any]]:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return QueryExecutor.__parse_results_many(cursor, result)

    def delete_one(
        query: str, params: Optional[List[Any]] = None
    ) -> None:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)

    def delete_many(
        query: str, params: Optional[List[Any]] = None
    ) -> None:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)

    @staticmethod
    def execute(query: str, params: Optional[List[Any]] = None) -> None:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)

    @staticmethod
    def count(query: str, params: Optional[List[Any]] = None) -> int:
        with QueryExecutor.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount

    @staticmethod
    def __parse_result(cursor, result):
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None

    @staticmethod
    def __parse_results_many(cursor, results):
        if results:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, result)) for result in results]
