from datetime import datetime, time
from enum import Enum
from typing import Any, ClassVar, List, Optional, Self, Type, TypedDict, Union
from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator, model_validator
from flask import Flask, Request, json
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
    IN = 'IN'
    NOT_IN = 'NOT IN'

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
        SqlOperator.IN,
        SqlOperator.NOT_IN,
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
        SqlOperator.IN,
        SqlOperator.NOT_IN,
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
        SqlOperator.IN,
        SqlOperator.NOT_IN,
    ],
    bool: [
        SqlOperator.EQUALS,
        SqlOperator.NOT_EQUALS,
        SqlOperator.IS_NULL,
        SqlOperator.IS_NOT_NULL,
        SqlOperator.IN,
        SqlOperator.NOT_IN,
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
        SqlOperator.IN,
        SqlOperator.NOT_IN,
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
        SqlOperator.IN,
        SqlOperator.NOT_IN,
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
    limit: Optional[int] = None
    offset: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None

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
        return max([value, 0]) if value else None

    @model_validator(mode="after")
    def page_from_limit(self, info: ValidationInfo) -> Self:
        if self.page and self.page_size:
            return self

        if not self.limit or not self.offset:
            return self

        self.page = self.offset // self.limit + 1
        self.page_size = self.limit

    @model_validator(mode="after")
    def offset_from_page_size(self, info: ValidationInfo) -> Self:
        if self.limit and self.offset:
            return self

        if not self.page or not self.page_size:
            return self

        self.limit = self.page_size
        self.offset = (self.page - 1) * self.page_size
        return self

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
    value: Optional[Union[str, list[str]]] = None
    where_clause: Optional[TextClause] = None

    extra: Optional[str] = None
    
    @model_validator(mode="after")
    def parse_json_extra(self, info: ValidationInfo) -> Self:
        if self.extra:
            try:
                self.extra = json.loads(self.extra)
            except json.JSONDecodeError as e:
                print(e)
                self.extra = None

        return self

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
        model = info.context['model']

        if type(key_types) is not dict:
            raise ValueError("The order_by context must be an Enum")

        if not issubclass(model, DeclarativeBase):
            raise ValueError("The model context must be a SingletonBase subclass")
        
        if not isinstance(key_types, dict):
            raise ValueError("The where context must be a dictionary of field types")

        if not key_types or self.field not in key_types:
            return self

        try:
            expected_type = key_types[self.field]
            if issubclass(expected_type, (datetime, time, str)):
                if isinstance(self.value, list):
                    self.value = [f"'{value}'" for value in self.value]
                else:
                    self.value = f"'{self.value}'"
            elif issubclass(expected_type, bool):
                if isinstance(self.value, list):
                    self.value = [value == 'true' or self.value == '1' for value in self.value]
                else:
                    self.value = self.value == 'true' or self.value == '1'
            else:
                if isinstance(self.value, list):
                    self.value = [expected_type(value) for value in self.value]
                else:
                    self.value = expected_type(self.value)
        except (ValueError, TypeError) as e:
            print(e)
            return self

        if self.operator not in typeToSqlOperator[expected_type]:
            return self
        
        if self.operator in [SqlOperator.IN, SqlOperator.NOT_IN] and not isinstance(self.value, list):
            self.value = [self.value]

        match self.operator:
            case SqlOperator.LIKE:
                self.where_clause = TextClause(f"LOWER({model.__table__}.{self.field}) {self.operator.value} '%{self.value.replace('\'', '')}%'")
            case SqlOperator.NOT_LIKE:
                self.where_clause = TextClause(f"LOWER({model.__table__}.{self.field}) {self.operator.value} '%{self.value.replace('\'', '')}%'")
            case SqlOperator.IS_NULL:
                self.where_clause = TextClause(f"{model.__table__}.{self.field} {self.operator.value}")
            case SqlOperator.IS_NOT_NULL:
                self.where_clause = TextClause(f"{model.__table__}.{self.field} {self.operator.value}")
            case SqlOperator.IN:
                self.where_clause = TextClause(f"{model.__table__}.{self.field} {self.operator.value} ({', '.join([str(v) for v in self.value])})")
            case SqlOperator.NOT_IN:
                self.where_clause = TextClause(f"{model.__table__}.{self.field} {self.operator.value} ({', '.join([str(v) for v in self.value])})")
            case _:
                self.where_clause = TextClause(f"{model.__table__}.{self.field} {self.operator.value} {self.value}")

        return self

def flatten_request_args(request: Request) -> dict[str, Any]:
    """
    Flattens the request arguments into a single dictionary.

    Returns:
        dict: A dictionary with flattened request arguments.
    """
    return {
        key: value[0] if len(value) == 1 else value
        for key, value in request.args.to_dict(flat=False).items()
    }

"""
These are the functions that are use to parse and return the response data.
"""
class Response[T](BaseModel):
    data: Optional[T] = None
    message: str = 'error'
    errors: Optional[List[str]] = None
    page: Optional[int] = None
    total_rows: Optional[int] = None

def response[T](
    message: str,
    code: int,
    data: Any = None,
    errors: Optional[List[str]] = None,
    page: Optional[int] = None,
    total_rows: Optional[int] = None,
) -> Response[T]:
    """
    Constructs a response object.

    Args:
        message (str): The message to include in the response.
        code (int): The HTTP status code for the response.
        data (Any, optional): The data to include in the response. Defaults to None.
        errors (Optional[List[str]], optional): A list of error messages. Defaults to None.
        page (Optional[int], optional): The page number for the response. Defaults to None.
        count (Optional[int], optional): The count of the data. Defaults to None.

    Returns:
        Response[T]: The constructed response object.
    """
    return Response[T](
        data=data, message=message, errors=errors, page=page, total_rows=total_rows
    ).model_dump_json(), code
