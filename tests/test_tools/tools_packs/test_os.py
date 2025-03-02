from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import MagicMock

from ai_cmd.tools.tool_pack import ToolPack
from ai_cmd.tools.tools_packs.os import OSPack


class TestOSPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.os_pack = OSPack(controller=MagicMock(), window=MagicMock())

    async def test_is_tool_pack(self):
        self.assertIsInstance(self.os_pack, ToolPack)

    async def test_tool_shell_success(self):
        result = await self.os_pack.tool_shell(command="echo hello world")
        self.assertEqual(result.get("returncode", None), 0)
        self.assertEqual(result.get("stdout", "").strip(), "hello world")
        self.assertEqual(result.get("stderr", None), "")

    async def test_tool_shell_failure(self):
        result = await self.os_pack.tool_shell(command="exits 1")
        self.assertEqual(result.get("returncode", None), 1)

    async def test_tool_system_stderr(self):
        result = await self.os_pack.tool_shell(command="ls /nonexistent")
        self.assertNotEqual(result["stderr"], "")


if __name__ == "__main__":
    main()
