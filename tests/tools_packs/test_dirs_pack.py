import os
import shutil
from unittest import IsolatedAsyncioTestCase, main

from ai_cmd.tool_packs.dirs_pack import DirsPack


class TestDirsPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.dirs_pack = DirsPack()
        self.test_dir = "test_dir"
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        os.makedirs(self.test_dir, exist_ok=True)
        with open(self.test_file, "w") as f:
            f.write("test content")

    async def asyncTearDown(self):
        shutil.rmtree(self.test_dir)

    async def test_tool_list(self):
        result = await self.dirs_pack.tool_list(path=self.test_dir)
        self.assertIn("path", result)
        self.assertIn("elements", result)
        self.assertIsInstance(result["elements"], list)
        self.assertIn("test_file.txt", result["elements"])

    async def test_tool_create(self):
        new_dir = os.path.join(self.test_dir, "new_dir")
        result = await self.dirs_pack.tool_create(path=new_dir)
        self.assertIn("message", result)
        self.assertEqual(result["message"], f"Directory {new_dir} created successfully")
        self.assertTrue(os.path.exists(new_dir))

    async def test_tool_delete(self):
        empty_dir = os.path.join(self.test_dir, "empty_dir")
        os.makedirs(empty_dir, exist_ok=True)
        result = await self.dirs_pack.tool_delete(path=empty_dir)
        self.assertIn("message", result)
        self.assertEqual(
            result["message"], f"Directory {empty_dir} deleted successfully"
        )
        self.assertFalse(os.path.exists(empty_dir))

    async def test_tool_rename(self):
        new_name = "new_name"
        new_path = os.path.join(os.path.dirname(self.test_dir), new_name)
        result = await self.dirs_pack.tool_rename(path=self.test_dir, new_name=new_path)
        if "error" in result:
            self.fail(f"Rename failed: {result['error']}")
        self.assertIn("message", result)
        self.assertEqual(
            result["message"], f"Directory {self.test_dir} deleted successfully"
        )
        self.assertTrue(os.path.exists(new_path))
        self.assertFalse(os.path.exists(self.test_dir))
        self.test_dir = new_path

    async def test_tool_find(self):
        result = await self.dirs_pack.tool_find(path=self.test_dir, pattern="*.txt")
        self.assertIn("elements", result)
        self.assertIsInstance(result["elements"], list)
        self.assertIn(self.test_file, result["elements"])

    async def test_tool_scan(self):
        result = await self.dirs_pack.tool_scan(path=self.test_dir)
        self.assertIn("path", result)
        self.assertIn("type", result)
        self.assertEqual(result["type"], "dir")


if __name__ == "__main__":
    main()
