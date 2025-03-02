import re
from typing import Any, Dict, Optional, Tuple


class DocstringParser:
    """Parsea docstrings en m\u00faltiples formatos para extraer metadatos"""

    SECTION_HEADERS = {
        "parameters": ["args", "parameters", "params"],
        "returns": ["returns", "return"],
        "raises": ["raises", "exceptions"],
    }

    @classmethod
    def parse(cls, doc: str) -> Tuple[str, dict[str, str]]:
        """Extrae descripci\u00f3n y par\u00e1metros del docstring"""
        if not doc:
            return "", {}

        description, params = cls._parse_rst(doc)
        if params:
            return description, params

        description, params = cls._parse_numpy(doc)
        if params:
            return description, params

        description, params = cls._parse_standard(doc)
        return description, params

    @classmethod
    def _parse_standard(cls, doc: str) -> Tuple[str, dict[str, str]]:
        lines = [line.strip() for line in doc.split("\n") if line.strip()]

        description: list[str] = []
        current_section: str | None = None
        params: Dict[str, str] = {}
        current_param: str | None = None

        for line in lines:
            if cls._is_section_header(line):
                current_section = cls._identify_section(line)
                current_param = None
                continue

            if current_section == "parameters":
                param, desc = cls._parse_param_line(line)
                if param:
                    current_param = param
                    params[current_param] = desc
                elif current_param:
                    params[current_param] += f" {line}"

            elif not current_section:
                description.append(line)
        return " ".join(description).strip(), params

    @classmethod
    def _parse_numpy(cls, doc: str) -> Tuple[str, dict[str, str]]:
        description = ""
        params: dict[str, Any] = {}
        lines = doc.splitlines()
        description_lines: list[str] = []
        param_name = None
        param_desc: list[str] = []
        in_parameters_section = False

        for line in lines:
            line = line.strip()

            if line.lower() == "parameters":
                in_parameters_section = True
                continue

            if in_parameters_section:
                if re.match(r"^-+$", line):
                    continue

                match = re.match(r"^(\w+)\s*:\s*(\w+)$", line)
                if match:
                    if param_name:
                        params[param_name] = " ".join(param_desc).strip()
                    param_name = match.group(1)
                    param_desc = []
                    continue

                if param_name:
                    param_desc.append(line)
            else:
                description_lines.append(line)

        if param_name:
            params[param_name] = " ".join(param_desc).strip()

        description = " ".join(description_lines).strip()
        return description, params

    @classmethod
    def _parse_rst(cls, doc: str) -> Tuple[str, dict[str, str]]:
        description = ""
        params: dict[str, Any] = {}
        lines = doc.splitlines()
        description_lines: list[str] = []
        param_name = None

        for line in lines:
            line = line.strip()

            if line.startswith(":param"):
                parts = line.split(":")
                if len(parts) > 2:
                    param_parts = parts[1].split(" ", 1)
                    param_name = param_parts[0].strip()
                    if param_name:
                        param_desc = " ".join(parts[2:]).strip()
                        params[param_name] = param_desc
            elif not params:
                description_lines.append(line)

        description = " ".join(description_lines).strip()
        return description, params

    @classmethod
    def _is_section_header(cls, line: str) -> bool:
        return any(
            line.lower().strip().startswith(f"{header}:")
            for headers in cls.SECTION_HEADERS.values()
            for header in headers
        )

    @classmethod
    def _identify_section(cls, line: str) -> Optional[str]:
        for section, headers in cls.SECTION_HEADERS.items():
            if any(line.lower().strip().startswith(f"{header}:") for header in headers):
                return section
        return None

    @staticmethod
    def _parse_param_line(line: str) -> tuple[str, str]:
        if ":" in line:
            param, desc = map(str.strip, line.split(":", 1))
            return param.split(" ")[0], desc
        return "", ""
