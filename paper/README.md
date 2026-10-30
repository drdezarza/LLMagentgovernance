# Paper verification

`numbers.json` lists every number quoted in the final manuscript (604 entries). Each entry gives:

| Field | Meaning |
|---|---|
| `id` | Stable identifier, e.g. `S3b.ecs_label.gap` |
| `value` | The value as rounded in the text |
| `kind`, `source`, `where`/`regex`, `column` | Where to read it: a CSV cell (row selected by `where`) or a regex match in a Markdown file |
| `tol` | Allowed absolute difference (rounding) |
| `scale` | Optional multiplier (e.g. 100 for percentages) |
| `used_in` | Section, table or figure of the manuscript where the number appears |

```bash
python paper/check_numbers.py
# 604 numbers checked; 0 drifted or missing
```

The checker uses only the Python standard library and reads only `data/runs/*/_analysis/` and `reports/`. Re-running
the analyses (`make analyze`) and then the checker shows that the published numbers follow from the saved unit records.
