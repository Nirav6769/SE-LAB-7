"""Validated student-grade helpers for Lab 7: Hypothesis fuzz testing."""

import re


def average_marks(marks_csv):
    """Return the mean of comma-separated integer marks.

    Accepts marks from 0 through 100. Whitespace around values is ignored.
    Raises TypeError for non-string input and ValueError for malformed,
    empty, or out-of-range values.
    """
    if not isinstance(marks_csv, str):
        raise TypeError("marks_csv must be a string")

    if not marks_csv.strip():
        raise ValueError("marks_csv must contain at least one mark")

    parts = marks_csv.split(",")
    marks = []
    for part in parts:
        token = part.strip()
        if not token:
            raise ValueError("marks_csv contains an empty mark")
        # Strict integer syntax: reject decimal values and other coercions.
        if not re.fullmatch(r"[+-]?\d+", token):
            raise ValueError("each mark must be an integer")
        mark = int(token)
        if not 0 <= mark <= 100:
            raise ValueError("each mark must be between 0 and 100")
        marks.append(mark)

    return round(sum(marks) / len(marks), 2)


def parse_srn(srn):
    """Parse an SRN such as PES1UG23CS123 into campus, year, department.

    SRN contract used in this lab: 13 characters, four-character campus
    prefix, one-character program marker, two-character course marker,
    two-digit year, two-letter department, and three-digit serial number.
    """
    if not isinstance(srn, str):
        raise TypeError("srn must be a string")

    normalized = srn.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}\dUG\d{2}[A-Z]{2}\d{3}", normalized):
        raise ValueError("srn must match the format PES1UG23CS123")

    campus = normalized[:4]
    year = int(normalized[6:8])
    department = normalized[8:10]
    return campus, year, department


def short_name(full_name):
    """Convert a two-or-more-part name to 'F. Surname'.

    The first token supplies the initial and the final token supplies the
    surname; repeated/leading/trailing whitespace is ignored.
    """
    if not isinstance(full_name, str):
        raise TypeError("full_name must be a string")

    parts = full_name.split()
    if len(parts) < 2:
        raise ValueError("full_name must contain at least a first and last name")

    first = parts[0]
    last = parts[-1]
    return first[0].upper() + ". " + last.capitalize()


def main():
    """Small interactive demonstration with friendly validation errors."""
    demos = (
        ("average_marks", "Enter marks as CSV (e.g. 78,85,92): ", average_marks),
        ("parse_srn", "Enter an SRN (e.g. PES1UG23CS123): ", parse_srn),
        ("short_name", "Enter first and last name (e.g. ravi kumar): ", short_name),
    )
    for label, prompt, function in demos:
        print("\n==== Running {} ====".format(label))
        try:
            result = function(input(prompt))
            print("Result:", result)
        except (TypeError, ValueError) as exc:
            print("Invalid input:", exc)


if __name__ == "__main__":
    main()
