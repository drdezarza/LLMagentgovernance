# Paper verification

`numbers.json` maps every number in the revised manuscript (v14-7, November 2026) to the analysis record it comes from:
1430 checks in total. Entries from the first submission are retained; entries added for the revision have ids starting
with `V14_4` or `RR3` and read from the new stages, `reports/rr/`, `reports/rr2/` and `reports/rr3/`. Each entry gives:

| Field | Meaning |
|---|---|
| `id` | Stable identifier, e.g. `S3b.ecs_label.gap` |
| `value` | The value as rounded in the text |
| `kind`, `source`, `where`/`regex`, `column` | Where to read it: a CSV cell (row selected by `where`) or a regex match in a Markdown file |
| `tol` | Allowed absolute difference (rounding) |
| `scale` | Optional multiplier (e.g. 100 for percentages) |
| `used_in` | Section, table or figure locator (from the earlier manuscript draft) |

```bash
python paper/check_numbers.py
# 1430 numbers checked; 0 drifted or missing
```

The checker uses only the Python standard library and reads only `data/runs/*/_analysis/` and `reports/`. Re-running
the analyses (`make analyze`, then `make revision-tables`) and then the checker shows that the published numbers
follow from the saved unit records. `make revision-tables` needs the SQLite ledger, which `make ledger-db` rebuilds
from `data/ledger/calls.csv.gz`.
