"""Mappers"""

from typing import (Any, Callable, Dict, List, Literal, Optional, Union,
                    get_args, get_origin)


class TypeToJSONSchemaMapper:
    """Convierte tipos Python a JSON Schema con soporte para tipos complejos"""

    TYPE_MAPPING: Dict[Any, Dict[str, Any]] = {
        str: {"type": "string"},
        int: {"type": "integer"},
        float: {"type": "number"},
        bool: {"type": "boolean"},
        list: {"type": "array"},
        dict: {"type": "object"},
        type(None): {"type": "null"},
    }

    @classmethod
    def map(cls, python_type: Any) -> Dict[str, Any]:
        """Genera schema recursivo para tipos complejos"""
        origin = get_origin(python_type) or python_type
        args = get_args(python_type)
        if schema := cls.TYPE_MAPPING.get(origin):
            return schema.copy()
        handler = cls._get_type_handler(origin)
        return handler(args) if handler else {"type": "string"}

    @classmethod
    def _get_type_handler(cls, origin: Any) -> Optional[Callable[[Any], Any]]:
        handlers: Dict[Any, Callable[[Any], Any]] = {
            Union: cls._handle_union,
            Optional: cls._handle_optional,
            list: cls._handle_list,
            List: cls._handle_list,
            dict: cls._handle_dict,
            Dict: cls._handle_dict,
            Literal: cls._handle_literal,
            Any: cls._handle_any,
        }
        return handlers.get(origin, None)

    @classmethod
    def _handle_union(cls, args: tuple[Any, ...]):
        return {"anyOf": [cls.map(t) for t in args]}

    @classmethod
    def _handle_any(cls, _args: Any) -> Any:
        return {}

    @classmethod
    def _handle_optional(cls, args: tuple[Any, ...])  -> Any:
        return {"anyOf": [cls.map(args[0]), {"type": "null"}]}

    @classmethod
    def _handle_list(cls, args: tuple[Any, ...])  -> Any:
        return {"type": "array", "items": cls.map(args[0]) if args else {}}

    @classmethod
    def _handle_dict(cls, args: tuple[Any, ...])  -> Any:
        key_type = cls.map(args[0]) if args else {}
        value_type = cls.map(args[1]) if len(args) > 1 else {}
        return {
            "type": "object",
            "additionalProperties": value_type,
            "propertyNames": key_type,
        }

    @classmethod
    def _handle_literal(cls, args: tuple[Any, ...])  -> Any:
        return {"enum": list(args)}
