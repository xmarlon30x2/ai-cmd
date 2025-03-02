from os import remove
from subprocess import PIPE, Popen
from typing import Any, Final, Literal, Self
from uuid import uuid4

Status = Literal["init", "pending", "complete", "error"]


class PythonProgram:

    def __init__(self, code: str):
        self.id: Final[str] = str(uuid4())
        self.path: Final[str] = self._serialize(code)
        self.process = None

    @property
    def return_code(self) -> int | None:
        return self.process.poll() if self.process else None

    def comunicate(self, input: str | None = None, timeout: float | None = None):
        if self.process:
            return self.process.communicate(input=input, timeout=timeout)
        else:
            raise RuntimeError("Proceso no iniciado")

    def start(self) -> None:
        self.process = Popen(
            args=f"python {self.path}",
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf-8",
            text=True,
        )

    def wait(self) -> None:
        if self.process:
            self.process.wait()

    def kill(self) -> None:
        if self.process:
            self.process.kill()
        try:
            remove(self.path)
        except OSError:
            pass

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, *args: Any) -> None:
        self.kill()

    def _serialize(self, code: str) -> str:
        path = f"code_{self.id}.py"
        with open(file=path, mode="w", encoding="utf-8") as temp_file:
            temp_file.write(code)
            return temp_file.name
