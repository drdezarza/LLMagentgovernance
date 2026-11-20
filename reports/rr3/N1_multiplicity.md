# N1: family-wise sensitivity analysis of the confirmatory claims (RR_PLAN_v3; no API calls)

The planned readout is unchanged. Family = C1, C2, C3, C4, C5a, C5b (K = 6). Components recomputed with the frozen data, resampling units and bootstrap (5000, seed 42); every recomputed 95% interval matches the recorded one: **True**. Bonferroni intervals are two-sided 99.17% percentile intervals; each component is tested against its own claim threshold.

| claim | component | n | estimate | criterion | 95% interval | Bonferroni interval | bootstrap p |
|---|---|---|---|---|---|---|---|
| C1 | ecs_text | 18 | +0.143 | lower limit > 0 | [+0.120, +0.166] | [+0.114, +0.173] | < 0.0002 |
| C1 | integrity_text | 18 | +0.650 | lower limit > 0 | [+0.553, +0.761] | [+0.522, +0.792] | < 0.0002 |
| C2 | label ASR given submission, R1 | 4 | +0.640 | lower limit > 0.3 | [+0.610, +0.670] | [+0.610, +0.670] | < 0.0002 |
| C2 | label ASR given submission, R2 | 4 | +0.990 | lower limit > 0.3 | [+0.970, +1.000] | [+0.970, +1.000] | < 0.0002 |
| C2 | label ASR given submission, R3 | 4 | +0.857 | lower limit > 0.3 | [+0.782, +0.929] | [+0.772, +0.939] | < 0.0002 |
| C3 | label - audit ASR per round, pooled | 12 | +0.717 | lower limit > 0 | [+0.630, +0.807] | [+0.607, +0.840] | < 0.0002 |
| C4 | raw memory - audit misclassification, pooled | 12 | +0.463 | lower limit > 0.1 | [+0.307, +0.600] | [+0.247, +0.637] | < 0.0002 |
| C5a | Gmsg - G0 objective, pooled over plans | 15 | -10.283 | upper limit < 25 | [-20.091, -1.118] | [-23.836, +1.593] | < 0.0002 |
| C5b | Gmsg - G0 content_integrity, pooled over plans | 15 | +0.078 | lower limit > 0 | [+0.042, +0.113] | [+0.029, +0.127] | < 0.0002 |

**Claim level** (composite claims: largest component p; Holm step-down at α = 0.05)

| claim | p (claim) | planned 95% rule | Bonferroni | Holm | note |
|---|---|---|---|---|---|
| C1 | < 0.0002 | met | met | met |  |
| C2 | < 0.0002 | met | met | met |  |
| C3 | < 0.0002 | met | met | met | positive in every rotation: True |
| C4 | < 0.0002 | met | met | met |  |
| C5a | < 0.0002 | met | met | met |  |
| C5b | < 0.0002 | met | met | met |  |

- Claims met under Bonferroni: 6/6; under Holm: 6/6.
- A bootstrap p of '< 0.0002' means no resample crossed the threshold (resolution 1/5000).
- Sensitivity analysis only: it does not replace the frozen decision rule.
