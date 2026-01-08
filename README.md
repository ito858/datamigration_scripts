# Data Migration Scripts

A collection of Python scripts for auditing and cleaning CSV files during data migration processes. These tools are designed to handle common issues like column mismatches and SQLCMD-specific formatting.

## Scripts Overview

### 1. `audit_csv.py`

This script audits CSV files to identify rows where the column count differs from the header. It is optimized for performance and can handle large files.

#### Capabilities:
- **Fast Execution**: Uses buffering for high-speed processing.
- **Colorized Logging**: Provides clear, color-coded feedback for errors and warnings.
- **Flexible Input**: Supports direct file paths, directory scans, and piped input.

#### Usage:
```bash
python audit_csv.py [files...] [--delimiter DELIMITER] [--encoding ENCODING]
```

#### Parameters:
- `files...`: Optional list of files to audit. If empty, scans the current directory for `.csv` files.
- `--delimiter`: Character used as column separator (default: `|`).
- `--encoding`: File encoding (default: `latin-1`).

#### Examples:
- **Audit specific files:**
  ```bash
  python audit_csv.py data_part1.csv data_part2.csv
  ```
- **Audit all CSVs in the current directory with a custom delimiter:**
  ```bash
  python audit_csv.py --delimiter ","
  ```
- **Using piped input (process output from another command):**
  ```bash
  dir /b *.csv | python audit_csv.py
  ```

---

### 2. `clean_csv_headers.py`

A utility to clean CSV files exported from SQLCMD. It removes the dashed separator line typically found as the second line in such exports.

#### Capabilities:
- **Auto-Detection**: Attempts multiple encodings (`utf-8`, `cp1252`, `latin-1`, `utf-16`) to ensure successful reading.
- **Smart Cleanup**: Identifies and removes lines containing only dashes, pipes, and whitespace (common in SQLCMD outputs).
- **Standardization**: Saves cleaned files as `UTF-8` for maximum compatibility.

#### Usage:
Simply run the script in the directory containing your CSV files:
```bash
python clean_csv_headers.py
```

#### What it does:
1. Scans the current directory for all `.csv` files.
2. For each file, it checks if the second line is a separator (e.g., `-------|-------`).
3. If found, it removes that line and saves the file back to disk.

---

## Requirements

- Python 3.x
- Standard library modules (no external dependencies required)
