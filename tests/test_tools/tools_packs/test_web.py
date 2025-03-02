import os
from unittest import IsolatedAsyncioTestCase, main, skipIf
from unittest.mock import MagicMock

from ai_cmd.tools.tools_packs.web import WebPack


class TestWebPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.web_pack = WebPack(controller=MagicMock(), window=MagicMock())

    @skipIf(
        os.system("pip show googlesearch-python > /dev/null 2>&1") != 0,
        "googlesearch-python is not installed",
    )
    async def test_tool_google_search(self):
        result = await self.web_pack.tool_search(query="test query", num_results=1)
        self.assertIn("results", result)
        self.assertIsInstance(result["results"], list)

    @skipIf(
        os.system("pip show googlesearch-python > /dev/null 2>&1") != 0,
        "googlesearch-python is not installed",
    )
    async def test_tool_google_search_invalid_query(self):
        result = await self.web_pack.tool_search(query="", num_results=1)
        self.assertIn("results", result)

    @skipIf(
        os.system("pip show beautifulsoup4 > /dev/null 2>&1") != 0,
        "beautifulsoup4 is not installed",
    )
    async def test_tool_extract_links(self):
        result = await self.web_pack.tool_links(url="https://www.example.com")
        self.assertIn("links", result)
        self.assertIsInstance(result["links"], list)
        self.assertIn("https://www.iana.org/domains/example", result["links"])

    @skipIf(
        os.system("pip show beautifulsoup4 > /dev/null 2>&1") != 0,
        "beautifulsoup4 is not installed",
    )
    async def test_tool_extract_links_invalid_url(self):
        result = await self.web_pack.tool_links(url="invalid-url")
        self.assertIn("error", result)

    @skipIf(
        os.system("pip show beautifulsoup4 > /dev/null 2>&1") != 0,
        "beautifulsoup4 is not installed",
    )
    async def test_tool_extract_links_nonexistent_url(self):
        result = await self.web_pack.tool_links(
            url="https://www.example.com/nonexistent"
        )
        self.assertIn("error", result)


if __name__ == "__main__":
    main()
