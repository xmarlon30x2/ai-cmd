import os
from unittest import IsolatedAsyncioTestCase, main, skipIf
from unittest.mock import patch

from ai_cmd.packs.display_pack import DisplayPack


class TestDisplayPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.display_pack = DisplayPack()

    @skipIf(
        os.system("pip show Pillow > /dev/null 2>&1") != 0, "Pillow is not installed"
    )
    async def test_tool_capture_screen_import_error(self):
        with patch("PIL.ImageGrab.grab", new=None):
            result = await self.display_pack.tool_capture_screen(
                filename="test_screenshot.png"
            )
            self.assertIn("error", result)
            self.assertIn("PIL (Pillow) is required", result["error"])

    @skipIf(
        os.system("pip show pynput > /dev/null 2>&1") != 0, "pynput is not installed"
    )
    async def test_tool_click_import_error(self):
        with patch("pynput.mouse.Controller", new=None):
            result = await self.display_pack.tool_click(x=100, y=100)
            self.assertIn("error", result)
            self.assertIn("pynput is required", result["error"])

    @skipIf(
        os.system("pip show pynput > /dev/null 2>&1") != 0, "pynput is not installed"
    )
    async def test_tool_move_mouse_import_error(self):
        with patch("pynput.mouse.Controller", new=None):
            result = await self.display_pack.tool_move_mouse(x=100, y=100)
            self.assertIn("error", result)
            self.assertIn("pynput is required", result["error"])

    @skipIf(
        os.system("pip show pynput > /dev/null 2>&1") != 0, "pynput is not installed"
    )
    async def test_tool_write_import_error(self):
        with patch("pynput.keyboard.Controller", new=None):
            result = await self.display_pack.tool_write(text="test text")
            self.assertIn("error", result)
            self.assertIn("pynput is required", result["error"])


if __name__ == "__main__":
    main()
