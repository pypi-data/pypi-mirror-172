import argparse

from superbox_utils.logging import LOG_LEVEL


def init_argparse(description: str) -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description)

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help=f"verbose mode: multiple -v options increase the verbosity (maximum: {len(LOG_LEVEL)})",
    )

    return parser
