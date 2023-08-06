import logging
from enum import auto, Enum
from html import escape
from typing import Optional

from omnihost.gemtext_parser import GemLine, LineType


class HTMLConverterState(Enum):
    DEFAULT = auto()
    PREFORMATTED = auto()
    LIST = auto()


class HTMLConverter:
    def __init__(self) -> None:
        self._state = HTMLConverterState.DEFAULT

    def convert_gemlines_to_html(
        self, gemlines: list[GemLine], title: str, stylesheet: Optional[str]
    ) -> str:
        self._state = HTMLConverterState.DEFAULT
        html_body = ""
        for gemline in gemlines:
            if self._state == HTMLConverterState.DEFAULT:
                if gemline.line_type == LineType.PREFORMATTED_ALT_TEXT:
                    html_body += self._start_preformatted_line(
                        alt_text=escape(gemline.line_contents)
                    )

                elif gemline.line_type == LineType.PREFORMATTED:
                    html_body += self._start_preformatted_line(
                        content=escape(gemline.line_contents)
                    )

                elif gemline.line_type == LineType.LISTITEM:
                    self._state = HTMLConverterState.LIST
                    html_body += f"<ul><li>{escape(gemline.line_contents)}</li>"

                else:
                    html_body += self._convert_default_gemline_to_html(gemline)

            elif self._state == HTMLConverterState.PREFORMATTED:
                if gemline.line_type == LineType.PREFORMATTED:
                    html_body += f"\n{escape(gemline.line_contents)}"

                elif gemline.line_type == LineType.END_PREFORMATTED:
                    self._state = HTMLConverterState.DEFAULT
                    html_body += "</pre>"

            elif self._state == HTMLConverterState.LIST:
                if gemline.line_type == LineType.LISTITEM:
                    html_body += f"<li>{escape(gemline.line_contents)}</li>"
                else:
                    html_body += "</ul>"

                    # the duplicate logic below could be eliminated if there was a
                    # separate END_LIST line in the gemline list

                    if gemline.line_type == LineType.PREFORMATTED_ALT_TEXT:
                        self._start_preformatted_line(alt_text=escape(gemline.line_contents))

                    elif gemline.line_type == LineType.PREFORMATTED:
                        self._start_preformatted_line(content=escape(gemline.line_contents))

                    else:
                        self._state = HTMLConverterState.DEFAULT
                        html_body += self._convert_default_gemline_to_html(gemline)

        html_contents = self._add_page_content_to_html_template(
            title, html_body, stylesheet
        )

        logging.info("HTML conversion successful")
        return html_contents

    def _start_preformatted_line(
        self, alt_text: Optional[str] = None, content: Optional[str] = None
    ) -> str:
        self._state = HTMLConverterState.PREFORMATTED
        if not alt_text and not content:
            raise HTMLConverterException(
                "The start of a preformatted block requires either alt_text or content."
            )
        elif alt_text and content:
            raise HTMLConverterException(
                "The start of a preformatted block cannot have both alt_text and "
                + f"content. Alt text: '{alt_text}', content: '{content}'"
            )
        elif alt_text:
            return f'<pre alt="{alt_text}">'
        else:
            return f"<pre>{content}"

    def _convert_default_gemline_to_html(self, gemline: GemLine) -> str:
        match gemline.line_type:
            case LineType.TEXT:
                return f"<p>{escape(gemline.line_contents)}</p>"
            case LineType.HEADING:
                return f"<h1>{escape(gemline.line_contents)}</h1>"
            case LineType.SUBHEADING:
                return f"<h2>{escape(gemline.line_contents)}</h2>"
            case LineType.SUBSUBHEADING:
                return f"<h3>{escape(gemline.line_contents)}</h3>"
            case LineType.LINK:
                return self._convert_link_to_html(gemline)
            case LineType.BLOCKQUOTE:
                return self._convert_block_quote_to_html(gemline)
            case _:
                raise HTMLConverterException(
                    "_convert_default_gemline_to_html() called on invalid LineType"
                    + f"{gemline.line_type}."
                )

    def _convert_link_to_html(self, gemline: GemLine) -> str:
        content = gemline.line_contents.strip().split()
        if len(content) == 0:
            raise HTMLConverterException("Empty link line")
        else:
            link = self._convert_link_for_html(content[0])
            if len(content) >= 2:
                return f'<p><a href="{link}">{" ".join(content[1:])}</a></p>'
            else:
                return f'<p><a href="{link}">{content[0]}</a></p>'

    def _convert_link_for_html(self, original_link: str) -> str:
        """Recognize if a link is an internal link and link to the html page instead
        of the original link referencing the gemtext page.

        Requires that internal links are using relative rather than absolute URLs
        TODO: is there a better way to handle this? are there additional edge cases not
        accounted for?
        """
        if "://" in original_link:
            # Absolute URL
            return original_link
        # This case probably doesn't need to be handled specially since AFAIK '.gmi' is
        # not a valid top level domain
        elif original_link.startswith("mailto:"):
            # Absolute URL
            return original_link
        else:
            # Relative link to gemini page
            if original_link.endswith(".gmi"):
                return f"{original_link[:-4]}.html"
            # Relative link to something else
            else:
                return original_link

    def _convert_block_quote_to_html(self, gemline: GemLine) -> str:
        """Handle a variable amount of whitespace at the start of a quote line."""
        quote_content = gemline.line_contents.strip()
        return f"<p>&gt; {escape(quote_content)}</p>"

    def _add_page_content_to_html_template(
        self, title: str, body: str, stylesheet: Optional[str]
    ) -> str:
        # TODO: is this worth something like a jinja template or at least another
        # solution where the multiline string doesn't ruin the indentation?
        css_link = ""
        if stylesheet is not None:
            css_link = f'<link rel="stylesheet" href="css/{stylesheet}" />'

        return f"""<!DOCTYPE HTML><html><head><title>{title}</title>{css_link}</head>
<body>{body}</body></html>"""


class HTMLConverterException(Exception):
    """Represents errors that occur within the HTMLConverter."""

    pass
