# Paper verification

`numbers.json` maps every number in the submitted manuscript (v14-1) to the analysis record it comes from: 416 numbers
quoted in the text, plus 71 entries from earlier drafts kept for provenance (`quoted: false`), 487 entries in total.
Each entry gives:

| Field | Meaning |
|---|---|
| `id` | Stable identifier, e.g. `S3b.ecs_label.gap` |
| `value` | The value as rounded in the text |
| `kind`, `source`, `where`/`regex`, `column` | Where to read it: a CSV cell (row selected by `where`) or a regex match in a Markdown file |
| `tol` | Allowed absolute difference (rounding) |
| `scale` | Optional multiplier (e.g. 100 for percentages) |
| `quoted` | Whether the number appears in the submitted text |
| `used_in` | Section, table or figure locator (from the earlier manuscript draft) |

```bash
python paper/check_numbers.py
# 487 numbers checked; 0 drifted or missing
```

The checker uses only the Python standard library and reads only `data/runs/*/_analysis/` and `reports/`. Re-running
the analyses (`make analyze`) and then the checker shows that the published numbers follow from the saved unit records.
