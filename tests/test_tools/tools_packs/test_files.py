import os
import shutil
from unittest import IsolatedAsyncioTestCase, main, skipIf
from unittest.mock import MagicMock

from ai_cmd.tools.tools_packs.files import FilesPack


class TestFilesPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.files_pack = FilesPack(controller=MagicMock(), window=MagicMock())
        self.test_dir = "test_dir"
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        try:
            os.makedirs(self.test_dir, exist_ok=True)
            with open(self.test_file, "w", encoding="utf-8") as f:
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
        with open(new_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), content)

    async def test_tool_read_file(self):
        result = await self.files_pack.tool_read(path=self.test_file)
        self.assertIn("content", result)
        self.assertEqual(result["content"], "This is a test file.\n")

    async def test_tool_read_file_nonexistent(self):
        nonexistent_file = os.path.join(self.test_dir, "nonexistent_file.txt")
        result = await self.files_pack.tool_read(path=nonexistent_file)
        self.assertIn("error", result)

    async def test_tool_delete_file(self):
        result = await self.files_pack.tool_delete(path=self.test_file)
        self.assertIn("message", result)
        self.assertEqual(
            result["message"], f"File {self.test_file} deleted successfully"
        )
        self.assertFalse(os.path.exists(self.test_file))

    async def test_tool_delete_file_nonexistent(self):
        nonexistent_file = os.path.join(self.test_dir, "nonexistent_file.txt")
        result = await self.files_pack.tool_delete(path=nonexistent_file)
        self.assertIn("error", result)

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
        with open(copy_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "This is a test file.\n")

    async def test_tool_copy_file_nonexistent(self):
        nonexistent_file = os.path.join(self.test_dir, "nonexistent_file.txt")
        copy_file = os.path.join(self.test_dir, "copy_file.txt")
        result = await self.files_pack.tool_copy(
            source_path=nonexistent_file, destination_path=copy_file
        )
        self.assertIn("error", result)

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

    async def test_tool_move_file_nonexistent(self):
        nonexistent_file = os.path.join(self.test_dir, "nonexistent_file.txt")
        move_file = os.path.join(self.test_dir, "move_file.txt")
        result = await self.files_pack.tool_move(
            source_path=nonexistent_file, destination_path=move_file
        )
        self.assertIn("error", result)

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

    async def test_tool_append(self):
        append_content = "This is appended content.\n"
        result = await self.files_pack.tool_append(
            path=self.test_file, content=append_content
        )
        self.assertIn("message", result)
        result_read = await self.files_pack.tool_read(path=self.test_file)
        self.assertEqual(
            result_read["content"], "This is a test file.\n" + append_content
        )

    async def test_tool_replace(self):
        old_string = "test"
        new_string = "different"
        result = await self.files_pack.tool_replace(
            path=self.test_file, old_string=old_string, new_string=new_string
        )
        self.assertIn("message", result)
        result_read = await self.files_pack.tool_read(path=self.test_file)
        self.assertEqual(result_read["content"], "This is a different file.\n")

    async def test_tool_replace_regex(self):
        content = "This is a line with a number 12345.\n"
        await self.files_pack.tool_write(path=self.test_file, content=content)
        pattern = r"\d+"
        replacement = "replacement"
        result = await self.files_pack.tool_replace_regex(
            path=self.test_file, pattern=pattern, replacement=replacement
        )
        self.assertIn("message", result)
        result_read = await self.files_pack.tool_read(path=self.test_file)
        self.assertEqual(
            result_read["content"], "This is a line with a number replacement.\n"
        )

    async def test_tool_insert_line(self):
        insert_content = "This is a new line."
        result = await self.files_pack.tool_insert_line(
            path=self.test_file, line_number=1, content=insert_content
        )
        self.assertIn("message", result)
        result_read = await self.files_pack.tool_read(path=self.test_file)
        self.assertEqual(
            result_read["content"], insert_content + "\nThis is a test file.\n"
        )

    async def test_tool_get_line(self):
        result = await self.files_pack.tool_get_line(path=self.test_file, line_number=1)
        self.assertIn("line", result)
        self.assertEqual(result["line"], "This is a test file.")

    async def test_tool_search(self):
        content = "This is a test line.\nAnother line.\nTest again.\n"
        await self.files_pack.tool_write(path=self.test_file, content=content)
        query = "test"
        result = await self.files_pack.tool_search(path=self.test_file, query=query)
        self.assertIn("lines", result)
        self.assertEqual(len(result["lines"]), 1)
        self.assertEqual(result["lines"][0]["line"], "This is a test line.")
        self.assertEqual(result["lines"][0]["line_number"], 1)

    async def test_tool_compress_decompress(self):
        archive_formats = ["zip", "tar", "gzip"]
        content = "This is a test file to compress.\n"
        await self.files_pack.tool_write(path=self.test_file, content=content)

        for archive_format in archive_formats:
            compressed_file = self.test_file + "." + archive_format
            result_compress = await self.files_pack.tool_compress(
                path=self.test_file, archive_format=archive_format
            )
            self.assertIn(
                "message", result_compress, f"Compression failed for {archive_format}"
            )
            self.assertTrue(
                os.path.exists(compressed_file),
                f"Compressed file not found for {archive_format}",
            )

            # Decompress
            # decompressed_path = self.test_dir + "/decompressed_file"
            result_decompress = await self.files_pack.tool_decompress(
                path=compressed_file, destination_path=self.test_dir
            )

            self.assertIn(
                "message",
                result_decompress,
                f"Decompression failed for {archive_format}",
            )
            decompressed_file = self.test_file
            if archive_format == "gzip":
                decompressed_file = self.test_dir + "/test_file"

            result_read = await self.files_pack.tool_read(path=decompressed_file)
            self.assertEqual(
                result_read["content"],
                content,
                f"Content mismatch for {archive_format}",
            )

            # Clean up
            os.remove(compressed_file)
            if archive_format == "gzip":
                os.remove(decompressed_file)

    async def test_tool_get_metadata(self):
        result = await self.files_pack.tool_get_metadata(path=self.test_file)
        self.assertIn("name", result)
        self.assertEqual(result["name"], "test_file.txt")
        self.assertIn("size", result)
        self.assertIn("creation_time", result)
        self.assertIn("modification_time", result)
        self.assertIn("access_time", result)
        self.assertIn("is_directory", result)
        self.assertIn("is_file", result)
        self.assertIn("is_link", result)
        self.assertEqual(result["is_file"], True)

    async def test_tool_hash(self):
        result = await self.files_pack.tool_hash(
            path=self.test_file, algorithm="sha256"
        )
        self.assertIn("hash", result)
        self.assertIsInstance(
            result["hash"],
            str,
        )

    @skipIf(
        os.system("pip show chardet > /dev/null 2>&1") != 0, "chardet is not installed"
    )
    async def test_tool_convert_encoding(self):
        content = "This is a test with some special characters: áéíóú\n"
        await self.files_pack.tool_write(
            path=self.test_file, content=content, encoding="latin-1"
        )
        result = await self.files_pack.tool_convert_encoding(
            path=self.test_file, from_encoding="latin-1", to_encoding="utf-8"
        )
        self.assertIn("message", result)
        result_read = await self.files_pack.tool_read(
            path=self.test_file, encoding="utf-8"
        )
        self.assertEqual(result_read["content"], content)


if __name__ == "__main__":
    main()
