from asyncio import sleep
from time import gmtime
from typing import Any

from ..tool_pack import ToolPack


class TimePack(ToolPack):

    name = "time"

    async def tool_info(self, confirm: bool) -> dict[str, Any]:
        """Muestra informacion sobre la fecha y hora"""
        struct = gmtime()
        return {
            "seconds": struct.tm_sec,
            "minutes": struct.tm_min,
            "hours": struct.tm_hour,
            "day": struct.tm_mday,
            "month": struct.tm_mon,
            "year": struct.tm_year,
        }

    async def tool_sleep(self, time: float):
        """Espera un determinado numero de segundos
        args:
            time: Cantidad de segundos a esperar"""
        await sleep(time)
