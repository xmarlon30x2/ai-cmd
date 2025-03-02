from unittest import IsolatedAsyncioTestCase, main

from ai_cmd.packs.python_pack import PythonPack


class TestPythonPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.python_pack = PythonPack()

    async def test_tool_list(self):
        ...

    async def test_tool_execute(self):
        ...
    
    async def test_tool_comunicate(self):
        ...
    
    async def test_tool_kill(self):
        ...

if __name__ == "__main__":
    main()
