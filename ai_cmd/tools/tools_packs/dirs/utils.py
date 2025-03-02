import os
from typing import Any


def scan_dir(path: str) -> dict[str, Any]:
    elements: list[dict[str, Any]] = []
    for element in os.scandir(path):
        if element.is_dir():
            try:
                elements.append(scan_dir(element.path))
            except Exception as exc:
                elements.append(
                    {"path": element.path, "type": "dir", "error": str(exc)}
                )
        else:
            elements.append(
                {
                    path: "str",
                    "type": (
                        "file"
                        if element.is_file()
                        else ("symlink" if element.is_symlink() else "none")
                    ),
                }
            )
    return {"path": path, "type": "dir", "elements": elements}
