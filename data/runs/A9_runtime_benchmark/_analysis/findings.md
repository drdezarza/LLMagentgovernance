**Reviewer-response stage v3** (exploratory, built 2026-11-18 after a third review of v14-2; not part of ANALYSIS_PLAN_v1). Reading rules fixed before any unit ran: reports/prereg/RR_PLAN_v3.md.

Complete governed-message paths, response cache off. Game path = every candidate of a recorded S5i round audited (with the bounded re-ask) plus selection; feeder path = audit, factual rewrite, re-audit, template fallback (S7b message rule) on recorded S7b_C no-governance messages, with the auditor model also writing the rewrite. Latency = wall-clock time of one path; throughput = completed paths per minute in a batch at the given concurrency. Research judge and simulator are not timed. One unit, so no other unit of the pipeline ran concurrently.

| auditor | path | concurrency | paths | failed | p50_s | p90_s | p99_s | max_s | throughput_paths_per_min | calls_per_path | call_errors | invalid_audits | rewrite_share | fallback_share | usd_per_1000_paths |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek_v4_flash | feeder | 1 | 40 | 0 | 0.627 | 0.853 | 2.082 | 2.107 | 85.811 | 1.100 | 0 | 0 | 0.050 | 0.000 | 0.304 |
| deepseek_v4_flash | feeder | 4 | 40 | 0 | 0.564 | 0.773 | 1.745 | 1.787 | 354.565 | 1.100 | 0 | 0 | 0.050 | 0.000 | 0.305 |
| deepseek_v4_flash | feeder | 16 | 40 | 0 | 0.709 | 0.946 | 2.150 | 2.218 | 1072.990 | 1.100 | 0 | 0 | 0.050 | 0.000 | 0.305 |
| deepseek_v4_flash | game | 1 | 40 | 0 | 1.757 | 2.059 | 2.334 | 2.442 | 34.543 | 3.000 | 0 | 0 | 0.000 | 0.000 | 0.404 |
| deepseek_v4_flash | game | 4 | 40 | 0 | 1.756 | 2.207 | 2.690 | 2.791 | 126.282 | 3.000 | 0 | 0 | 0.000 | 0.000 | 0.405 |
| deepseek_v4_flash | game | 16 | 40 | 0 | 1.673 | 1.869 | 2.075 | 2.121 | 466.201 | 3.000 | 0 | 0 | 0.000 | 0.000 | 0.404 |
| deepseek_v4_pro | feeder | 1 | 40 | 0 | 1.486 | 3.210 | 5.711 | 5.861 | 31.625 | 1.150 | 0 | 0 | 0.075 | 0.000 | 1.218 |
| deepseek_v4_pro | feeder | 4 | 40 | 0 | 1.551 | 2.627 | 5.166 | 5.545 | 126.771 | 1.150 | 0 | 0 | 0.075 | 0.000 | 1.221 |
| deepseek_v4_pro | feeder | 16 | 40 | 0 | 2.746 | 7.326 | 15.232 | 17.591 | 117.754 | 1.200 | 0 | 0 | 0.100 | 0.000 | 1.258 |
| deepseek_v4_pro | game | 1 | 40 | 0 | 5.804 | 13.687 | 23.167 | 24.145 | 7.861 | 3.000 | 1 | 0 | 0.000 | 0.000 | 1.796 |
| deepseek_v4_pro | game | 4 | 40 | 0 | 3.055 | 3.297 | 3.651 | 3.685 | 76.177 | 3.000 | 0 | 0 | 0.000 | 0.000 | 1.797 |
| deepseek_v4_pro | game | 16 | 40 | 0 | 5.049 | 5.897 | 8.185 | 9.163 | 128.327 | 3.000 | 0 | 0 | 0.000 | 0.000 | 1.796 |
| glm53 | feeder | 1 | 40 | 0 | 0.751 | 2.428 | 153.382 | 249.166 | 8.314 | 1.325 | 2 | 0 | 0.150 | 0.000 | 1.285 |
| glm53 | feeder | 4 | 40 | 0 | 0.763 | 15.449 | 325.653 | 375.589 | 6.390 | 1.300 | 7 | 0 | 0.125 | 0.025 | 1.311 |
| glm53 | feeder | 16 | 40 | 0 | 0.939 | 138.148 | 248.489 | 248.749 | 9.577 | 1.275 | 19 | 0 | 0.100 | 0.025 | 1.294 |
| glm53 | game | 1 | 40 | 0 | 70.325 | 248.205 | 254.767 | 255.917 | 0.743 | 3.025 | 25 | 0 | 0.000 | 0.000 | 1.563 |
| glm53 | game | 4 | 40 | 0 | 1.902 | 123.831 | 326.665 | 377.219 | 6.362 | 3.050 | 8 | 0 | 0.000 | 0.000 | 1.570 |
| glm53 | game | 16 | 40 | 0 | 2.668 | 249.392 | 377.843 | 378.093 | 6.347 | 3.050 | 29 | 0 | 0.000 | 0.000 | 1.567 |
| minimax_m3 | feeder | 1 | 40 | 0 | 5.593 | 21.260 | 52.580 | 60.944 | 5.667 | 1.600 | 0 | 2 | 0.200 | 0.000 | 1.587 |
| minimax_m3 | feeder | 4 | 40 | 0 | 5.366 | 21.584 | 40.171 | 44.305 | 22.063 | 1.600 | 2 | 1 | 0.125 | 0.075 | 1.694 |
| minimax_m3 | feeder | 16 | 40 | 0 | 7.537 | 95.400 | 122.773 | 124.204 | 19.322 | 1.300 | 0 | 0 | 0.050 | 0.025 | 1.432 |
| minimax_m3 | game | 1 | 40 | 0 | 9.281 | 16.401 | 58.659 | 79.345 | 4.999 | 3.000 | 2 | 0 | 0.000 | 0.000 | 1.680 |
| minimax_m3 | game | 4 | 40 | 0 | 8.430 | 10.596 | 13.515 | 14.337 | 26.955 | 3.000 | 0 | 0 | 0.000 | 0.000 | 1.686 |
| minimax_m3 | game | 16 | 40 | 0 | 10.637 | 14.154 | 16.530 | 16.755 | 69.995 | 3.000 | 0 | 0 | 0.000 | 0.000 | 1.660 |
| qwen38_27b | feeder | 1 | 40 | 0 | 0.456 | 1.283 | 1.631 | 1.674 | 95.622 | 1.300 | 0 | 0 | 0.150 | 0.000 | 0.730 |
| qwen38_27b | feeder | 4 | 40 | 0 | 0.460 | 1.025 | 1.586 | 1.662 | 397.103 | 1.200 | 0 | 0 | 0.100 | 0.000 | 0.679 |
| qwen38_27b | feeder | 16 | 40 | 0 | 0.464 | 1.506 | 1.859 | 1.868 | 1018.288 | 1.250 | 0 | 0 | 0.125 | 0.000 | 0.705 |
| qwen38_27b | game | 1 | 40 | 0 | 1.568 | 1.842 | 2.033 | 2.057 | 38.061 | 3.000 | 0 | 0 | 0.000 | 0.000 | 1.071 |
| qwen38_27b | game | 4 | 40 | 0 | 1.386 | 1.628 | 2.006 | 2.079 | 160.568 | 3.000 | 0 | 0 | 0.000 | 0.000 | 1.072 |
| qwen38_27b | game | 16 | 40 | 0 | 1.387 | 1.742 | 2.303 | 2.566 | 537.528 | 3.000 | 0 | 0 | 0.000 | 0.000 | 1.072 |

**Reading (RR_PLAN_v3)**: descriptive (R-R1 latency distribution, R-R2 throughput and its scaling with concurrency, R-R3 failures, invalid audits, rewrites and fallbacks, R-R4 cost per 1000 governed messages).