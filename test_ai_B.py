import pytest

from load_scores import load_scores


def test_loads_valid_score_rows(tmp_path):
    scores_file = tmp_path / "valid_scores.csv"
    scores_file.write_text(
        "name,score\nAlice,85\nBob,90\n",
        encoding="utf-8",
    )

    assert load_scores(scores_file) == ([("Alice", 85), ("Bob", 90)], [])


def test_loads_name_with_quoted_comma(tmp_path):
    scores_file = tmp_path / "comma_in_name.csv"
    scores_file.write_text(
        'name,score\n"Smith, Jane",75\n',
        encoding="utf-8",
    )

    assert load_scores(scores_file) == ([("Smith, Jane", 75)], [])


def test_blank_line_does_not_discard_valid_rows(tmp_path):
    scores_file = tmp_path / "blank_line.csv"
    scores_file.write_text(
        "name,score\nAlice,85\n\nBob,90\n",
        encoding="utf-8",
    )

    scores, _skipped = load_scores(scores_file)

    assert scores == [("Alice", 85), ("Bob", 90)]


def test_wrong_column_counts_are_recorded_as_skipped(tmp_path):
    scores_file = tmp_path / "wrong_columns.csv"
    scores_file.write_text(
        "name,score\nOnlyName\nToo,Many,Columns\n",
        encoding="utf-8",
    )

    _scores, skipped = load_scores(scores_file)

    assert len(skipped) == 2


def test_zero_is_an_inclusive_valid_lower_boundary(tmp_path):
    scores_file = tmp_path / "zero_boundary.csv"
    scores_file.write_text("name,score\nAlice,0\n", encoding="utf-8")

    assert load_scores(scores_file) == ([("Alice", 0)], [])


def test_one_hundred_is_an_inclusive_valid_upper_boundary(tmp_path):
    scores_file = tmp_path / "hundred_boundary.csv"
    scores_file.write_text("name,score\nAlice,100\n", encoding="utf-8")

    assert load_scores(scores_file) == ([("Alice", 100)], [])


def test_scores_outside_inclusive_range_are_skipped(tmp_path):
    scores_file = tmp_path / "out_of_range.csv"
    scores_file.write_text(
        "name,score\nBelow,-1\nAbove,101\n",
        encoding="utf-8",
    )

    scores, skipped = load_scores(scores_file)

    assert scores == []
    assert len(skipped) == 2


def test_missing_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")
