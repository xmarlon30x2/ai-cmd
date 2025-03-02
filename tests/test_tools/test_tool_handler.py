import unittest
from typing import list
from unittest.mock import AsyncMock, MagicMock

from .tool_handler import ToolHandler
from .tool_pack import ToolPack


class TestToolHandler(unittest.TestCase):

    async def test_bind(self):
        tool_handler = ToolHandler()
        app = MagicMock()
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_handler._tool_packs = [tool_pack1, tool_pack2]
        await tool_handler.bind(app)
        self.assertEqual(tool_handler.app, app)
        tool_pack1.bind.assert_called_once_with(app)
        tool_pack2.bind.assert_called_once_with(app)

    async def test_add(self):
        tool_handler = ToolHandler()
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.name = "tool_pack1"
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_pack2.name = "tool_pack2"
        await tool_handler.add([tool_pack1, tool_pack2])
        self.assertEqual(len(tool_handler._tool_packs), 2)
        self.assertIn(tool_pack1, tool_handler._tool_packs)
        self.assertIn(tool_pack2, tool_handler._tool_packs)

    async def test_add_duplicate(self):
        tool_handler = ToolHandler()
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.name = "tool_pack1"
        await tool_handler.add([tool_pack1])
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_pack2.name = "tool_pack1"
        with self.assertRaises(ValueError):
            await tool_handler.add([tool_pack2])

    async def test_remove(self):
        tool_handler = ToolHandler()
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.name = "tool_pack1"
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_pack2.name = "tool_pack2"
        tool_handler._tool_packs = [tool_pack1, tool_pack2]
        await tool_handler.remove("tool_pack1")
        self.assertEqual(len(tool_handler._tool_packs), 1)
        self.assertNotIn(tool_pack1, tool_handler._tool_packs)
        self.assertIn(tool_pack2, tool_handler._tool_packs)

    async def test_execute(self):
        tool_handler = ToolHandler()
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.exists = AsyncMock(return_value=True)
        tool_pack1.execute = AsyncMock(return_value={"result": "success"})
        tool_pack1.name = "tool_pack1"

        tool_handler._tool_packs = [tool_pack1]
        tool_call = {"function": {"name": "my_tool"}}
        result = await tool_handler.execute(tool_call)
        self.assertEqual(result, {"result": "success"})
        tool_pack1.execute.assert_called_once_with(tool_call)

    async def test_execute_tool_not_found(self):
        tool_handler = ToolHandler()
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.exists = AsyncMock(return_value=False)
        tool_pack1.name = "tool_pack1"
        tool_handler._tool_packs = [tool_pack1]
        tool_call = {"function": {"name": "my_tool"}}
        result = await tool_handler.execute(tool_call)
        self.assertIn("error", result)

    async def test_reset(self):
        tool_handler = ToolHandler()
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_handler._tool_packs = [tool_pack1, tool_pack2]
        await tool_handler.reset()
        tool_pack1.reset.assert_called_once()
        tool_pack2.reset.assert_called_once()

    async def test_specs(self):
        tool_handler = ToolHandler()
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.specs = AsyncMock(return_value=[{"name": "tool1"}])
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_pack2.specs = AsyncMock(return_value=[{"name": "tool2"}])
        tool_handler._tool_packs = [tool_pack1, tool_pack2]
        specs = await tool_handler.specs()
        self.assertEqual(len(specs), 2)
        self.assertEqual(specs[0], {"name": "tool1"})
        self.assertEqual(specs[1], {"name": "tool2"})


if __name__ == "__main__":
    unittest.main()
