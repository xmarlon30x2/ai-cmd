import os
import shutil
from unittest import IsolatedAsyncioTestCase, main

from ai_cmd.tool_packs.files_pack import FilesPack


class TestFilesPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.files_pack = FilesPack()
        self.test_dir = "test_dir"
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        try:
            os.makedirs(self.test_dir, exist_ok=True)
            with open(self.test_file, "w") as f:
                f.write("This is a test file.\n")
        except Exception as e:
            self.fail(f"setUp failed: {e}")

    async def asyncTearDown(self):
        try:
            shutil.rmtree(self.test_dir)
        except Exception as e:
            print(f"tearDown failed: {e}")

    async def test_tool_write_file(self):
        new_file = os.path.join(self.test_dir, "new_file.txt")
        content = "New content\n"
        result = await self.files_pack.tool_write(content=content, path=new_file)
        self.assertIn("message", result)
        self.assertEqual(result["message"], f"File {new_file} written successfully")
        with open(new_file, "r") as f:
            self.assertEqual(f.read(), content)

    async def test_tool_read_file(self):
        result = await self.files_pack.tool_read(path=self.test_file)
        self.assertIn("content", result)
        self.assertEqual(result["content"], "This is a test file.\n")

    async def test_tool_delete_file(self):
        result = await self.files_pack.tool_delete(path=self.test_file)
        self.assertIn("message", result)
        self.assertEqual(
            result["message"], f"File {self.test_file} deleted successfully"
        )
        self.assertFalse(os.path.exists(self.test_file))

    async def test_tool_copy_file(self):
        copy_file = os.path.join(self.test_dir, "copy_file.txt")
        result = await self.files_pack.tool_copy(
            source_path=self.test_file, destination_path=copy_file
        )
        self.assertIn("message", result)
        self.assertEqual(
            result["message"],
            f"File {self.test_file} copied to {copy_file} successfully",
        )
        self.assertTrue(os.path.exists(copy_file))
        with open(copy_file, "r") as f:
            self.assertEqual(f.read(), "This is a test file.\n")

    async def test_tool_move_file(self):
        move_file = os.path.join(self.test_dir, "move_file.txt")
        result = await self.files_pack.tool_move(
            source_path=self.test_file, destination_path=move_file
        )
        self.assertIn("message", result)
        self.assertEqual(
            result["message"],
            f"File {self.test_file} moved to {move_file} successfully",
        )
        self.assertTrue(os.path.exists(move_file))
        self.assertFalse(os.path.exists(self.test_file))
        self.test_file = move_file

    async def test_tool_get_file_size(self):
        result = await self.files_pack.tool_size(path=self.test_file)
        self.assertIn("size", result)
        self.assertIsInstance(result["size"], int)
        self.assertEqual(result["size"], os.path.getsize(self.test_file))

    async def test_tool_count_lines(self):
        result = await self.files_pack.tool_count_lines(path=self.test_file)
        self.assertIn("line_count", result)
        self.assertIsInstance(result["line_count"], int)
        self.assertEqual(result["line_count"], 1)


if __name__ == "__main__":
    main()
