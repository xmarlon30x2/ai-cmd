from typing import TYPE_CHECKING

from prompt_toolkit import HTML
from prompt_toolkit.layout import BufferControl, FormattedTextControl, HSplit, Window
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.widgets import HorizontalLine
from pygments.lexers import get_lexer_for_filename

from ...utils import load_safe_json
from ..styles import ACTION_MESSAGE_STYLE
from .utils import simple_render_frame

if TYPE_CHECKING:
    from ...tools.types import ToolCall


simple_render_tool_call = simple_render_frame(
    title="Acción", class_name="action-message", style=ACTION_MESSAGE_STYLE
)


@simple_render_tool_call
async def render_generic_tool_call(tool_call: "ToolCall"):
    return Window(
        FormattedTextControl(
            HTML(f"🏷️ Nombre: <gray><b>{tool_call.function.name}</b></gray>")
        ),
        wrap_lines=True,
    )


@simple_render_tool_call
async def render_files_read_tool_call(tool_call: "ToolCall"):
    parameters = load_safe_json(tool_call.function.arguments)
    path = parameters.get("path", "")
    return Window(
        FormattedTextControl(
            HTML(f"👁️ <i>Leyendo</i> el archivo: <yellow><b>{path}</b></yellow>")
        ),
        wrap_lines=True,
    )


@simple_render_tool_call
async def render_files_write_tool_call(tool_call: "ToolCall"):
    parameters = load_safe_json(tool_call.function.arguments)
    path = parameters.get("path", "")
    content = parameters.get("content", "")
    header = FormattedTextControl(
        HTML(f"✏️ <i>Escribiendo</i> en el archivo: <yellow><b>{path}</b></yellow>")
    )
    pygment_lexer = get_lexer_for_filename(path)
    lexer = PygmentsLexer(type(pygment_lexer))
    arg_content = BufferControl(lexer=lexer)
    arg_content.buffer.text = content
    return HSplit(
        [
            Window(header, wrap_lines=True),
            HorizontalLine(),
            Window(arg_content, wrap_lines=True),
        ]
    )


@simple_render_tool_call
async def render_os_shell_tool_call(tool_call: "ToolCall"):
    parameters = load_safe_json(tool_call.function.arguments)
    command = parameters.get("command", "")
    return Window(
        FormattedTextControl(
            HTML(f"💻 <i>Ejecutando</i> comando: <yellow><b>{command}</b></yellow>")
        )
    )


@simple_render_tool_call
async def render_dirs_list_tool_call(tool_call: "ToolCall"):
    parameters = load_safe_json(tool_call.function.arguments)
    path = parameters.get("path", "")
    return Window(
        FormattedTextControl(
            HTML(f"📜 <i>Listando</i> el directorio: <yellow>{path}</yellow>")
        )
    )
