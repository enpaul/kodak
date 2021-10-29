"""Development server stub entrypoint

Flask comes with a built-in development server. This entrypoint allows ``kodak``
to be run directly to run the development server and expose some simple config options for ease of
access. Run the below command to start the server:

::

  python -m kodak

In addition to the helpful CLI flags, the Flask development server run by this module will also
load any ``.env`` files in the current working directory when running the application.

.. warning:: As the development server will tell you on startup, do not use this for production
             deployments.
"""
import argparse
import sys

from kodak.application import APPLICATION


def main():
    """Run the development server"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--bind",
        help="Address or socket to bind the server to",
        default="127.0.0.1",
    )
    parser.add_argument(
        "-p", "--port", help="Port bind the server to", default=5000, type=int
    )
    parser.add_argument(
        "-D", "--debug", help="Run Flask in debug mode", action="store_true"
    )
    args = parser.parse_args()
    APPLICATION.run(host=args.bind, port=args.port, debug=args.debug, load_dotenv=True)


if __name__ == "__main__":
    sys.exit(main())
