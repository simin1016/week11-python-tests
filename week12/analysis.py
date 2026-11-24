import pandas as pd


def load_data(path):
    """CSV 파일을 UTF-8로 읽어 DataFrame으로 반환한다."""
    return pd.read_csv(path, encoding="utf-8")


def 정제(df):
    """명세에 따라 복사본의 점수 데이터를 정제한다."""
    cleaned = df.copy()
    print(f"시작: 남은 행 {len(cleaned)}개, 삭제 행 0개")

    # 점수가 비어 있는 행을 먼저 삭제한다.
    before = len(cleaned)
    cleaned = cleaned.dropna(subset=["점수"])
    print(f"빈 점수 제거: 남은 행 {len(cleaned)}개, 삭제 행 {before - len(cleaned)}개")

    # 모든 열이 완전히 같은 중복 행을 제거한다.
    before = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    print(f"중복 제거: 남은 행 {len(cleaned)}개, 삭제 행 {before - len(cleaned)}개")

    # 반과 과목 값의 앞뒤 공백을 제거한다.
    cleaned["반"] = cleaned["반"].str.strip()
    cleaned["과목"] = cleaned["과목"].str.strip()
    print(f"공백 제거: 남은 행 {len(cleaned)}개, 삭제 행 0개")

    # 점수가 0~100 범위를 벗어나는 행을 삭제한다.
    before = len(cleaned)
    cleaned = cleaned[cleaned["점수"].between(0, 100)].copy()
    print(f"점수 범위 밖 제거: 남은 행 {len(cleaned)}개, 삭제 행 {before - len(cleaned)}개")

    return cleaned


def filter_math(df):
    """정제된 데이터에서 수학 과목의 행만 반환한다."""
    filtered = df[df["과목"] == "수학"].copy()
    print(f"수학 필터링: 전 {len(df)}행, 후 {len(filtered)}행")
    return filtered


def group_scores(df):
    """정제된 전체 데이터를 반 및 과목·반 기준으로 그룹화한다."""
    class_groups = (
        df.groupby("반")["점수"]
        .agg(["mean", "count", "sum"])
        .rename(columns={"mean": "평균", "count": "개수", "sum": "합계"})
    )
    subject_class_groups = (
        df.groupby(["과목", "반"])["점수"]
        .agg(["mean", "count", "sum"])
        .rename(columns={"mean": "평균", "count": "개수", "sum": "합계"})
    )

    grouped_score_sum = subject_class_groups["합계"].sum()
    total_score_sum = df["점수"].sum()
    grouped_row_count = subject_class_groups["개수"].sum()

    if len(subject_class_groups) != 6:
        raise AssertionError(f"과목·반 조합이 6개가 아닙니다: {len(subject_class_groups)}개")
    if grouped_score_sum != total_score_sum:
        raise AssertionError("그룹별 점수 합계와 전체 점수 합계가 다릅니다.")
    if grouped_row_count != len(df):
        raise AssertionError("그룹별 행 개수 합계와 전체 행 개수가 다릅니다.")

    print("반별 그룹 결과:")
    print(class_groups.to_string(float_format=lambda value: f"{value:.2f}"))
    print("과목·반별 그룹 결과:")
    print(subject_class_groups.to_string(float_format=lambda value: f"{value:.2f}"))
    print(f"그룹별 점수 합계: {grouped_score_sum} / 전체 점수 합계: {total_score_sum} (일치)")
    print(f"그룹별 행 개수 합계: {grouped_row_count} / 전체 행 개수: {len(df)} (일치)")

    return class_groups, subject_class_groups


def class_statistics(df):
    """정제된 전체 데이터의 반별 개수, 평균, 중앙값, 최댓값을 계산한다."""
    statistics = (
        df.groupby("반")["점수"]
        .agg(["count", "mean", "median", "max"])
        .rename(columns={"count": "데이터 개수", "mean": "평균", "median": "중앙값", "max": "최댓값"})
    )

    print("반별 통계:")
    print(statistics.to_string(float_format=lambda value: f"{value:.2f}"))
    print(f"전체 행 수: {len(df)}")
    print(f"전체 점수 합계: {df['점수'].sum()}")

    return statistics


if __name__ == "__main__":
    scores = load_data(r"week12\scores_2026.csv")
    cleaned = 정제(scores)
    filter_math(cleaned)
    group_scores(cleaned)
