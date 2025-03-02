from typing import TYPE_CHECKING

from prompt_toolkit import HTML
from prompt_toolkit.layout import FormattedTextControl, HSplit, Window

from ...utils import load_safe_json
from ..styles import TOOL_MESSAGE_STYLE
from .utils import simple_render_frame

if TYPE_CHECKING:
    from ...core.history.types import ToolMessage
    from ...tools.types import ToolCall

simple_render_tool_message = simple_render_frame(
    title="Herramienta", class_name="tool-message", style=TOOL_MESSAGE_STYLE
)


def to_formated_text_controll(text: str):
    return FormattedTextControl(HTML(text))


@simple_render_tool_message
async def render_generic_tool_message(
    tool_call: "ToolCall", tool_message: "ToolMessage"
):
    response = load_safe_json(tool_message.content)
    name = tool_call.function.name
    if error := response.get("error"):
        text = f"<red>❌ Error <b>{name}</b>: {error}</red>"
    else:
        text = f"<green>✅ Accion <b>{name}</b> completada</green>"
    return Window(to_formated_text_controll(text), wrap_lines=True)


@simple_render_tool_message
async def render_dirs_list_tool_message(
    tool_call: "ToolCall", tool_message: "ToolMessage"
):
    response = load_safe_json(tool_message.content)
    name = tool_call.function.name
    if error := response.get("error"):
        text = f"<red>❌ Error <b>{name}</b>: {error}</red>"
        container = Window(FormattedTextControl(HTML(text)), wrap_lines=True)
    else:
        elements: list[str] = response.get("elements", [])
        path: str = response.get("path", "")
        size = len(str(len(elements)))
        container = HSplit(
            [
                Window(to_formated_text_controll(f"Directorio <b>{path}</b>")),
                *(
                    Window(to_formated_text_controll(f" {i:0>{size}}:{element}"))
                    for i, element in enumerate(elements)
                ),
            ]
        )
    return container


@simple_render_tool_message
async def render_dirs_create_tool_message(
    tool_call: "ToolCall", tool_message: "ToolMessage"
):
    response = load_safe_json(tool_message.content)
    name = tool_call.function.name
    if error := response.get("error"):
        text = f"<red>❌ Error <b>{name}</b>: {error}</red>"
    else:
        path: str = response.get("path", "")
        text = f"<green>Carpeta <b>{path}</b> creada con exito</red>"
    return Window(FormattedTextControl(HTML(text)), wrap_lines=True)


@simple_render_tool_message
async def render_os_shell_tool_message(
    tool_call: "ToolCall", tool_message: "ToolMessage"
):
    parameters = load_safe_json(tool_call.function.arguments)
    response = load_safe_json(tool_message.content)
    if error := response.get("error"):
        name = tool_call.function.name
        text = f"<red>❌ Error <b>{name}</b>: {error}</red>"
        container = Window(FormattedTextControl(HTML(text)), wrap_lines=True)
    else:
        command = parameters.get("command")
        stdout = response.get("stdout", "")
        stderr = response.get("stderr", "")
        returncode = response.get("returncode", "")
        text_command = f"Comando <b>{command}</b>"
        text_stdout = f"<gray>{stdout}</gray>"
        text_stderr = f"<red>{stderr}</red>"
        text_returncode = f"<orange>{returncode}</orange>"
        container = HSplit(
            [
                Window(to_formated_text_controll(text_command)),
                Window(to_formated_text_controll(text_stdout)),
                Window(to_formated_text_controll(text_stderr)),
                Window(to_formated_text_controll(text_returncode)),
            ]
        )
    return container
