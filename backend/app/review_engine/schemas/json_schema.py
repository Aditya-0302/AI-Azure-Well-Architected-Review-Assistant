from __future__ import annotations

from copy import deepcopy
from typing import Any, TypeVar

from pydantic import BaseModel

SchemaModel = TypeVar("SchemaModel", bound=BaseModel)


def openai_json_schema(model: type[BaseModel], *, name: str) -> dict[str, object]:
    schema = deepcopy(model.model_json_schema())
    _normalize_json_schema(schema)
    return {
        "type": "json_schema",
        "json_schema": {
            "name": name,
            "schema": schema,
            "strict": True,
        },
    }


def _normalize_json_schema(node: Any) -> None:
    if isinstance(node, dict):
        if node.get("type") == "object" or "properties" in node:
            properties = node.get("properties", {})
            if isinstance(properties, dict):
                node["additionalProperties"] = False
                node["required"] = list(properties.keys())
        for value in node.values():
            _normalize_json_schema(value)
    elif isinstance(node, list):
        for item in node:
            _normalize_json_schema(item)

