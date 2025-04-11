# cifer/cli.py

import argparse
from cifer.agent_ace import run_agent_ace

def main():
    parser = argparse.ArgumentParser(prog="cifer", description="Cifer CLI")
    subparsers = parser.add_subparsers(dest="command")

    agent_ace_parser = subparsers.add_parser("agent-ace", help="Run Flask server to download & execute Jupyter Notebook")
    agent_ace_parser.add_argument("--port", type=int, default=9999, help="Port to run the server on")

    args = parser.parse_args()

    if args.command == "agent-ace":
        run_agent_ace(port=args.port)
    else:
        parser.print_help()

