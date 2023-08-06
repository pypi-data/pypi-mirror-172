import argparse
import logging
import json
from interactive_select.core import select

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("items", nargs="*")
    parser.add_argument("-m", "--min", default=0)
    parser.add_argument("-M", "--max", default=-1)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-i", "--index", action="store_true")
    config = parser.parse_args()

    if config.debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug(config)

    min_items = config.min
    if config.max == -1:
        max_items = None
    else:
        max_items = config.max

    result = select(
            config.items,
            min_items=min_items,
            max_items=max_items
                    )

    if config.index:
        result = [config.items[index] for index in result]

    if config.json:
        print(json.dumps(result))
    else:
        for line in result:
            print(line)


if __name__ == "__main__":
    main()
