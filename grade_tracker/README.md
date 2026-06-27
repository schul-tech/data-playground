# grade_tracker

Reads a CSV of student scores over time and reports per-student averages,
trends, and a class-wide summary. Useful for spotting which students are
improving, plateauing, or slipping between assessments.

## Requirements

Pure Python standard library — no installation needed. Python 3.7+.

## Usage

```bash
# Run against the included sample data
python grade_tracker.py

# Use your own CSV
python grade_tracker.py --file my_scores.csv

# Report on a single student
python grade_tracker.py --student "Ava Chen"
```

## Input format

The CSV must have these three columns:

| column  | description                       |
| ------- | --------------------------------- |
| student | student name                      |
| date    | assessment date as `YYYY-MM-DD`   |
| score   | numeric score (e.g. 0–100)        |

See `sample_scores.csv` for an example. Malformed rows are skipped with a
warning rather than crashing the run.

## What it reports

- **Per student:** number of assessments, average, latest score, and a trend
  label (improving / declining / steady) based on first-vs-latest score.
- **Class summary:** student count, class average, highest and lowest scores,
  and standard deviation.
