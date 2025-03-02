import unittest
from typing import Any, Dict, list
from unittest.mock import AsyncMock, MagicMock

from .tool_handler import ToolHandler
from .tool_pack import ToolPack


class TestToolPack(unittest.TestCase):

    async def test_bind(self):
        tool_pack = ToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        self.assertEqual(tool_pack.app, app)

    async def test_collect_tools(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        tool_pack = MyToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        tools = tool_pack._tools
        self.assertIn("my_tool", tools)
        self.assertEqual(len(tools), 1)
        tool = tools["my_tool"]
        self.assertIn("callable", tool)
        self.assertIn("spec", tool)

    async def test_specs(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        tool_pack = MyToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        specs = await tool_pack.specs()
        self.assertEqual(len(specs), 1)
        self.assertIn("name", specs[0]["function"])
        self.assertIn("description", specs[0]["function"])
        self.assertIn("parameters", specs[0]["function"])

    async def test_exists(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        tool_pack = MyToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        self.assertTrue(await tool_pack.exists("my_tool"))
        self.assertFalse(await tool_pack.exists("non_existent_tool"))

    async def test_execute(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        tool_pack = MyToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        tool_call = {
            "function": {"name": "my_tool", "arguments": '{"arg1": 10, "arg2": "test"}'}
        }
        result = await tool_pack.execute(tool_call)
        self.assertEqual(result, {"result": 14})

    async def test_execute_json_decode_error(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        tool_pack = MyToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        tool_call = {
            "function": {"name": "my_tool", "arguments": '{"arg1": 10, "arg2": test}'}
        }
        result = await tool_pack.execute(tool_call)
        self.assertIn("error", result)

    async def test_execute_missing_parameters(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        tool_pack = MyToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        tool_call = {"function": {"name": "my_tool", "arguments": '{"arg1": 10}'}}
        result = await tool_pack.execute(tool_call)
        self.assertIn("error", result)

    async def test_execute_tool_not_found(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                return {"result": arg1 + len(arg2)}

        tool_pack = MyToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        tool_call = {
            "function": {
                "name": "other_tool",
                "arguments": '{"arg1": 10, "arg2": "test"}',
            }
        }
        result = await tool_pack.execute(tool_call)
        self.assertIn("error", result)

    async def test_execute_exception(self):
        class MyToolPack(ToolPack):
            async def tool_my_tool(self, arg1: int, arg2: str) -> Dict[str, Any]:
                """My Tool"""
                raise ValueError("Something went wrong")

        tool_pack = MyToolPack()
        app = MagicMock()
        await tool_pack.bind(app)
        tool_call = {
            "function": {"name": "my_tool", "arguments": '{"arg1": 10, "arg2": "test"}'}
        }
        result = await tool_pack.execute(tool_call)
        self.assertIn("error", result)

    async def test_reset(self):
        tool_pack = ToolPack()
        await tool_pack.reset()
        self.assertTrue(True)  # Just to check that it runs without errors


if __name__ == "__main__":
    unittest.main()
