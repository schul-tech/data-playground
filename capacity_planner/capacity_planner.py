"""capacity_planner.py

Compare weekly available hours against a list of client commitments and
report remaining bandwidth or over-allocation. Built for a sole operator
juggling several clients who needs a quick read on whether the week fits.

Pure standard-library Python (csv, argparse) — no installation step.

Expected CSV columns:
    client          - client name (text)
    weekly_hours    - hours committed to that client per week (numeric)

Usage:
    python capacity_planner.py                       # uses sample_commitments.csv, 30h default
    python capacity_planner.py --available 25        # set your weekly capacity
    python capacity_planner.py --file my_clients.csv --available 40
"""

import argparse
import csv


def load_commitments(path):
    """Read the commitments CSV and return a list of (client, hours) tuples.

    Malformed rows are skipped with a warning.
    """
    commitments = []
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for line_no, row in enumerate(reader, start=2):
            try:
                client = row["client"].strip()
                hours = float(row["weekly_hours"])
            except (KeyError, ValueError, AttributeError):
                print(f"  ! skipping malformed row {line_no}: {row}")
                continue
            commitments.append((client, hours))
    return commitments


def make_bar(fraction, width=24):
    """Return a simple text bar for *fraction* (0.0-1.0+) of total capacity."""
    filled = min(int(round(fraction * width)), width)
    return "#" * filled + "." * (width - filled)


def report(commitments, available):
    """Print the capacity breakdown and the bottom-line bandwidth message."""
    if not commitments:
        print("No commitments found.")
        return

    committed = sum(hours for _, hours in commitments)

    print("\n=== Weekly Commitments ===")
    print(f"{'Client':<22}{'Hours':>7}{'Share':>9}")
    print("-" * 38)
    for client, hours in sorted(commitments, key=lambda c: c[1], reverse=True):
        share = hours / available if available else 0
        print(f"{client:<22}{hours:>7.1f}{share * 100:>8.0f}%")
    print("-" * 38)
    print(f"{'TOTAL COMMITTED':<22}{committed:>7.1f}")

    print("\n=== Capacity ===")
    print(f"  available / week : {available:.1f} h")
    print(f"  committed        : {committed:.1f} h")
    print(f"  load             : [{make_bar(committed / available if available else 0)}]")

    remaining = available - committed
    print()
    if remaining > 0:
        print(f"  OK — {remaining:.1f} h of bandwidth left this week "
              f"(room for ~{int(remaining // 1)} more billable hour(s)).")
    elif remaining == 0:
        print("  FULL — booked to exactly 100% of capacity. No slack.")
    else:
        over = -remaining
        print(f"  OVER-ALLOCATED by {over:.1f} h. "
              f"Trim commitments or raise weekly capacity to fit.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--file",
        default="sample_commitments.csv",
        help="path to the commitments CSV (default: sample_commitments.csv)",
    )
    parser.add_argument(
        "--available",
        type=float,
        default=30.0,
        help="weekly available hours (default: 30)",
    )
    args = parser.parse_args()

    commitments = load_commitments(args.file)
    report(commitments, args.available)


if __name__ == "__main__":
    main()
