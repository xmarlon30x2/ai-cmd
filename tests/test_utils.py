from unittest.async_case import IsolatedAsyncioTestCase

from ai_cmd.utils import load_safe_json, wrapped_sync


class TestToolPack(IsolatedAsyncioTestCase):
    async def test_wrapped_sync_with_async_function(self):
        async def async_function(a: int, b: int):
            return a + b

        result = await wrapped_sync(async_function, 1, 2)
        self.assertEqual(result, 3)

    async def test_wrapped_sync_with_sync_function(self):
        def async_function(a: int, b: int):
            return a + b

        result = await wrapped_sync(async_function, 1, 2)
        self.assertEqual(result, 3)

    async def test_load_safe_json_with_valid_json(self):
        json = '{"data":true}'
        expect = {"data": True}
        result = load_safe_json(json)
        self.assertEqual(result, expect)

    async def test_load_safe_json_with_invalid_json(self):
        json = '{"data":true'
        expect = {}
        result = load_safe_json(json)
        self.assertEqual(result, expect)
