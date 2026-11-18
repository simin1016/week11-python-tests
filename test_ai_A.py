import pytest

from load_scores import load_scores


def test_reads_valid_rows_and_ignores_first_row(tmp_path):
    scores_file = tmp_path / "valid.csv"
    scores_file.write_text(
        "name,score\nAlice,85\nBob,90\n",
        encoding="utf-8",
    )

    assert load_scores(scores_file) == ([("Alice", 85), ("Bob", 90)], [])


def test_strips_whitespace_from_names_and_scores(tmp_path):
    scores_file = tmp_path / "whitespace.csv"
    scores_file.write_text("name,score\n Alice , 42 \n", encoding="utf-8")

    assert load_scores(scores_file) == ([("Alice", 42)], [])


def test_ignores_empty_csv_rows(tmp_path):
    scores_file = tmp_path / "empty_rows.csv"
    scores_file.write_text("name,score\n\nAlice,42\n", encoding="utf-8")

    assert load_scores(scores_file) == ([("Alice", 42)], [])


def test_records_rows_with_wrong_column_count(tmp_path):
    scores_file = tmp_path / "wrong_columns.csv"
    scores_file.write_text(
        "name,score\nSolo\nAlice,42,extra\n",
        encoding="utf-8",
    )

    assert load_scores(scores_file) == (
        [],
        [
            (2, "Solo", "열 개수가 2가 아님"),
            (3, "Alice,42,extra", "열 개수가 2가 아님"),
        ],
    )


def test_records_empty_name_and_empty_score(tmp_path):
    scores_file = tmp_path / "empty_fields.csv"
    scores_file.write_text(
        "name,score\n,10\nAlice,\n",
        encoding="utf-8",
    )

    assert load_scores(scores_file) == (
        [],
        [
            (2, ",10", "이름이 비어 있음"),
            (3, "Alice,", "점수가 비어 있음"),
        ],
    )


def test_records_non_integer_scores(tmp_path):
    scores_file = tmp_path / "non_integer.csv"
    scores_file.write_text("name,score\nAlice,abc\n", encoding="utf-8")

    assert load_scores(scores_file) == (
        [],
        [(2, "Alice,abc", "점수가 정수가 아님")],
    )


def test_records_scores_outside_zero_to_one_hundred(tmp_path):
    scores_file = tmp_path / "out_of_range.csv"
    scores_file.write_text(
        "name,score\nAlice,-1\nBob,101\n",
        encoding="utf-8",
    )

    assert load_scores(scores_file) == (
        [],
        [
            (2, "Alice,-1", "점수가 0~100 밖"),
            (3, "Bob,101", "점수가 0~100 밖"),
        ],
    )


def test_raises_file_not_found_for_missing_path(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")
