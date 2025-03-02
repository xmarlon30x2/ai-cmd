from unittest import TestCase

from pexpect import spawn


class Test__main__(TestCase):
    def test_execute(self):
        unit: spawn[str] = spawn("python -m ai_cmd", cwd="../")
        self.assertEqual(unit.exitstatus, 0)
