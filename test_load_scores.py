import pytest

from load_scores import load_scores


def test_load_scores_reads_regular_score_file(tmp_path):
    scores_file = tmp_path / "scores.csv"
    scores_file.write_text(
        "name,score\n민수,85\n지수,90\n",
        encoding="utf-8",
    )

    assert load_scores(scores_file) == ([("민수", 85), ("지수", 90)], [])


def test_load_scores_skips_blank_line_and_keeps_valid_scores(tmp_path):
    scores_file = tmp_path / "scores_with_blank_line.csv"
    scores_file.write_text(
        "name,score\n민수,85\n\n지수,90\n",
        encoding="utf-8",
    )

    scores, skipped = load_scores(scores_file)

    assert scores == [("민수", 85), ("지수", 90)]
    assert len(skipped) == 1


def test_load_scores_reads_name_containing_comma(tmp_path):
    scores_file = tmp_path / "score_with_comma_in_name.csv"
    scores_file.write_text(
        'name,score\n"홍,길동",75\n',
        encoding="utf-8",
    )

    assert load_scores(scores_file) == ([("홍,길동", 75)], [])


def test_load_scores_raises_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(missing_file)


def test_load_scores_with_header_only_file_has_unspecified_result(tmp_path):
    scores_file = tmp_path / "header_only.csv"
    scores_file.write_text("name,score\n", encoding="utf-8")

    pytest.xfail(
        "명세에 헤더만 있는 파일의 기대 결과나 예외가 정의되어 있지 않음"
    )


@pytest.mark.parametrize(
    ("score", "expected_scores", "expected_skipped_count"),
    [
        (0, [("학생", 0)], 0),
        (100, [("학생", 100)], 0),
        (101, [], 1),
    ],
)
def test_load_scores_handles_score_boundaries(
    tmp_path,
    score,
    expected_scores,
    expected_skipped_count,
):
    scores_file = tmp_path / f"score_{score}.csv"
    scores_file.write_text(
        f"name,score\n학생,{score}\n",
        encoding="utf-8",
    )

    scores, skipped = load_scores(scores_file)

    assert scores == expected_scores
    assert len(skipped) == expected_skipped_count
