import os
from os import remove
from typing import Any, Final, Literal, Self
from uuid import uuid4

from pexpect import EOF, TIMEOUT, spawn

Status = Literal["init", "pending", "complete", "error"]


class PythonProgram:

    def __init__(self, code: str):
        self.id: Final[str] = str(uuid4())
        self.path: Final[str] = self._serialize(code)
        self.child: spawn[str] | None = None

    @property
    def return_code(self) -> int | None:
        return self.child.exitstatus if self.child else None

    def comunicate(self, input: str | None = None, timeout: float | None = None):
        if self.child:
            try:
                if input:
                    self.child.sendline(input)

                if timeout is None:
                    timeout = 0.1  # Timeout pequeño por defecto para no bloquear indefinidamente

                self.child.expect([TIMEOUT, EOF], timeout=timeout)
                stdout = self.child.before.strip() if self.child.before else ""
                stderr = (
                    self.child.read_nonblocking(size=10000, timeout=timeout).strip()
                    if hasattr(self.child, "read_nonblocking")
                    else ""
                )

                return {"stdout": stdout, "stderr": stderr}
            except EOF:
                return {"stdout": self.child.before.strip() if self.child.before else "", "stderr": ""}
            except TIMEOUT:
                return {"stdout": self.child.before.strip() if self.child.before else "", "stderr": ""}
            except Exception as e:
                return {"error": str(e)}
        else:
            raise RuntimeError("Proceso no iniciado")

    def start(self) -> None:
        try:
            self.child = spawn(f"python {self.path}", encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Error al iniciar el proceso: {e}")

    def wait(self) -> None:
        if self.child:
            self.child.wait()

    def kill(self) -> None:
        if self.child:
            try:
                self.child.close(force=True)
            except Exception as e:
                print(f"Error al cerrar el proceso: {e}")

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
        file_path = os.path.join(os.path.dirname(__file__), f"{self.id}.py")
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(code)
        return file_path

    def __del__(self):
        try:
            self.kill()
        except:
            pass
