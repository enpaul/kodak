import argparse
import logging
import sys

from kodak import __about__
from kodak import configuration
from kodak import database
from kodak import index


def get_args() -> argparse.Namespace:
    """Setup the flags for the basic CLI"""

    parser = argparse.ArgumentParser(
        prog=__about__.__name__, description=__about__.__summary__
    )

    parser.add_argument(
        "--server", action="store_true", help="Run the Flask development server"
    )
    parser.add_argument(
        "--config", action="store_true", help="Check that the configuration is valid"
    )
    parser.add_argument(
        "--version", action="store_true", help="Show program version and exit"
    )
    parser.add_argument(
        "--index", action="store_true", help="Rebuild the source image index"
    )

    return parser.parse_args()


def main() -> int:
    """Main entrypoint for the CLI tooling"""
    args = get_args()

    logging.basicConfig(
        stream=sys.stderr,
        format="(%(asctime)s) %(levelname)s: %(message)s",
        datefmt="%I:%M:%S",
        level=logging.DEBUG,
    )

    if args.version:
        print(f"{__about__.__title__} {__about__.__version__}", file=sys.stderr)
        return 0

    if args.config:
        try:
            configuration.load()
        except Exception as err:  # pylint: disable=broad-except
            print(f"Configuration check failed: {err}", file=sys.stderr)
            return 1
        else:
            print("Configuration check successful!", file=sys.stderr)
            return 0

    if args.index:
        config = configuration.load()
        database.initialize(config)
        index.build(config)
        return 0

    if args.server:
        from kodak import application  # pylint: disable=import-outside-toplevel

        application.APPLICATION.run(host="127.0.0.1")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
