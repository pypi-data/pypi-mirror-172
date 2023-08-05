import os

from sanic import Sanic
from tortoise import Tortoise, Model, fields, functions, queryset
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.manager import Manager as ModelManager
from tortoise.transactions import atomic as with_transaction, in_transaction


__all__ = (
    'Model',
    'ModelManager',
    'fields',
    'functions',
    'queryset',
    'in_transaction',
    'with_transaction',
    'init_db_connection',
    'close_db_connection',
)

def get_db_connection() -> BaseDBAsyncClient:
    return Tortoise.get_connection('default')

async def init_db_connection() -> BaseDBAsyncClient:
    application = Sanic.get_app()
    database_url = application.config.DATABASE_URL

    # Building list of blueprints with `models.py`
    # to add them into list of modules for TortoiseORM
    blueprint_models = {}
    for blueprint_name in application.blueprints:
        if os.path.exists(f'src/{blueprint_name}/models.py'):
            blueprint_models[blueprint_name] = [f'{blueprint_name}.models']

    # @TODO: Fix this ugly hack. Tortoise doesn't like empty modules so we trick it
    # empty_models: dict[str, dict] = {'models': {}}

    await Tortoise.init(db_url=database_url, modules=blueprint_models or None)  # type: ignore
    return get_db_connection()

async def close_db_connection() -> None:
    await Tortoise.close_connections()
