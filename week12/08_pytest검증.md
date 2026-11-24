# 12주차 STEP 4 pytest 자동 검증 결과

실행 명령:

```text
C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe -m pytest -v --color=no week12\test_analysis.py
```

| 테스트 | 결과 |
|---|---|
| `test_scores_clean_to_100_rows` | PASS |
| `test_scores_have_only_two_classes` | PASS |
| `test_grouped_score_sum_matches_total` | PASS |
| `test_total_score_is_7484` | PASS |
| `test_mini_cleans_to_7_rows` | PASS |
| `test_mini_class_1_average_is_80` | PASS |
| `test_mini_class_2_average_is_70` | PASS |
| `test_subject_class_groups_have_six_combinations` | PASS |

**총 8개, 통과 8개, 실패 0개.** pytest 실행 결과는 `8 passed in 0.70s`였습니다.
