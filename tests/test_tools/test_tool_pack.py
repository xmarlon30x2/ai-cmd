from typing import Any, Dict
from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from ai_cmd.tools.tool_pack import ToolPack
from ai_cmd.tools.types import FunctionCall, Tool, ToolCall


class TestToolPack(IsolatedAsyncioTestCase):
    async def test_collect_tools(self):

        class MyToolPack(ToolPack):
            name: str = "my_tool_pack"

            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        controller = MagicMock()
        window = MagicMock()
        tool_pack = MyToolPack(controller, window=window)
        tools = getattr(tool_pack, "_tools")
        self.assertEqual(len(tools), 1)
        tool = tools[0]
        self.assertIsInstance(tool, Tool)
        tool: Tool
        self.assertEqual(tool.function.name, "my_tool_pack_my_tool")
        self.assertEqual(tool.function.description, "My Tool")
        self.assertEqual(tool.function.callable, tool_pack.tool_my_tool)

    async def test_tools(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        controller = MagicMock()
        window = MagicMock()
        tool_pack = MyToolPack(controller, window=window)
        tools: list[Tool] = await tool_pack.tools()
        self.assertEqual(len(tools), 1)
        self.assertIsInstance(tools[0], Tool)

    async def test_exists(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        controller = MagicMock()
        window = MagicMock()
        tool_pack = MyToolPack(controller, window=window)
        self.assertTrue(await tool_pack.exists("tool_my_tool"))
        self.assertFalse(await tool_pack.exists("non_existent_tool"))

    async def test_execute(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        controller = MagicMock()
        window = MagicMock()
        tool_pack = MyToolPack(controller, window=window)
        tool_call = ToolCall(
            id="none",
            function=FunctionCall(
                name="tool_my_tool", arguments='{"arg1": 10, "arg2": "test"}'
            ),
        )
        result = await tool_pack.execute(tool_call)
        self.assertEqual(result, {"result": 14})

    async def test_execute_json_decode_error(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        controller = MagicMock()
        window = MagicMock()
        tool_pack = MyToolPack(controller, window=window)
        tool_call = ToolCall(
            id="none",
            function=FunctionCall(
                name="tool_my_tool", arguments='{"arg1": 10, "arg2": "test"'
            ),
        )
        result = await tool_pack.execute(tool_call)
        self.assertIn("error", result)

    async def test_execute_missing_parameters(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        controller = MagicMock()
        window = MagicMock()
        tool_pack = MyToolPack(controller, window=window)
        tool_call = ToolCall(
            id="none",
            function=FunctionCall(name="tool_my_tool", arguments='{"arg1": 10}'),
        )
        result = await tool_pack.execute(tool_call)
        self.assertIn("error", result)

    async def test_execute_tool_not_found(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        controller = MagicMock()
        window = MagicMock()
        tool_pack = MyToolPack(controller, window=window)
        tool_call = ToolCall(
            id="none",
            function=FunctionCall(name="tool_other_tool", arguments='{"arg1": 10}'),
        )
        result = await tool_pack.execute(tool_call)
        self.assertIn("error", result)

    async def test_execute_exception(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                raise ValueError("Something went wrong")

        controller = MagicMock()
        window = MagicMock()
        tool_pack = MyToolPack(controller, window=window)
        tool_call = ToolCall(
            id="test-id",
            function=FunctionCall(
                name="my_tool", arguments='{"arg1": 10, "arg2": "test"}'
            ),
        )
        result = await tool_pack.execute(tool_call)
        self.assertIn("error", result)

    async def test_reset_without_errors(self):
        controller = MagicMock()
        window = MagicMock()
        tool_pack = ToolPack(controller, window=window)
        await tool_pack.reset()
        self.assertTrue(True)  # Just to check that it runs without errors
