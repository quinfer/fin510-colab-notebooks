Mirrored dataset for Hilpisch notebooks

This folder contains a local mirror of the CSV expected by the companion notebooks:

- `tr_eikon_eod_data.csv` — end‑of‑day sample data as used in the book notebooks

Populate/update locally

```bash
make fetch-hilpisch-data
```

The Makefile target downloads the pinned version from the upstream repository. Commit the CSV if you want it available via the website and for Colab users.

License/attribution
- Source: https://github.com/yhilpisch/py4fi2nd (pinned to commit 5995cc9)
- Copyright remains with the original author/publisher. This mirror is for educational use within this course.

