import os
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import MagicMock

from ai_cmd.tools.tool_pack import ToolPack
from ai_cmd.tools.tools_packs.paths import PathsPack


class TestPathsPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.paths_pack = PathsPack(controller=MagicMock(), window=MagicMock())
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("test content")

    async def asyncTearDown(self):
        os.remove(self.test_file)

    async def test_is_tool_pack(self):
        self.assertIsInstance(self.paths_pack, ToolPack)

    async def test_tool_exists_true(self):
        result = await self.paths_pack.tool_exists(path=self.test_file)
        self.assertIn("exists", result)
        self.assertTrue(result["exists"])

    async def test_tool_exists_false(self):
        result = await self.paths_pack.tool_exists(path="nonexistent_file.txt")
        self.assertIn("exists", result)
        self.assertFalse(result["exists"])

    async def test_tool_creation_date(self):
        result = await self.paths_pack.tool_creation_date(path=self.test_file)
        self.assertIn("creation_time", result)
        self.assertIsInstance(result["creation_time"], float)

    async def test_tool_modification_date(self):
        result = await self.paths_pack.tool_modification_date(path=self.test_file)
        self.assertIn("modification_time", result)
        self.assertIsInstance(result["modification_time"], float)

    async def test_tool_creation_date_error(self):
        result = await self.paths_pack.tool_creation_date(path="nonexistent_file.txt")
        self.assertIn("error", result)

    async def test_tool_modification_date_error(self):
        result = await self.paths_pack.tool_modification_date(
            path="nonexistent_file.txt"
        )
        self.assertIn("error", result)


if __name__ == "__main__":
    main()
