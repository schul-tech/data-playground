# capacity_planner

Compares your weekly available hours against a list of client commitments and
reports remaining bandwidth or over-allocation. Designed for a sole operator
managing several clients who needs a fast answer to "does this week fit?"

## Requirements

Pure Python standard library — no installation needed. Python 3.7+.

## Usage

```bash
# Run against the sample data with a 30-hour default week
python capacity_planner.py

# Set your own weekly capacity
python capacity_planner.py --available 25

# Use your own client list
python capacity_planner.py --file my_clients.csv --available 40
```

## Input format

The CSV must have these two columns:

| column       | description                         |
| ------------ | ----------------------------------- |
| client       | client name                         |
| weekly_hours | hours committed to that client/week |

See `sample_commitments.csv` for an example. Malformed rows are skipped with a
warning.

## What it reports

- Each client's weekly hours and share of your capacity, sorted heaviest first.
- Total committed hours and a text load bar.
- A bottom-line message: hours of bandwidth left, exactly full, or
  over-allocated by N hours.
