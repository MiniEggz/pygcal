#!/usr/bin/env python3
import argparse

from pygcal import end_event, set_timezone, start_event, upcoming


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # def start command
    start_parser = subparsers.add_parser("start", help="Start a calendar event.")
    start_parser.add_argument("event_name", type=str, help="Name of calendar event.")
    start_parser.add_argument(
        "-d",
        "--description",
        type=str,
        default="",
        help="Optional description of calendar event.",
    )

    # def stop command
    stop_parser = subparsers.add_parser("stop", help="Stop an event.")
    stop_parser.add_argument("event_name", type=str, help="Name of calendar event.")

    # def view command
    view_parser = subparsers.add_parser("view", help="View events.")
    view_parser.add_argument(
        "-n", type=int, default=10, help="Optional max number of events to view."
    )
    view_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print table (not verbose) or all details.",
    )

    # def settz command
    settz_parser = subparsers.add_parser("settz", help="Set timezone for google api.")

    # handle all arguments
    args = parser.parse_args()
    if args.command == "start":
        start_event(args.event_name, args.description)
    elif args.command == "stop":
        end_event(args.event_name)
    elif args.command == "view":
        upcoming(args.n, verbose=args.verbose)
    elif args.command == "settz":
        set_timezone()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
