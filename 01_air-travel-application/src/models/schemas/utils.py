from pydantic import BaseModel, create_model
from typing import Type
from functools import lru_cache


@lru_cache(maxsize=None)
def make_update_schema(input_schema: Type[BaseModel]) -> Type[BaseModel]:
    """From https://stackoverflow.com/a/72365032"""
    fields = input_schema.__fields__
    validators = {"__validators__": input_schema.__validators__}
    optional_fields = {key: (item.type_ | None, None) for key, item in fields.items()}
    return create_model(input_schema.__name__.replace("Input", "Update"), **optional_fields, __validators__=validators)
