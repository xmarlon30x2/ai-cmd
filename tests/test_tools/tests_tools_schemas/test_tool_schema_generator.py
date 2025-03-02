import enum
import unittest
from typing import Any, Callable, Dict, Optional, Union

from ai_cmd.tools.schemas.generators import function_to_tool_schema


class TestToolSchemaGenerator(unittest.TestCase):

    def test_function_with_simple_arguments(self):
        def my_function(a: int, b: str) -> bool:
            """My function"""
            return True

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["name"], "my_function")
        self.assertEqual(schema["description"], "My function")
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "integer")
        self.assertEqual(schema["parameters"]["properties"]["b"]["type"], "string")
        self.assertEqual(schema["parameters"]["required"], ["a", "b"])

    def test_function_with_no_arguments(self):
        def my_function() -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["name"], "my_function")
        self.assertEqual(schema["description"], "My function")
        self.assertEqual(schema["parameters"]["properties"], {})
        self.assertEqual(schema["parameters"]["required"], [])

    def test_function_with_default_values(self):
        def my_function(a: int = 1, b: str = "hello") -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["name"], "my_function")
        self.assertEqual(schema["description"], "My function")
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "integer")
        self.assertEqual(schema["parameters"]["properties"]["b"]["type"], "string")
        self.assertEqual(schema["parameters"]["required"], [])

    def test_function_with_docstring_descriptions(self):
        def my_function(a: int, b: str) -> None:
            """My function

            Args:
                a: The first argument
                b: The second argument
            """
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["name"], "my_function")
        self.assertEqual(schema["description"], "My function")
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["description"],
            "The first argument",
        )
        self.assertEqual(
            schema["parameters"]["properties"]["b"]["description"],
            "The second argument",
        )
        self.assertEqual(schema["parameters"]["required"], ["a", "b"])

    def test_function_with_list_argument(self):
        def my_function(a: list[int]) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "array")
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["items"]["type"],
            "integer",
        )

    def test_function_with_optional_argument(self):
        def my_function(a: Optional[int]) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "integer")
        self.assertTrue(schema["parameters"]["properties"]["a"]["nullable"])

    def test_function_with_enum_argument(self):
        class MyEnum(enum.Enum):
            VALUE1 = "value1"
            VALUE2 = "value2"

        def my_function(a: MyEnum) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "string")
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["enum"],
            ["value1", "value2"],
        )

    def test_method_with_self_parameter(self):
        class MyClass:
            def my_method(self) -> None:
                """My method"""
                pass

        schema = function_to_tool_schema(MyClass().my_method)
        self.assertEqual(schema["name"], "my_method")
        self.assertEqual(schema["parameters"]["properties"], {})
        self.assertEqual(schema["parameters"]["required"], [])

    def test_function_with_bytes_argument(self):
        def my_function(a: bytes) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "string")

    def test_function_with_bytearray_argument(self):
        def my_function(a: bytearray) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "string")

    def test_function_with_memoryview_argument(self):
        def my_function(a: memoryview) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "string")

    def test_function_with_nested_list_argument(self):
        def my_function(a: list[list[int]]) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "array")
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["items"]["type"],
            "array",
        )
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["items"]["items"]["type"],
            "integer",
        )

    def test_function_with_dict_list_argument(self):
        def my_function(a: Dict[str, list[int]]) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "object")
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["additionalProperties"]["type"],
            "array",
        )
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["additionalProperties"]["items"][
                "type"
            ],
            "integer",
        )

    def test_function_with_union_argument(self):
        def my_function(a: Union[int, str]) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(len(schema["parameters"]["properties"]["a"]["oneOf"]), 2)
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["oneOf"][0]["type"],
            "integer",
        )
        self.assertEqual(
            schema["parameters"]["properties"]["a"]["oneOf"][1]["type"],
            "string",
        )

    def test_function_with_union_argument_with_none(self):
        def my_function(a: Optional[int]) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "integer")
        self.assertTrue(schema["parameters"]["properties"]["a"]["nullable"])

    def test_function_with_callable_argument(self):
        def my_function(a: Callable[[int], str]) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "string")

    def test_function_with_any_argument(self):
        def my_function(a: Any) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "string")

    def test_function_with_forward_ref_argument(self):
        class MyClass:
            pass

        def my_function(a: "MyClass") -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "string")

    def test_function_with_custom_class_argument(self):
        class MyClass:
            pass

        def my_function(a: MyClass) -> None:
            """My function"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["parameters"]["properties"]["a"]["type"], "string")

    def test_function_with_unicode_docstring(self):
        def my_function(a: int) -> None:
            """My function with ünicode"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["description"], "My function with ünicode")

    def test_function_with_special_chars_docstring(self):
        def my_function(a: int) -> None:
            """My function with !@#$%^&*()"""
            pass

        schema = function_to_tool_schema(my_function)
        self.assertEqual(schema["description"], "My function with !@#$%^&*()")


if __name__ == "__main__":
    unittest.main()
