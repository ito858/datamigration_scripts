import logging
import argparse
import os
import time
import sys
import glob
from pathlib import Path

# --- Optimized Color Logger ---
class FastColorFormatter(logging.Formatter):
    COLORS = {
        logging.INFO: "\x1b[34m",    # Blue
        logging.WARNING: "\x1b[33m", # Yellow
        logging.ERROR: "\x1b[31m",   # Red
        'RESET': "\x1b[0m"
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        reset = self.COLORS['RESET']
        return f"{color}{record.levelname}: {record.msg}{reset}"

logger = logging.getLogger("FastAudit")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(FastColorFormatter())
logger.addHandler(ch)

def audit_single_file(file_path: str, delimiter: str, encoding: str):
    """Audits one file and returns (mismatch_count, file_size_mb, duration)"""
    mismatch_count = 0
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    buffer_size = 1024 * 1024

    start_time = time.perf_counter()

    try:
        with open(file_path, mode='r', encoding=encoding, buffering=buffer_size) as f:
            header = f.readline()
            if not header:
                logger.error(f"File '{file_path}' is empty.")
                return 0, 0, 0

            expected_delimiters = header.count(delimiter)
            expected_cols = expected_delimiters + 1

            logger.info(f"Processing: {os.path.basename(file_path)} ({file_size_mb:.2f} MB)")

            for line_num, line in enumerate(f, start=2):
                if line.count(delimiter) != expected_delimiters:
                    mismatch_count += 1
                    actual_cols = line.count(delimiter) + 1
                    status = "LEAKY" if actual_cols > expected_cols else "THIN"

                    logger.warning(
                        f"  [{os.path.basename(file_path)}] Line {line_num} {status} | "
                        f"Expected {expected_cols}, Got {actual_cols}"
                    )

        duration = time.perf_counter() - start_time
        return mismatch_count, file_size_mb, duration

    except Exception as e:
        logger.error(f"Failed to process '{file_path}': {e}")
        return -1, 0, 0

def main():
    parser = argparse.ArgumentParser(description="Fast CSV Audit.")
    # nargs='*' means 0 or more files are acceptable
    parser.add_argument("inputs", nargs='*', help="CSV files or leave empty for all CSVs in dir")
    parser.add_argument("--delimiter", default="|", help="Delimiter (default: |)")
    parser.add_argument("--encoding", default="latin-1", help="Encoding (default: latin-1)")
    args = parser.parse_args()

    input_files = []

# 1. Check for Command Line Arguments
    if args.inputs:
        input_files = args.inputs

    # 2. Check for Piped Input (Standard Input)
    elif not sys.stdin.isatty():
        input_files = [line.strip() for line in sys.stdin if line.strip()]

    # 3. Fallback: Search current directory (Case Insensitive)
    else:
        logger.info("No inputs provided. Scanning current directory for files ending in .csv...")
        # Path.cwd().glob handles Windows paths and case sensitivity better
        input_files = [str(p) for p in Path('.').iterdir() if p.suffix.lower() == '.csv']

        # Debugging line to see what was found
        if input_files:
            logger.info(f"Found {len(input_files)} files: {', '.join([os.path.basename(f) for f in input_files])}")

    if not input_files:
        logger.error(f"No CSV files found in: {os.getcwd()}")
        return

    total_mismatches = 0
    total_mb = 0
    total_time = 0
    files_processed = 0

    print("=" * 50)
    for file_path in input_files:
        if os.path.exists(file_path):
            mismatches, mb, duration = audit_single_file(file_path, args.delimiter, args.encoding)
            if mismatches != -1:
                total_mismatches += mismatches
                total_mb += mb
                total_time += duration
                files_processed += 1
        else:
            logger.error(f"File not found: {file_path}")

    # Final Summary Report
    print("=" * 50)
    if files_processed > 0:
        throughput = total_mb / total_time if total_time > 0 else 0
        logger.info(f"Summary: Processed {files_processed} files ({total_mb:.2f} MB)")
        logger.info(f"Total Time: {total_time:.2f}s | Avg Throughput: {throughput:.2f} MB/s")

        if total_mismatches == 0:
            logger.info("RESULT: All files passed successfully.")
        else:
            logger.error(f"RESULT: Found {total_mismatches} total mismatched lines across all files.")
    else:
        logger.error("No files were successfully processed.")

if __name__ == "__main__":
    main()
