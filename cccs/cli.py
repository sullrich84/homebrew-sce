import sys
import argparse
from cccs.globals import (
    app_version,
    app_name,
    app_full_name,
    app_description,
    app_epilog,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog=app_name,
        description=app_description,
        epilog=app_epilog,
    )

    parser.add_argument(
        "-v",
        "--version",
        help="prints the applications version",
        action="version",
        version=f"%(prog)s {app_version}",
    )

    return parser.parse_args()


def cli():
    try:
        args = parse_arguments()
        print(f"{app_full_name} v{app_version}")

    except KeyboardInterrupt:
        print("Aborted by user.")
        sys.exit(0)


if __name__ == "__main__":
    cli()
