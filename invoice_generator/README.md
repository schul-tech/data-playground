# invoice_generator

Reads a CSV work log and writes a clean, plain-text invoice for a chosen
client. Each line item is `hours × rate`; the script totals the work, applies
an optional tax rate, and saves a `.txt` invoice you can email or print.

## Requirements

Pure Python standard library — no installation needed. Python 3.7+.

## Usage

```bash
# List the clients present in the file
python invoice_generator.py

# Generate an invoice for one client
python invoice_generator.py --client "Lin Family"

# Add a tax rate (percentage)
python invoice_generator.py --client "Lin Family" --tax 8.25

# Use your own work log
python invoice_generator.py --client "Lin Family" --file my_work.csv
```

## Input format

The CSV must have these columns:

| column      | description                     |
| ----------- | ------------------------------- |
| client      | client name                     |
| date        | work date as `YYYY-MM-DD`       |
| description | short description of the work   |
| hours       | hours worked (numeric)          |
| rate        | hourly rate in dollars (numeric)|

See `sample_work.csv` for an example. Malformed rows are skipped with a
warning.

## Output

The invoice is printed to the screen and saved as
`invoice_<client>_<date>.txt` in the current folder.
