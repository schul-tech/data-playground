"""invoice_generator.py

Read a CSV of billable work entries and write a plain-text invoice for a
chosen client. Each line item is hours x rate; the script totals them, adds
an optional tax rate, and writes a neatly aligned .txt invoice to disk.

Pure standard-library Python (csv, argparse, datetime) — no installation step.

Expected CSV columns:
    client      - client name (text)
    date        - work date in YYYY-MM-DD format
    description - short description of the work
    hours       - hours worked (numeric)
    rate        - hourly rate in dollars (numeric)

Usage:
    python invoice_generator.py                          # lists clients in sample data
    python invoice_generator.py --client "Lin Family"    # invoice one client
    python invoice_generator.py --client "Lin Family" --tax 8.25
    python invoice_generator.py --client "Lin Family" --file my_work.csv
"""

import argparse
import csv
from collections import defaultdict
from datetime import date, datetime


def load_entries(path):
    """Read the work-log CSV and return {client: [entry, ...]}.

    Each entry is a dict with parsed date, description, hours, and rate.
    Malformed rows are skipped with a warning.
    """
    by_client = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for line_no, row in enumerate(reader, start=2):
            try:
                entry = {
                    "date": datetime.strptime(row["date"].strip(), "%Y-%m-%d").date(),
                    "description": row["description"].strip(),
                    "hours": float(row["hours"]),
                    "rate": float(row["rate"]),
                }
            except (KeyError, ValueError, AttributeError):
                print(f"  ! skipping malformed row {line_no}: {row}")
                continue
            by_client[row["client"].strip()].append(entry)

    for client in by_client:
        by_client[client].sort(key=lambda e: e["date"])
    return by_client


def build_invoice(client, entries, tax_rate=0.0):
    """Return the invoice as a single formatted string.

    *tax_rate* is a percentage, e.g. 8.25 for 8.25%.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("INVOICE".center(60))
    lines.append("=" * 60)
    lines.append(f"Bill to : {client}")
    lines.append(f"Date    : {date.today():%Y-%m-%d}")
    lines.append("-" * 60)
    lines.append(f"{'Date':<12}{'Description':<26}{'Hrs':>5}{'Rate':>7}{'Amt':>9}")
    lines.append("-" * 60)

    subtotal = 0.0
    total_hours = 0.0
    for e in entries:
        amount = e["hours"] * e["rate"]
        subtotal += amount
        total_hours += e["hours"]
        desc = (e["description"][:23] + "...") if len(e["description"]) > 26 else e["description"]
        lines.append(
            f"{e['date']:%Y-%m-%d}  {desc:<26}{e['hours']:>5.1f}"
            f"{e['rate']:>7.0f}{amount:>9.2f}"
        )

    lines.append("-" * 60)
    lines.append(f"{'Total hours':<43}{total_hours:>8.1f}")
    lines.append(f"{'Subtotal':<43}{'$' + format(subtotal, '.2f'):>17}")

    tax_amount = subtotal * (tax_rate / 100.0)
    if tax_rate:
        lines.append(f"{f'Tax ({tax_rate:.2f}%)':<43}{'$' + format(tax_amount, '.2f'):>17}")

    total = subtotal + tax_amount
    lines.append("=" * 60)
    lines.append(f"{'TOTAL DUE':<43}{'$' + format(total, '.2f'):>17}")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Thank you for your business!")
    return "\n".join(lines)


def safe_filename(client):
    """Turn a client name into a filesystem-friendly invoice filename."""
    slug = "".join(c if c.isalnum() else "_" for c in client).strip("_").lower()
    return f"invoice_{slug}_{date.today():%Y%m%d}.txt"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--file",
        default="sample_work.csv",
        help="path to the work-log CSV (default: sample_work.csv)",
    )
    parser.add_argument("--client", help="client name to invoice (exact match)")
    parser.add_argument(
        "--tax",
        type=float,
        default=0.0,
        help="tax rate as a percentage, e.g. 8.25 (default: 0)",
    )
    args = parser.parse_args()

    by_client = load_entries(args.file)

    if not args.client:
        print("Clients found in this file:")
        for name in sorted(by_client):
            print(f"  - {name}")
        print("\nRe-run with --client \"<name>\" to generate an invoice.")
        return

    entries = by_client.get(args.client)
    if not entries:
        print(f"No entries found for client: {args.client!r}")
        return

    invoice = build_invoice(args.client, entries, args.tax)
    print("\n" + invoice)

    out_path = safe_filename(args.client)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(invoice + "\n")
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
