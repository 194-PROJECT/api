from typing import Optional, List, Any
from database.postgres.database import PostgresDatabase

class QueryExecutor:
    db = PostgresDatabase()
    
    @staticmethod
    def fetch_all(query: str, params: Optional[List[Any]] = None) -> Optional[List[Any]]:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return QueryExecutor.__parse_results_many(cursor, result)
        finally:
            conn.close()

    @staticmethod
    def fetch_many(query: str, size: int, params: Optional[List[Any]] = None) -> Optional[List[Any]]:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchmany(size)
                return QueryExecutor.__parse_results_many(cursor, result)
        finally:
            conn.close()

    @staticmethod
    def fetch_one(query: str, params: Optional[List[Any]] = None) -> Optional[Any]:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return QueryExecutor.__parse_result(cursor, result)
        finally:
            conn.close()

    @staticmethod       
    def insert_one(query: str, params: Optional[List[Any]] = None) -> Optional[Any]:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description is not None:
                    result = cursor.fetchone()
                else:
                    result = None
                conn.commit()
                return QueryExecutor.__parse_result(cursor, result)
        finally:
            conn.close()

    @staticmethod
    def insert_many(query: str, params: Optional[List[Any]] = None) -> Optional[List[Any]]:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                conn.commit()
                return QueryExecutor.__parse_results_many(cursor, result)
        finally:
            conn.close()

    @staticmethod
    def update_one(query: str, params: Optional[List[Any]] = None) -> Optional[List[Any]]:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                conn.commit()
                return QueryExecutor.__parse_result(cursor, result)
        finally:
            conn.close()

    @staticmethod
    def update_many(query: str, params: Optional[List[Any]] = None) -> Optional[List[Any]]:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                conn.commit()
                return QueryExecutor.__parse_results_many(cursor, result)
        finally:
            conn.close()

    @staticmethod
    def delete_one(query: str, params: Optional[List[Any]] = None) -> None:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete_many(query: str, params: Optional[List[Any]] = None) -> None:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def execute(query: str, params: Optional[List[Any]] = None) -> None:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def count(query: str, params: Optional[List[Any]] = None) -> int:
        conn = QueryExecutor.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        finally:
            conn.close()

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
