"""Parsers"""

from typing import Dict, List, Optional, Tuple


class DocstringParser:
    """Parsea docstrings en múltiples formatos para extraer metadatos"""

    SECTION_HEADERS = {
        "parameters": ["args", "parameters", "params"],
        "returns": ["returns", "return"],
        "raises": ["raises", "exceptions"],
    }

    @classmethod
    def parse(cls, doc: str) -> Tuple[str, dict[str, str]]:
        """Extrae descripción y parámetros del docstring"""
        lines = [line.strip() for line in doc.split("\n") if line.strip()]
        if not lines:
            return "", {}

        description: List[str] = []
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
    def _is_section_header(cls, line: str) -> bool:
        return any(
            line.lower().startswith(f"{header}:")
            for headers in cls.SECTION_HEADERS.values()
            for header in headers
        )

    @classmethod
    def _identify_section(cls, line: str) -> Optional[str]:
        for section, headers in cls.SECTION_HEADERS.items():
            if any(line.lower().startswith(f"{header}:") for header in headers):
                return section
        return None

    @staticmethod
    def _parse_param_line(line: str) -> tuple[str, str]:
        if ":" in line:
            param, desc = map(str.strip, line.split(":", 1))
            return param, desc
        return "", ""
