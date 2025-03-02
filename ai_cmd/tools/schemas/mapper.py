from typing import Any, Dict, Optional, Tuple, Union, get_args, get_origin

from ai_cmd.tools.schemas.utils import get_enum_values, typing_is_enum


class TypeToJSONSchemaMapper:
    """Converts Python types to JSON Schema with support for complex types."""

    @classmethod
    def map(cls, python_type: Any) -> Dict[str, Any]:
        """Generates a JSON schema for a given Python type."""
        origin = get_origin(python_type)
        args = get_args(python_type)

        if python_type is str:
            return {"type": "string"}
        elif python_type is int:
            return {"type": "integer"}
        elif python_type is float:
            return {"type": "number"}
        elif python_type is bool:
            return {"type": "boolean"}
        elif origin is list or origin is list:
            if args:
                item_type = args[0]
                if get_origin(item_type) is Union:
                    schemas = [cls.map(arg) for arg in get_args(item_type)]
                    return {"type": "array", "items": {"oneOf": schemas}}
                elif get_origin(item_type) is Optional or python_type is Optional:
                    schema = cls.map(item_type)
                    schema["nullable"] = True
                    return {"type": "array", "items": schema}
                else:
                    return {"type": "array", "items": cls.map(item_type)}
            else:
                return {"type": "array"}
        elif origin is tuple or origin is Tuple:
            if args:
                item_schemas = [cls.map(arg) for arg in args]
                return {
                    "type": "array",
                    "items": item_schemas,
                    "minItems": len(args),
                    "maxItems": len(args),
                }
            else:
                return {"type": "array"}
        elif origin is dict or origin is Dict:
            if len(args) == 2:
                value_type = args[1]
                value_schemas: list[dict[str, Any]] = []
                if get_origin(value_type) is Union:
                    for arg in get_args(value_type):
                        schema = cls.map(arg)
                        if arg is type(None) and "nullable" not in schema:
                            schema["nullable"] = True
                        value_schemas.append(schema)

                    if len(value_schemas) > 1:
                        additional_properties = {"oneOf": value_schemas}
                    elif value_schemas:
                        additional_properties = value_schemas[0]
                    else:
                        additional_properties = {}
                elif get_origin(value_type) is Optional or python_type is Optional:
                    schema = cls.map(value_type)
                    schema["nullable"] = True
                    additional_properties = schema
                else:
                    additional_properties = cls.map(value_type)

                return {
                    "type": "object",
                    "additionalProperties": additional_properties,
                }
            else:
                return {"type": "object"}
        elif origin is Union and type(None) in args:
            non_none_type = next((arg for arg in args if arg is not type(None)), None)
            if non_none_type:
                schema = cls.map(non_none_type)
                schema["nullable"] = True
                return schema
            else:
                return {"type": "null"}
        elif origin is Union:
            schemas = [cls.map(arg) for arg in args]
            return {"oneOf": schemas}
        elif typing_is_enum(python_type):
            return {"type": "string", "enum": get_enum_values(python_type)}
        else:
            return {"type": "string"}
