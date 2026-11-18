# Cache-replay audit of feeder cells (RR_PLAN_v2 amendment 1; no API calls)

Each recorded cell re-run with the current code, every model call answered from the LLM cache. 'exact' = replayed objective equals the recorded one to 1e-6. Differences come from the pre-2026-11-17 cache race (parallel units sending the same prompt; the cache kept the last answer).

| study | cells | replayed | exact | max_abs_dev | median_abs_dev_if_differs |
|---|---|---|---|---|---|
| S7b_C | 120 | 117 | 100 | 92.38 | 20.55 |
| S7b_mechanism_ablation | 180 | 175 | 162 | 16.46 | 7.07 |
| S7c_nonresponse | 360 | 347 | 329 | 70.23 | 11.00 |
| S7d_search_mechanism | 240 | 177 | 175 | 26.50 | 16.56 |
