# Lab 7 Report - Fuzzing for Input Validation Bugs

**Student:** Nirav Choudhary  
**SRN:** PES2UG24CS323  
**Objective:** Apply Hypothesis property-based fuzzing to uncover input-validation defects and harden the supplied Python functions.

## 1. Original application

The assigned starter program contains `average_marks`, `parse_srn`, and `short_name`. The code assumes all inputs have the expected type and format. It does not validate empty CSV tokens, numeric ranges, SRN structure, or the number of name components.

## 2. Fuzzing methodology

Hypothesis strategies generate arbitrary text, lists of valid marks, integers, and combinations of name tokens. Tests express expected properties rather than manually enumerating every input. Pytest runs the tests, and Hypothesis shrinks failing examples to simpler counterexamples.

## 3. Bugs / edge cases explored

| Function | Edge case | Starter-code risk | Corrected behavior |
|---|---|---|---|
| `average_marks` | Empty string | Division by zero | Reject with `ValueError` |
| `average_marks` | `1,,3` | Empty token causes conversion error | Reject with `ValueError` |
| `average_marks` | Text / decimal token | Conversion error / unclear contract | Reject with `ValueError` |
| `average_marks` | Negative or above 100 | Accepts invalid marks | Reject with `ValueError` |
| `average_marks` | `None` or non-string | Attribute error | Reject with `TypeError` |
| `parse_srn` | Short / malformed SRN | May slice invalid positions or fail conversion | Validate complete format first |
| `parse_srn` | Example SRN `PES1UG23CS123` | Original slices return incorrect fields | Return `('PES1', 23, 'CS')` |
| `short_name` | Empty / one-token name | Unpacking error | Reject with `ValueError` |
| `short_name` | Extra whitespace / middle names | Fragile unpacking | Use first and final tokens |
| All | Non-string input | Incidental runtime exception | Reject with `TypeError` |

## 4. Fixes implemented

- Added explicit input type checks.
- Validated CSV structure, integer syntax, non-empty entries, and mark bounds.
- Validated the complete SRN format before extracting fields.
- Corrected SRN extraction to match the sample in the assignment.
- Normalized whitespace in names and made the first/last-token rule explicit.
- Added a friendly interactive error message so invalid input does not terminate the demo unexpectedly.

## 5. Test results

Run the original baseline tests:

```powershell
py -m pytest -q test_student_grades_buggy.py
```

The baseline tests are deliberately expected to fail, demonstrating the starter defects.

Run the hardened implementation tests:

```powershell
py -m pytest -q test_student_grades.py
```

The corrected test suite should pass. Record the actual terminal summary in the screenshot below; do not write a test count until it is produced by your run.

## 6. Screenshots to capture

Add genuine screenshots from your own VS Code terminal (do not fabricate terminal output):

1. `screenshots/01_original_program.png` - run `py student_grades_buggy.py` with normal sample inputs.
2. `screenshots/02_failing_fuzz_tests.png` - run `py -m pytest -q test_student_grades_buggy.py` and show baseline failures.
3. `screenshots/03_fixed_program.png` - run `py student_grades.py` with valid inputs.
4. `screenshots/04_passing_fuzz_tests.png` - run `py -m pytest -q test_student_grades.py` and show passing summary.

## 7. Conclusion

Property-based fuzzing helps discover edge cases that a few manually selected examples may miss. Explicit validation and clear exception contracts make the functions more predictable. Hypothesis supplements conventional examples by generating many inputs and shrinking failures to understandable cases.
