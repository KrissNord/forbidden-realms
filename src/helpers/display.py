import textwrap


def print_styled(console, settings, text, style="white", wrap=True):
    """Print text with style if colors enabled, plain if disabled."""
    if wrap and settings["text_width"]:
        text = textwrap.fill(text, width=settings["text_width"])

    if settings["colors_enabled"]:
        console.print(text, style=style)
    else:
        console.print(text)
