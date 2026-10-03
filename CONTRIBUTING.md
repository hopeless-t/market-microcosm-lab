# Contributing

Thanks for helping improve Market Microcosm Lab.

This repository is a research system, so contributions are evaluated on both **usefulness** and **epistemic discipline**.

## Useful contributions

Good contributions include a new falsifiable market mechanism, stress world, exact small-world checker, failure biopsy, evaluator, meta-evaluator, reproducibility improvement, accounting fix, or clearer statement of assumptions and limits.

## Research contribution contract

Every experiment-changing pull request should answer:

1. What question does this change test?
2. What hypothesis could be falsified?
3. What world/model version is used?
4. Which seeds/data are discovery, promotion, and meta-holdout?
5. Which hard constraints are protected?
6. What evidence would cause rejection?
7. Can the result be replayed?

## Local setup

```bash
python -m pip install -e ".[dev]"
pytest -q
python scripts/run_e000.py
python scripts/run_e010.py
python scripts/run_e011.py
python scripts/run_e012.py
```

## Research style

Keep failure cases. Prefer explicit assumptions to hidden defaults. Keep a slow reference implementation before optimizing. Separate model-relative findings from real-world claims. Treat visualizations as aids rather than evidence. Candidate-generation code must not certify its own candidate.

See `spec/ROOT_OF_TRUST.md`, `docs/VALIDATION.md`, and `docs/THREATS_TO_VALIDITY.md`.
