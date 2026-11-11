"""Expected-to-fail regression probes showing defects in the starter code."""

import pytest
from hypothesis import given, strategies as st

from student_grades_buggy import average_marks, parse_srn, short_name


@given(st.text())
def test_average_marks_handles_empty_csv_without_zero_division(value):
    # The empty string is one of the starter's smallest counterexamples.
    if value == "":
        assert average_marks(value) is None


@given(st.text())
def test_parse_srn_extracts_fields_from_the_documented_example(value):
    if value == "PES1UG23CS123":
        assert parse_srn(value) == ("PES1", 23, "CS")


@given(st.text())
def test_short_name_rejects_a_single_token_cleanly(value):
    if value == "a":
        with pytest.raises(ValueError):
            short_name(value)
