from unittest import IsolatedAsyncioTestCase, main

from ai_cmd.tool_packs.python_pack import PythonPack


class TestPythonPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.python_pack = PythonPack()

    async def test_tool_reset(self):
        result = await self.python_pack.tool_reset(confirm=True)
        self.assertEqual(result, {"success": True})
        self.assertEqual(self.python_pack.globals, {})

    async def test_tool_exec_stdout(self):
        code = "for x in range(2):\n    print(x)"
        result = await self.python_pack.tool_exec(code=code)
        self.assertEqual(result["stdout"], "0\n1\n")

        code = "for x in range(2):\n    a = x"
        result = await self.python_pack.tool_exec(code=code)
        self.assertEqual(result["stdout"], "")

    async def test_tool_exec_globals(self):
        code = "data=[]\nfor x in range(2):\n    data.append(x)"
        await self.python_pack.tool_exec(code=code)
        self.assertEqual(self.python_pack.globals["data"], [0, 1])

    async def test_tool_exec_error(self):
        code = "raise ValueError()"
        result = await self.python_pack.tool_exec(code=code)
        self.assertEqual(result.get("stdout", None), "")
        self.assertEqual(result.get("error", None), str(ValueError()))
        self.assertEqual(result.get("type_error", None), "ValueError")

    async def test_tool_eval(self):
        code = "1 + 1"
        result = await self.python_pack.tool_eval(code=code)
        self.assertEqual(result["stdout"], "")
        self.assertEqual(result["value"], 2)

    # hay que arreglarlo
    # async def test_tool_pip(self):
    #    args = [
    #        "install",
    #        "requests",
    #    ]
    #    result = await self.python_pack.tool_pip(args=args)
    #    self.assertIn("Successfully installed", result["stdout"])


if __name__ == "__main__":
    main()
