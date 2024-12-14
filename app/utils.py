import re
from typing import Sequence

from chatgpt_md_converter import telegram_format


def md_to_html(text: str) -> str:
    """Converts markdown in the provided text to HTML supported by Telegram."""
    return telegram_format(text)  # type: ignore[no-any-return]


def split_msg(msg: str, *, with_photo: bool = False) -> Sequence[str]:
    """Split a message into parts that fit within the Telegram message length limit."""
    parts: list[str] = []
    while msg:
        # Determining the maximum message length based on
        # with_photo and whether it's the first iteration
        # (photo is sent only with the first message).
        if parts:
            max_msg_length = 4096
        else:
            if with_photo:
                max_msg_length = 1024
            else:
                max_msg_length = 4096

        if len(msg) <= max_msg_length:
            # The message length fits within the maximum allowed.
            parts.append(msg)
            break
        else:
            # Cutting a part of the message with the maximum length from msg
            # and finding a position for a break by a newline character.
            part = msg[:max_msg_length]
            first_ln = part.rfind("\n")

            if first_ln != -1:
                # Found a newline character. Splitting the message by it, excluding the character itself.
                new_part = part[:first_ln]
                parts.append(new_part)
                # Trimming msg to the length of the new part
                # and removing the newline character.
                msg = msg[first_ln + 1 :]
            else:
                # No newline character found in the message part.
                # Try to find at least a space for a break.
                first_space = part.rfind(" ")

                if first_space != -1:
                    # Found a space. Splitting the message by it, excluding the space itself.
                    new_part = part[:first_space]
                    parts.append(new_part)
                    # Trimming msg to the length of the new part
                    # and removing the space.
                    msg = msg[first_space + 1 :]
                else:
                    # No suitable place for a break found in the message part.
                    # Simply add the current part and trim the message
                    # to its length.
                    parts.append(part)
                    msg = msg[max_msg_length:]
    return parts


def split_msg_html(text: str, *, with_photo: bool = False) -> Sequence[str]:
    """Splits the text into parts considering tags."""
    result = split_msg(msg=text, with_photo=with_photo)
    result_parts = []
    open_tags: Sequence[str] = ()
    for part in result:
        text, open_tags = close_tags(part, open_tags)
        result_parts.append(text)
    return result_parts


def close_tags(
    html: str, open_tags: Sequence[str] = ()
) -> tuple[str, Sequence[str]]:
    """Close all opening tags. Add missing opening tags"""
    # Pattern for finding tags considering attributes
    tag_pattern = re.compile(r"<(/?)(\w+)([^>]*)>")
    open_stack: list[str] = []
    close_queue: list[str] = []
    close_open_tags: list[str] = []

    for tag in tag_pattern.finditer(html):
        is_closing_tag = tag.group(1) == "/"
        tag_name = tag.group(2)
        tag_atr = tag.group(3)

        if not is_closing_tag:
            # If it's an opening tag, put it in the stack
            open_stack.insert(0, tag_name)
            close_open_tags.append(f"<{tag_name}{tag_atr}>")

        elif open_stack and open_stack[0] == tag_name:
            # If it's a closing tag and the last opening tag in the stack matches the current closing tag, remove it from the stack
            open_stack.pop(0)

        else:
            # If the closing tag has no opening tag, add it to the queue
            close_queue.append(tag_name)

    # Close all unclosed tags
    for tag_name in open_stack:
        html += "</" + tag_name + ">"

    if open_tags:
        html = "".join(open_tags) + html
    else:
        # Open all unopened tags
        for tag_name in close_queue:
            html = "<" + tag_name + ">" + html

    return html, close_open_tags[-len(open_stack) :]
