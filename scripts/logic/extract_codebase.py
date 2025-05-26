#!/usr/bin/env python3
import os
import sys
import datetime

EXCLUDED_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "build",
    "dist",
    ".mypy_cache",
    ".pytest_cache",
}

ALLOWED_SUFFIX = ".py"
ENCODING = "utf-8"


def should_exclude_dir(dirname):
    return dirname in EXCLUDED_DIRS


def gather_python_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
        for file in files:
            if file.endswith(ALLOWED_SUFFIX):
                yield os.path.join(root, file)


def write_log(log_path, message):
    with open(log_path, "a", encoding=ENCODING) as log:
        log.write(message + "\n")


def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    suffix = sys.argv[1].strip() if len(sys.argv) >= 2 else ""
    custom_output_name = (
        f"{timestamp}_{suffix}" if suffix else f"{timestamp}_output.txt"
    )

    output_path = os.path.join(script_dir, custom_output_name)
    log_path = os.path.join(script_dir, f"{timestamp}_combine_log.txt")
    search_path = (
        os.path.abspath(sys.argv[2])
        if len(sys.argv) >= 3
        else os.path.abspath(os.path.join(script_dir, "..", ".."))
    )

    if not os.path.isdir(search_path):
        print(f"ERROR: Directory does not exist: {search_path}")
        write_log(log_path, f"ERROR: Directory does not exist: {search_path}")
        sys.exit(1)

    write_log(log_path, f"Start: {datetime.datetime.now()} | Scanning {search_path}")

    file_count = 0
    with open(output_path, "w", encoding=ENCODING) as output_file:
        output_file.write("Merged Python source files\n" + "=" * 30 + "\n\n")
        for file_path in gather_python_files(search_path):
            try:
                with open(file_path, "r", encoding=ENCODING, errors="ignore") as f:
                    content = f.read()
                output_file.write(f"----- {file_path} -----\n{content}\n{'=' * 30}\n\n")
                write_log(log_path, f"✔ Processed: {file_path}")
                file_count += 1
            except Exception as e:
                write_log(log_path, f"✘ ERROR reading {file_path}: {e}")

    result = (
        f"{file_count} files processed." if file_count else "No Python files found."
    )
    print(f"✅ {result}\nOutput: {output_path}\nLog: {log_path}")
    write_log(log_path, f"Done: {datetime.datetime.now()} | {result}")


if __name__ == "__main__":
    main()
