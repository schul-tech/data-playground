"""grade_tracker.py

Read a CSV of student scores over time and report per-student averages,
trends (improving / declining / steady), and a class-wide summary.

The script is pure standard-library Python (csv, argparse, statistics) so it
runs anywhere with no installation step.

Expected CSV columns:
    student   - student name (text)
    date      - assessment date in YYYY-MM-DD format
    score     - numeric score, e.g. 0-100

Usage:
    python grade_tracker.py                      # uses sample_scores.csv
    python grade_tracker.py --file my_scores.csv # use your own data
    python grade_tracker.py --student "Ava Chen" # report on one student
"""

import argparse
import csv
import statistics
from collections import defaultdict
from datetime import datetime


def load_scores(path):
    """Read the CSV at *path* and return {student: [(date, score), ...]}.

    Rows are sorted by date for each student so trend logic is reliable.
    Rows with missing or unparseable data are skipped with a warning.
    """
    by_student = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for line_no, row in enumerate(reader, start=2):  # header is line 1
            try:
                name = row["student"].strip()
                date = datetime.strptime(row["date"].strip(), "%Y-%m-%d").date()
                score = float(row["score"])
            except (KeyError, ValueError, AttributeError):
                print(f"  ! skipping malformed row {line_no}: {row}")
                continue
            by_student[name].append((date, score))

    for name in by_student:
        by_student[name].sort(key=lambda pair: pair[0])
    return by_student


def trend(scores):
    """Return a short label describing the direction of a score list.

    Compares the first and last scores. A change within +/- 2 points is
    treated as 'steady' to avoid over-reacting to tiny fluctuations.
    """
    if len(scores) < 2:
        return "n/a (need 2+ scores)"
    change = scores[-1] - scores[0]
    if change > 2:
        return f"improving (+{change:.1f})"
    if change < -2:
        return f"declining ({change:.1f})"
    return f"steady ({change:+.1f})"


def report(by_student):
    """Print a per-student report followed by a class summary."""
    if not by_student:
        print("No valid score data found.")
        return

    print("\n=== Per-Student Report ===")
    all_scores = []
    for name in sorted(by_student):
        scores = [score for _, score in by_student[name]]
        all_scores.extend(scores)
        avg = statistics.mean(scores)
        latest = scores[-1]
        print(f"\n{name}")
        print(f"  assessments : {len(scores)}")
        print(f"  average     : {avg:.1f}")
        print(f"  latest      : {latest:.1f}")
        print(f"  trend       : {trend(scores)}")

    print("\n=== Class Summary ===")
    print(f"  students        : {len(by_student)}")
    print(f"  total scores    : {len(all_scores)}")
    print(f"  class average   : {statistics.mean(all_scores):.1f}")
    print(f"  highest score   : {max(all_scores):.1f}")
    print(f"  lowest score    : {min(all_scores):.1f}")
    if len(all_scores) > 1:
        print(f"  std deviation   : {statistics.stdev(all_scores):.1f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--file",
        default="sample_scores.csv",
        help="path to the scores CSV (default: sample_scores.csv)",
    )
    parser.add_argument(
        "--student",
        help="limit the report to a single student (exact name match)",
    )
    args = parser.parse_args()

    by_student = load_scores(args.file)

    if args.student:
        by_student = {
            name: rows
            for name, rows in by_student.items()
            if name == args.student
        }
        if not by_student:
            print(f"No data found for student: {args.student!r}")
            return

    report(by_student)


if __name__ == "__main__":
    main()
