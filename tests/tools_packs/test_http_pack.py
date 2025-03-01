from unittest import IsolatedAsyncioTestCase, main

from ai_cmd.tool_packs.http_pack import HttpPack


class TestHttpPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.http_pack = HttpPack()

    async def test_tool_request_get(self):
        result = await self.http_pack.tool_request(url="https://www.example.com")
        self.assertIn("status_code", result)
        self.assertEqual(result["status_code"], 200)
        self.assertIn("content", result)
        self.assertIn("<html", result["content"].lower())

    async def test_tool_request_post(self):
        result = await self.http_pack.tool_request(url="https://httpbin.org/post", method="post", data="{}")
        self.assertIn("status_code", result)
        self.assertEqual(result["status_code"], 200)
        self.assertIn("content", result)

    async def test_tool_request_error(self):
        result = await self.http_pack.tool_request(url="https://www.example.com/nonexistent")
        self.assertIn("error", result)

    async def test_tool_status(self):
        result = await self.http_pack.tool_status(url="https://www.example.com")
        self.assertIn("status_code", result)
        self.assertEqual(result["status_code"], 200)

    async def test_tool_status_error(self):
        result = await self.http_pack.tool_status(url="https://www.example.com/nonexistent")
        self.assertIn("status_code", result)
        self.assertEqual(result["status_code"], 404)

if __name__ == '__main__':
    main()