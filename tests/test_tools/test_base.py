import unittest
from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from ai_cmd.core.history.types import ToolMessage
from ai_cmd.tools.base import Tools
from ai_cmd.tools.tool_pack import ToolPack
from ai_cmd.tools.types import FunctionCall, ToolCall


def create_cotroller():
    controller = MagicMock()
    controller.trigger = AsyncMock()
    return controller


class TestTools(IsolatedAsyncioTestCase):
    async def test_add(self):
        tools = Tools(controller=create_cotroller(), tool_packs=[])
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.name = "tool_pack1"
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_pack2.name = "tool_pack2"
        await tools.add(tool_pack1)
        await tools.add(tool_pack2)
        self.assertEqual(len(tools.tool_packs), 2)
        self.assertIn(tool_pack1, tools.tool_packs)
        self.assertIn(tool_pack2, tools.tool_packs)

    async def test_add_duplicate(self):
        tools = Tools(controller=create_cotroller(), tool_packs=[])
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.name = "tool_pack1"
        await tools.add(tool_pack1)
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_pack2.name = "tool_pack1"
        with self.assertRaises(ValueError):
            await tools.add(tool_pack2)

    async def test_remove(self):
        tools = Tools(controller=create_cotroller(), tool_packs=[])
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.name = "tool_pack1"
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_pack2.name = "tool_pack2"
        tools.tool_packs = [tool_pack1, tool_pack2]
        await tools.remove("tool_pack1")
        self.assertEqual(len(tools.tool_packs), 1)
        self.assertNotIn(tool_pack1, tools.tool_packs)
        self.assertIn(tool_pack2, tools.tool_packs)

    async def test_execute(self):
        tools = Tools(controller=create_cotroller(), tool_packs=[])
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.exists = AsyncMock(return_value=True)
        tool_pack1.execute = AsyncMock(return_value={"result": "success"})
        tool_pack1.name = "tool_pack1"

        tools.tool_packs = [tool_pack1]
        tool_call = ToolCall(
            id="none", function=FunctionCall(name="tool_pack1_my_tool", arguments="")
        )
        result = await tools.execute(tool_call)
        self.assertIsInstance(result, ToolMessage)
        self.assertEqual(result.content, '{"result": "success"}')
        tool_pack1.execute.assert_called_once_with(tool_call=tool_call)

    async def test_execute_tool_not_found(self):
        tools = Tools(controller=create_cotroller(), tool_packs=[])
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.exists = AsyncMock(return_value=False)
        tool_pack1.name = "tool_pack1"
        tools.tool_packs = [tool_pack1]
        tool_call = ToolCall(
            id="none", function=FunctionCall(name="tool_pack1_my_tool", arguments="")
        )
        result = await tools.execute(tool_call)
        self.assertIn("error", result.content)

    async def test_reset(self):
        tools = Tools(controller=create_cotroller(), tool_packs=[])
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack2 = MagicMock(spec=ToolPack)
        tools.tool_packs = [tool_pack1, tool_pack2]
        await tools.reset()
        tool_pack1.reset.assert_called_once()
        tool_pack2.reset.assert_called_once()

    async def test_list(self):
        tools = Tools(controller=create_cotroller(), tool_packs=[])
        tool_pack1 = MagicMock(spec=ToolPack)
        tool_pack1.tools = AsyncMock(return_value=[{"name": "tool1"}])
        tool_pack2 = MagicMock(spec=ToolPack)
        tool_pack2.tools = AsyncMock(return_value=[{"name": "tool2"}])
        tools.tool_packs = [tool_pack1, tool_pack2]
        list = await tools.list()
        self.assertEqual(len(list), 2)
        self.assertEqual(list[0], {"name": "tool1"})
        self.assertEqual(list[1], {"name": "tool2"})


if __name__ == "__main__":
    unittest.main()
