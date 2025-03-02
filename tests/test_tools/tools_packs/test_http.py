from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import MagicMock

from ai_cmd.tools.tools_packs.http import HttpPack


class TestHttpPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.http_pack = HttpPack(controller=MagicMock(), window=MagicMock())

    async def test_tool_request_get(self):
        result = await self.http_pack.tool_request(url="https://www.example.com")
        self.assertIn("status_code", result)
        self.assertEqual(result["status_code"], 200)
        self.assertIn("content", result)
        self.assertIn("<html", result["content"].lower())

    async def test_tool_request_post(self):
        result = await self.http_pack.tool_request(
            url="https://httpbin.org/post", method="post", data="{}"
        )
        self.assertIn("status_code", result)
        self.assertEqual(result["status_code"], 200)
        self.assertIn("content", result)

    async def test_tool_request_error(self):
        result = await self.http_pack.tool_request(
            url="https://www.example.com/nonexistent"
        )
        self.assertIn("error", result)

    async def test_tool_request_invalid_url(self):
        result = await self.http_pack.tool_request(url="invalid-url")
        self.assertIn("error", result)

    async def test_tool_request_timeout(self):
        result = await self.http_pack.tool_request(
            url="https://www.example.com", timeout=0.001
        )
        self.assertIn("error", result)

    async def test_tool_status(self):
        result = await self.http_pack.tool_status(url="https://www.example.com")
        self.assertIn("status_code", result)
        self.assertEqual(result["status_code"], 200)

    async def test_tool_status_error(self):
        result = await self.http_pack.tool_status(
            url="https://www.example.com/nonexistent"
        )
        self.assertIn("error", result)

    async def test_tool_status_invalid_url(self):
        result = await self.http_pack.tool_status(url="invalid-url")
        self.assertIn("error", result)


if __name__ == "__main__":
    main()
