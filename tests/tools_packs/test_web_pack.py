import os
from unittest import IsolatedAsyncioTestCase, main, skipIf

from ai_cmd.packs.web_pack import WebPack


class TestWebPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.web_pack = WebPack()

    @skipIf(
        os.system("pip show googlesearch-python > /dev/null 2>&1") != 0,
        "googlesearch-python is not installed",
    )
    async def test_tool_google_search(self):
        result = await self.web_pack.tool_search(query="test query", num_results=1)
        self.assertIn("results", result)
        self.assertIsInstance(result["results"], list)

    @skipIf(
        os.system("pip show beautifulsoup4") != 0,
        "beautifulsoup4 is not installed",
    )
    async def test_tool_extract_links(self):
        result = await self.web_pack.tool_links(url="https://www.example.com")
        self.assertIn("links", result)
        self.assertIsInstance(result["links"], list)
        self.assertIn("https://www.iana.org/domains/example", result["links"])


if __name__ == "__main__":
    main()
