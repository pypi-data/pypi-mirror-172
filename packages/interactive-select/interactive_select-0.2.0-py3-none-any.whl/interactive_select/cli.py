import argparse
import json
import logging

from interactive_select.core import select

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("items", nargs="*", type=str)
    parser.add_argument("-m", "--min", type=int, default=0)
    parser.add_argument("-M", "--max", type=int, default=-1)
    parser.add_argument("-r", "--retry", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-i", "--index", action="store_true")
    parser.add_argument("-p", "--prompt", type=str, default="Select: ")
    config = parser.parse_args()

    if config.debug:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug(config)

    min_items = config.min
    if config.max == -1:
        max_items = None
    else:
        max_items = config.max

    result = select(config.items, min_items=min_items, max_items=max_items, retry=config.retry, prompt=config.prompt)

    if not config.index:
        result = [config.items[index] for index in result]

    if config.json:
        print(json.dumps(result))
    else:
        for line in result:
            print(line)


if __name__ == "__main__":
    main()
