import textwrap
from datetime import datetime


def format_time(t: datetime):
    return t.strftime("%Y-%m-%d %H:%M")


def truncate_string(s, length=20):
    """Truncates string to given length."""
    return textwrap.shorten(s, width=length, placeholder="...")


def print_event(event, verbose=False):
    """Print an individual event to the screen."""
    start = datetime.fromisoformat(event.get("start").get("dateTime"))
    end = datetime.fromisoformat(event.get("end").get("dateTime"))
    summary = event.get("summary")
    description = event.get("description", "")
    if not verbose:
        print(
            "|{:^20}|{:^20}|{:^20}|".format(
                format_time(start), format_time(end), truncate_string(summary)
            )
        )
    else:
        print("* EVENT:")
        print("Title:")
        print(f"  {summary}")
        print("Start time:")
        print(f"  {format_time(start)}")
        print("End Time:")
        print(f"  {format_time(end)}")
        print("Description:")
        print(f"  {description}")
        print()


def display_events(events, verbose=False):
    """Display all events in an event list."""
    print()
    if not verbose:
        print(" {:^20} {:^20} {:^20}".format("Start Time", "End Time", "Title"))
        print("-" * 64)

    # print start and name of the next 10 events
    for event in events:
        print_event(event, verbose=verbose)

    if not verbose:
        print("-" * 64)

    print()
