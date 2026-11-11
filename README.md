# Lab 7 - Fuzz Testing Student Grades

**Student:** Nirav Choudhary  
**SRN:** PES2UG24CS323  
**Course/Lab:** Lab 7 - Fuzzing for Input Validation Bugs

## Project files

- `student_grades_buggy.py` - original buggy program copied from the assigned Lab 7 folder, retained for baseline reproduction.
- `test_student_grades_buggy.py` - Hypothesis tests that demonstrate the original defects.
- `student_grades.py` - hardened implementation.
- `test_student_grades.py` - property-based tests for the corrected implementation.
- `requirements.txt` - Python test dependencies.
- `REPORT.md` - experiment notes and screenshot checklist.

## Run in VS Code (Windows PowerShell)

Open this folder in VS Code, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, use `py -m pip install -r requirements.txt` and replace `pytest` with `py -m pytest` below.

### 1. Reproduce the original program

```powershell
py student_grades_buggy.py
```

Try ordinary values first (`78,85,92`, `PES1UG23CS123`, `ravi kumar`). Then run the buggy tests:

```powershell
py -m pytest -q test_student_grades_buggy.py
```

Some tests are expected to fail: those failures are the evidence of defects in the original implementation.

### 2. Run the fixed program

```powershell
py student_grades.py
```

### 3. Run the fixed implementation's fuzz tests

```powershell
py -m pytest -q test_student_grades.py
```

All tests should pass. Hypothesis generates and shrinks inputs automatically. The suite is property-based; a passing run is evidence for the stated properties, not a mathematical proof that all possible inputs are safe.

## Validation policy

- Marks must be comma-separated integers in the inclusive range 0-100. Empty entries, non-integers, empty input, and out-of-range values are rejected.
- SRNs follow the 13-character pattern illustrated in the lab handout (`PES1UG23CS123`): three campus letters, one campus digit, `UG`, two year digits, two department letters, and three serial digits. The function returns `(campus, year, department)`.
- Names must contain at least two whitespace-separated tokens. The first token provides the initial; the final token provides the surname.

The original source slices the SRN at incorrect positions for the stated example. The corrected parser uses the documented example format and extracts `PES1`, `23`, and `CS` from `PES1UG23CS123`.
