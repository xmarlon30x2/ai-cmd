from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import MagicMock

from ai_cmd.tools.tools_packs.python.base import PythonPack


class TestPythonPack(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.python_pack = PythonPack(controller=MagicMock(), window=MagicMock())

    async def test_tool_list(self): ...

    async def test_tool_execute(self): ...

    async def test_tool_comunicate(self): ...

    async def test_tool_kill(self): ...


if __name__ == "__main__":
    main()
