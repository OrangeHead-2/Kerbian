import strawberry
from typing import List, Optional
from kerbian.db.orm import Model

def model_to_strawberry_type(model_cls):
    fields = []
    for name, field in model_cls._fields.items():
        pytype = int if "INT" in field.column_type else str
        fields.append((name, strawberry.field(type_=pytype)))
    return strawberry.type(type(model_cls.__name__, (), dict(fields)))

def make_query_type(models):
    queries = {}
    for model_cls in models:
        typ = model_to_strawberry_type(model_cls)
        @strawberry.field
        def all_items(info) -> List[typ]:
            conn = info.context["db"]
            rows = model_cls.all(conn)
            return [typ(**{k: getattr(row, k) for k in model_cls._fields}) for row in rows]
        queries[f"all_{model_cls.__name__.lower()}s"] = all_items
    return strawberry.type("Query", queries)

# Usage in FastAPI:
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter

def get_db():
    from kerbian.db.connection import DatabaseConnection
    return DatabaseConnection.get_instance("default", "sqlite", path="kerbian.db").conn

def create_graphql_app(models):
    schema = strawberry.Schema(query=make_query_type(models))
    graphql_app = GraphQLRouter(schema, context_getter=lambda req: {"db": get_db()})
    return graphql_app