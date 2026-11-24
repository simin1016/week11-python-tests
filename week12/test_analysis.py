from pathlib import Path

from week12.analysis import class_statistics, group_scores, load_data, 정제


WEEK12_DIR = Path(__file__).parent
scores = 정제(load_data(WEEK12_DIR / "scores_2026.csv"))
mini = 정제(load_data(WEEK12_DIR / "mini.csv"))


def test_scores_clean_to_100_rows():
    assert len(scores) == 100


def test_scores_have_only_two_classes():
    assert set(scores["반"]) == {"1반", "2반"}


def test_grouped_score_sum_matches_total():
    _, subject_class_groups = group_scores(scores)
    assert subject_class_groups["합계"].sum() == scores["점수"].sum()


def test_total_score_is_7484():
    assert scores["점수"].sum() == 7484


def test_mini_cleans_to_7_rows():
    assert len(mini) == 7


def test_mini_class_1_average_is_80():
    statistics = class_statistics(mini)
    assert statistics.loc["1반", "평균"] == 80


def test_mini_class_2_average_is_70():
    statistics = class_statistics(mini)
    assert statistics.loc["2반", "평균"] == 70


def test_subject_class_groups_have_six_combinations():
    _, subject_class_groups = group_scores(scores)
    assert len(subject_class_groups) == 6
