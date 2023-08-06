import logging
import re
from dataclasses import dataclass
from string import ascii_letters
from typing import Any, Callable, List, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ShortcutNotGenerated(Exception):
    pass


class FailedToParseInput(Exception):
    pass


class TooManyItemsSelected(Exception):
    pass


class TooFewItemsSelected(Exception):
    pass


@dataclass
class Item:
    index: int
    data: Any
    display: str
    shortcut: str

    def display_with_shortcut(self):
        return re.sub(self.shortcut, f"[{self.shortcut}]", self.display)


def _convert_to_str(element: Any) -> str:
    return str(element)


def select(
    choices: List[Any],
    retry: bool = True,
    min_items: int = 0,
    max_items: Optional[int] = None,
    print_function: Callable[[Any], None] = print,
    prompt: str = "Select item(s): ",
    **kwargs,
) -> List[int]:
    if len(choices) == 0:
        return []
    if min_items < 0:
        raise ValueError("min_items < 0")
    if max_items:
        if max_items < min_items:
            raise ValueError(f"min_items: {min_items}, max_items: {max_items}")
    items = _generate_items(choices, **kwargs)
    _display_items(items, print_function)
    result: List[Item] = []
    while not result:
        try:
            inp = input(prompt)
            if min_items == 0 and inp == "":
                break
            query_result = []
            queries = inp.split()
            if len(queries) < min_items:
                raise TooFewItemsSelected
            if max_items:
                if len(queries) > max_items:
                    raise TooManyItemsSelected
            for query in queries:
                item = _find_item(query, items)
                if item is None:
                    raise FailedToParseInput
                query_result.append(item)
            result = query_result
        except (FailedToParseInput, TooFewItemsSelected, TooManyItemsSelected) as error:
            if retry:
                print("Please try again.")
                continue
            raise error
    return [item.index for item in result]


def _find_item(inp: str, items: List[Item]) -> Optional[Item]:
    for item in items:
        if item.shortcut == inp:
            return item
        if item.index == int(inp):
            return item
        # TODO
        if item.display == inp:
            return item
    return None


def _generate_items(choices: List[str], **kwargs):
    shortcuts: List[Item] = []
    for index, element in enumerate(choices):
        shortcuts.append(generate_shortcut(
            index, element, shortcuts, **kwargs))
    return shortcuts


def _display_items(items, print_function: Callable[[Any], None]):
    for item in items:
        print_function(f"{item.index} - {item.display_with_shortcut()}")


def generate_shortcut(
    index: int,
    data: Any,
    existing_items: List[Item],
    convert_to_str_func: Callable[[Any], str] = _convert_to_str,
    generate_lowercase=True,
    generate_uppercase=True,
    use_long_shortcuts=True,
) -> Item:
    short_shortcuts = [item.shortcut for item in existing_items]
    display = convert_to_str_func(data)
    # 'a'
    for letter in list(display):
        if letter not in ascii_letters:
            continue
        if letter not in short_shortcuts:
            return Item(index, data, display, letter)
    # 'A'
    if generate_uppercase:
        for letter in list(display.upper()):
            if letter not in ascii_letters:
                continue
            if letter not in short_shortcuts:
                return Item(index, data, display, letter)
    # 'a'
    if generate_lowercase:
        for letter in list(display.lower()):
            if letter not in ascii_letters:
                continue
            if letter not in short_shortcuts:
                return Item(index, data, display, letter)
    # 'aa'
    if use_long_shortcuts:
        for shortcut_length in range(len(display)):
            if shortcut_length in [0, 1]:
                continue
            start_index = 0
            looping = True
            while looping:
                try:
                    long_shortcut = display[start_index: start_index +
                                            shortcut_length]
                    for letter in long_shortcut:
                        if letter not in ascii_letters:
                            continue
                    if long_shortcut not in short_shortcuts:
                        return Item(index, data, display, long_shortcut)
                    start_index += 1
                except IndexError:
                    looping = False
    raise ShortcutNotGenerated
