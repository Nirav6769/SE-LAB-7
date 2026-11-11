"""Property-based fuzz tests for student_grades.py."""

import pytest
from hypothesis import given, strategies as st

from student_grades import average_marks, parse_srn, short_name


# ---------- average_marks ----------

@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1).map(
    lambda values: ",".join(map(str, values))
))
def test_average_marks_valid_input_matches_reference(csv_marks):
    values = [int(item) for item in csv_marks.split(",")]
    assert average_marks(csv_marks) == round(sum(values) / len(values), 2)


@given(st.text())
def test_average_marks_arbitrary_text_is_either_valid_or_rejected_cleanly(value):
    try:
        result = average_marks(value)
    except ValueError:
        return
    values = [int(item.strip()) for item in value.split(",")]
    assert values and all(0 <= mark <= 100 for mark in values)
    assert result == round(sum(values) / len(values), 2)


@given(st.one_of(st.none(), st.integers(), st.lists(st.integers())))
def test_average_marks_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        average_marks(value)


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1).map(
    lambda values: ", ".join(map(str, values))
))
def test_average_marks_accepts_whitespace_around_valid_values(csv_marks):
    assert isinstance(average_marks(csv_marks), float)


@given(st.integers().filter(lambda n: n < 0 or n > 100))
def test_average_marks_rejects_out_of_range_marks(mark):
    with pytest.raises(ValueError):
        average_marks(str(mark))


# ---------- parse_srn ----------

@given(st.integers(min_value=0, max_value=99), st.sampled_from(["CS", "EC", "ME", "IS", "AI"]))
def test_parse_srn_valid_format_extracts_fields(year, department):
    srn = "PES1UG{:02d}{}123".format(year, department)
    campus, parsed_year, parsed_department = parse_srn(srn)
    assert campus == "PES1"
    assert parsed_year == year
    assert parsed_department == department


@given(st.text())
def test_parse_srn_arbitrary_text_is_rejected_or_correctly_parsed(value):
    try:
        result = parse_srn(value)
    except ValueError:
        return
    normalized = value.strip().upper()
    assert len(normalized) == 13
    assert normalized[:3].isalpha() and normalized[3].isdigit()
    assert normalized[4:6] == "UG"
    assert normalized[6:8].isdigit()
    assert normalized[8:10].isalpha()
    assert normalized[10:13].isdigit()
    assert result == (normalized[:4], int(normalized[6:8]), normalized[8:10])


@given(st.one_of(st.none(), st.integers(), st.lists(st.text())))
def test_parse_srn_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        parse_srn(value)


# ---------- short_name ----------

@given(st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
       st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1))
def test_short_name_uses_first_initial_and_last_token(first, last):
    assert short_name(first + " " + last) == first[0].upper() + ". " + last.capitalize()


@given(st.text())
def test_short_name_rejects_single_token_or_empty(value):
    if len(value.split()) < 2:
        with pytest.raises(ValueError):
            short_name(value)
    else:
        assert isinstance(short_name(value), str)


@given(st.one_of(st.none(), st.integers(), st.lists(st.text())))
def test_short_name_rejects_non_string_input(value):
    with pytest.raises(TypeError):
        short_name(value)


@given(st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
       st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
       st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1))
def test_short_name_uses_last_token_as_surname(first, middle, last):
    assert short_name("{} {} {}".format(first, middle, last)) == first[0].upper() + ". " + last.capitalize()
