from __future__ import annotations

from typing import Iterable, Literal


hr = "[HR]"


def link(url: str, link_text: str | None = None) -> str:
    """
    Formats a URL to a link.

    If no link text given, the URL will be used as the text.
    """
    return f"[URL={url}]{link_text}[/URL]" if link_text is not None else f"[URL]{url}[/URL]"


def img(image_url: str) -> str:
    """Formats a URL to embed an image"""
    return f"[IMG]{image_url}[/IMG]"


def size(font_size: int | str, string: str) -> str:
    """
    Formats the given text to a specific font size.

    Font size can be relative to the current size by indicating with '+' or '-'

    Example:
        - size(font_size=24, '...')
        - size(font_size='+2', '...')
        - size(font_size='-2', '...')
    """

    return f"[SIZE={font_size}]{string}[/SIZE]"


def color(color_code: str, string: str) -> str:
    """
    Formats the given text to have color.

    Available color formats:
        - HTML Color Name (e.g. "red", "SpringGreen")
        - Hex Triplet (e.g. "#f00", "#ff0000")
    """

    return f"[COLOR={color_code}]{string}[/COLOR]"


def bold(string: str) -> str:
    """Bolden the given text"""
    return f"[B]{string}[/B]"


def italic(string: str) -> str:
    """Italicize the given text"""
    return f"[I]{string}[/I]"


def underline(string: str) -> str:
    """Underlines the given text"""
    return f"[U]{string}[/U]"


def strike(string: str) -> str:
    """Strikethrough the given text"""
    return f"[S]{string}[/S]"


def center(string: str) -> str:
    """Floats the given text to the center"""
    return f"[CENTER]{string}[/CENTER]"


def left(string: str) -> str:
    """Floats the given text to the left"""
    return f"[LEFT]{string}[/LEFT]"


def right(string: str) -> str:
    """Floats the given text to the right"""
    return f"[RIGHT]{string}[/RIGHT]"


def list_(members: Iterable[str], style: Literal["1", "a", "i", "A", "I"] | None = None) -> str:
    """Formats a list. Will default to bullet style list if none provided.

    Other available styles:
        - Numeric list: '1'
        - Lower alphabetical list: 'a'
        - Lower Roman numeral list: 'i'
        - Upper alphabetical list: 'A'
        - Upper Roman numeral list: 'I'
    """

    items = "\n".join(f"[*]{item}" for item in members)
    return f"""{'[LIST]' if style is None else f'[LIST={style}]'}\n{items}\n[/LIST]"""


def table(rows: Iterable[str]) -> str:
    table_rows = "\n".join(map(str, rows))
    return f"[TABLE]\n{table_rows}\n[/TABLE]"


def table_header_row(members: Iterable[str]) -> str:
    return f"""[TR]{"".join(f"[TH]{member}[/TH]" for member in members)}[/TR]"""


def table_row(members: Iterable[str]) -> str:
    return f"""[TR]{"".join(f"[TD]{member}[/TD]" for member in members)}[/TR]"""
