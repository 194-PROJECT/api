from datetime import datetime, time
from enum import Enum
from typing import Any, ClassVar, List, Optional, Self, Type, TypedDict
from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator, model_validator
from flask import Flask
from sqlalchemy import TextClause
from sqlalchemy.orm import DeclarativeBase

class Api:
    _instance = None
    application = Flask(__name__)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Api, cls).__new__(cls)
        return cls._instance

    @classmethod
    def route(cls, rule, **options):
        def decorator(f):
            cls._instance.app.route(rule, **options)(f)
            return f
        return decorator

"""
Query operators that can be used in the where clause for filtering results.
These operators are mapped to their respective SQL representations.
"""
class SqlOperator(str, Enum):
    EQUALS = '='
    NOT_EQUALS = '<>'
    GREATER_THAN = '>'
    LESS_THAN = '<'
    GREATER_THAN_OR_EQUAL = '>='
    LESS_THAN_OR_EQUAL = '<='
    LIKE = 'LIKE'
    NOT_LIKE = 'NOT LIKE'
    IS_NULL = 'IS NULL'
    IS_NOT_NULL = 'IS NOT NULL'

class OrderDirection(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'

typeToSqlOperator: dict[Type,list[SqlOperator]] = {
    str: [
        SqlOperator.EQUALS,
        SqlOperator.NOT_EQUALS,
        SqlOperator.LIKE,
        SqlOperator.NOT_LIKE,
        SqlOperator.IS_NULL,
        SqlOperator.IS_NOT_NULL,
    ],
    int: [
        SqlOperator.EQUALS,
        SqlOperator.NOT_EQUALS,
        SqlOperator.GREATER_THAN,
        SqlOperator.LESS_THAN,
        SqlOperator.GREATER_THAN_OR_EQUAL,
        SqlOperator.LESS_THAN_OR_EQUAL,
        SqlOperator.IS_NULL,
        SqlOperator.IS_NOT_NULL,
    ],
    float: [
        SqlOperator.EQUALS,
        SqlOperator.NOT_EQUALS,
        SqlOperator.GREATER_THAN,
        SqlOperator.LESS_THAN,
        SqlOperator.GREATER_THAN_OR_EQUAL,
        SqlOperator.LESS_THAN_OR_EQUAL,
        SqlOperator.IS_NULL,
        SqlOperator.IS_NOT_NULL,
    ],
    bool: [
        SqlOperator.EQUALS,
        SqlOperator.NOT_EQUALS,
        SqlOperator.IS_NULL,
        SqlOperator.IS_NOT_NULL,
    ],
    datetime: [
        SqlOperator.EQUALS,
        SqlOperator.NOT_EQUALS,
        SqlOperator.GREATER_THAN,
        SqlOperator.LESS_THAN,
        SqlOperator.GREATER_THAN_OR_EQUAL,
        SqlOperator.LESS_THAN_OR_EQUAL,
        SqlOperator.IS_NULL,
        SqlOperator.IS_NOT_NULL,
    ],
    time: [
        SqlOperator.EQUALS,
        SqlOperator.NOT_EQUALS,
        SqlOperator.GREATER_THAN,
        SqlOperator.LESS_THAN,
        SqlOperator.GREATER_THAN_OR_EQUAL,
        SqlOperator.LESS_THAN_OR_EQUAL,
        SqlOperator.IS_NULL,
        SqlOperator.IS_NOT_NULL,
    ]
}

class WhereClause(TypedDict):
    field: str
    operator: SqlOperator
    value: Any

"""
These are general request models that can be used for any API.
"""
class GetRequest(BaseModel):
    LIMIT_MAX_VALUE: ClassVar[int] = 1000

    id: Optional[int] = None
    limit: Optional[int] = 100
    offset: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    
    @model_validator(mode="after")
    def offset_from_page_size(self, info: ValidationInfo) -> Self:
        if not self.page or not self.page_size:
            return self

        self.limit = self.page_size
        self.offset = (self.page - 1) * self.page_size
        return self

    @field_validator("limit", mode="after")
    @classmethod
    def validate_limit(cls, value: int):
        return min([
            max([value, 0]),
            cls.LIMIT_MAX_VALUE
        ]) if value else None

    @field_validator("offset", mode="after")
    @classmethod
    def validate_offset(cls, value: int):
        return max([value, 0])

class GetModelRequest(GetRequest):
    DEFAULT_ORDER_BY: ClassVar[str] = 'id'

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    order_by: Optional[str] = DEFAULT_ORDER_BY
    order_direction: Optional[OrderDirection] = OrderDirection.ASC
    order_by_clause: Optional[TextClause] = None

    field: Optional[str] = None
    operator: Optional[SqlOperator] = None
    value: Optional[str] = None
    where_clause: Optional[TextClause] = None

    @model_validator(mode="after")
    def build_order_clause(self, info: ValidationInfo) -> Self:
        table_keys: Enum = info.context['table_keys']
        model = info.context['model']

        if not issubclass(table_keys, Enum):
            raise ValueError("The order_by context must be an Enum")

        if not issubclass(model, DeclarativeBase):
            raise ValueError("The model context must be a SingletonBase subclass")

        if self.order_by not in [field.value for field in table_keys]:
            self.order_by = self.DEFAULT_ORDER_BY

        if self.order_direction not in OrderDirection:
            self.order_direction = OrderDirection.ASC

        order_by_clause = model.__table__.c[self.order_by]
        if self.order_direction == OrderDirection.ASC:
            order_by_clause = order_by_clause.asc()
        elif self.order_direction == OrderDirection.DESC:
            order_by_clause = order_by_clause.desc()

        order_by_clause = order_by_clause.compile(
            compile_kwargs={"literal_binds": True}
        )

        self.order_by_clause = TextClause(str(order_by_clause))

        return self

    @model_validator(mode="after")
    def build_where_clause(self, info: ValidationInfo) -> Self:
        if not self.field or not self.operator or not self.value:
            return self

        key_types: dict[str, Type] = dict[str, Type](info.context['key_types'])
        
        if not isinstance(key_types, dict):
            raise ValueError("The where context must be a dictionary of field types")

        if not key_types or self.field not in key_types:
            return self

        try:
            expected_type = key_types[self.field]
            if issubclass(expected_type, (datetime, time, str)):
                self.value = f"'{self.value}'"
            else:
                self.value = expected_type(self.value)
        except (ValueError, TypeError) as e:
            print(e)
            return self

        if self.operator not in typeToSqlOperator[expected_type]:
            return self

        match self.operator:
            case SqlOperator.LIKE:
                self.where_clause = TextClause(f"{self.field} {self.operator.value} '%{self.value.replace('\'', '')}%'")
            case SqlOperator.NOT_LIKE:
                self.where_clause = TextClause(f"{self.field} {self.operator.value} '%{self.value.replace('\'', '')}%'")
            case SqlOperator.IS_NULL:
                self.where_clause = TextClause(f"{self.field} {self.operator.value}")
            case SqlOperator.IS_NOT_NULL:
                self.where_clause = TextClause(f"{self.field} {self.operator.value}")
            case _:
                self.where_clause = TextClause(f"{self.field} {self.operator.value} {self.value}")

        return self

"""
These are the functions that are use to parse and return the response data.
"""
class Response[T](BaseModel):
    data: Optional[T] = None
    message: str = 'error'
    errors: Optional[List[str]] = None

def response[T](
    message: str, code: int, data: Any = None, errors: Optional[List[str]] = None
) -> Response[T]:
    """
    Constructs a response object.

    Args:
        message (str): The message to include in the response.
        code (int): The HTTP status code for the response.
        data (Any, optional): The data to include in the response. Defaults to None.
        errors (Optional[List[str]], optional): A list of error messages. Defaults to None.

    Returns:
        Response[T]: The constructed response object.
    """
    return Response[T](
        data=data, message=message, errors=errors
    ).model_dump_json(), code
