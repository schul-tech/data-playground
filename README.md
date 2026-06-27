# data-playground

A small collection of pure-Python command-line tools for running a tutoring
practice — tracking student progress, billing clients, and managing weekly
capacity. Each tool lives in its own folder with sample data so it runs out of
the box.

**Author:** Leah Schulman

## Requirements

Python 3.7 or newer. Every tool uses only the Python standard library, so there
is nothing to install.

```bash
python --version   # confirm 3.7+
```

## Tools

### grade_tracker

Reads a CSV of student scores over time and reports per-student averages,
trends (improving / declining / steady), and a class-wide summary.

```bash
cd grade_tracker
python grade_tracker.py                       # uses sample_scores.csv
python grade_tracker.py --file my_scores.csv  # use your own data
python grade_tracker.py --student "Ava Chen"  # report on one student
```

CSV columns: `student`, `date` (YYYY-MM-DD), `score`.

### invoice_generator

Reads a CSV work log and writes a clean plain-text invoice for a chosen
client. Each line item is `hours × rate`, with an optional tax rate.

```bash
cd invoice_generator
python invoice_generator.py                            # list clients in the file
python invoice_generator.py --client "Lin Family"      # generate an invoice
python invoice_generator.py --client "Lin Family" --tax 8.25
python invoice_generator.py --client "Lin Family" --file my_work.csv
```

CSV columns: `client`, `date` (YYYY-MM-DD), `description`, `hours`, `rate`.
The invoice prints to screen and saves as `invoice_<client>_<date>.txt`.

### capacity_planner

Compares your weekly available hours against a list of client commitments and
reports remaining bandwidth or over-allocation.

```bash
cd capacity_planner
python capacity_planner.py                        # uses sample data, 30h default
python capacity_planner.py --available 25         # set your weekly capacity
python capacity_planner.py --file my_clients.csv --available 40
```

CSV columns: `client`, `weekly_hours`.

## Project layout

```
data-playground/
├── grade_tracker/
│   ├── grade_tracker.py
│   ├── sample_scores.csv
│   ├── requirements.txt
│   └── README.md
├── invoice_generator/
│   ├── invoice_generator.py
│   ├── sample_work.csv
│   ├── requirements.txt
│   └── README.md
└── capacity_planner/
    ├── capacity_planner.py
    ├── sample_commitments.csv
    ├── requirements.txt
    └── README.md
```

Each folder also has its own README with more detail on that tool.