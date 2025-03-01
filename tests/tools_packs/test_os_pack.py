from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import MagicMock

from ai_cmd.tool_packs.os_pack import OSPack


class TestOSPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.app_mock = MagicMock()
        self.os_pack = OSPack()
        await self.os_pack.bind(self.app_mock)

    async def test_tool_system_success(self):
        result = await self.os_pack.tool_system(command="echo hello world")
        self.assertEqual(result.get("returncode", None), 0)
        self.assertEqual(result.get("stdout", "").strip(), "hello world")
        self.assertEqual(result.get("stderr", None), "")

    async def test_tool_system_failure(self):
        result = await self.os_pack.tool_system(command="exit 1")
        self.assertEqual(result.get("returncode", None), 1)

    async def test_tool_system_stderr(self):
        result = await self.os_pack.tool_system(command="ls /nonexistent")
        self.assertNotEqual(result["stderr"], "")


if __name__ == "__main__":
    main()
