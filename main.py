"""
Main entry point for the Web Authentication Testing Framework.

This script parses CLI arguments and launches the LoginEngine
to perform authentication testing and artifact analysis.
"""

import argparse
from core.login_engine import LoginEngine


def main():
    """
    Parse command line arguments and execute the login engine.
    """

    parser = argparse.ArgumentParser(
        description="Web Authentication Testing Framework"
    )

    # URL of the login page to test
    parser.add_argument(
        "--url",
        required=True,
        help="Login URL"
    )

    # Optional username for automated login
    parser.add_argument(
        "--username",
        required=False,
        help="Username for login"
    )

    # Optional password for automated login
    parser.add_argument(
        "--password",
        required=False,
        help="Password for login"
    )

    args = parser.parse_args()

    print("\n[START] Web Authentication Testing Framework\n")

    engine = LoginEngine(
        url=args.url,
        username=args.username,
        password=args.password
    )

    engine.run()


if __name__ == "__main__":
    main()