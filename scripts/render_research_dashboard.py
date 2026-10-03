from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
E011 = ROOT / "artifacts/e011/pressure-report.json"
E012 = ROOT / "artifacts/e012/evaluation-design-report.json"
OUT = ROOT / "docs/generated"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rounded_auc(payload: dict) -> dict[str, float]:
    return {
        str(name): round(float(value), 3)
        for name, value in payload["resilience_auc"].items()
    }


def render_e011(payload: dict) -> str:
    auc = _rounded_auc(payload)
    knees = payload["knees"]
    order = sorted(auc, key=lambda name: (-auc[name], name))
    max_value = max(auc.values()) if auc else 1.0

    width = 1040
    height = 120 + 60 * len(order)
    label_x = 32
    bar_x = 250
    bar_width = 650

    rows: list[str] = []
    for index, name in enumerate(order):
        y = 92 + index * 60
        value = auc[name]
        shown = int(round(bar_width * value / max_value)) if max_value else 0
        knee = knees.get(name)
        knee_text = "n/a" if knee is None else str(knee)
        rows.append(
            f'<text x="{label_x}" y="{y + 20}" class="label">{html.escape(name)}</text>'
            f'<rect x="{bar_x}" y="{y}" width="{bar_width}" height="28" rx="14" class="track"/>'
            f'<rect x="{bar_x}" y="{y}" width="{shown}" height="28" rx="14" class="bar"/>'
            f'<text x="{bar_x + bar_width + 18}" y="{y + 20}" class="value">'
            f'AUC {value:.3f} · knee {knee_text}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E011 pressure resilience</title>
<desc id="desc">Normalized survival area and preliminary pressure knee by allocation mechanism.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .label {{ font: 600 16px Inter,Segoe UI,Arial,sans-serif; fill: #e5edf8; }}
  .value {{ font: 14px Inter,Segoe UI,Arial,sans-serif; fill: #bfd0e6; }}
  .track {{ fill: #26354d; }}
  .bar {{ fill: url(#g); }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#132d31"/>
  </linearGradient>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8b5cf6"/>
    <stop offset=".55" stop-color="#06b6d4"/>
    <stop offset="1" stop-color="#22c55e"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="32" y="42" class="title">E011 · Pressure Resilience</text>
<text x="32" y="68" class="sub">Synthetic stress ladder · normalized survival area · first level below 90% observed survival</text>
{''.join(rows)}
</svg>
'''


def render_e012(payload: dict) -> str:
    winner = str(payload["winner_design"])
    results = payload["results"]
    width = 1040
    height = 330
    card_width = 300
    gap = 28
    start_x = 32

    cards: list[str] = []
    for index, row in enumerate(results):
        design = str(row["design_name"])
        mechanism = str(row["selected_mechanism"])
        x = start_x + index * (card_width + gap)
        winning = design == winner
        card_class = "winner" if winning else "card"
        kicker = "META WINNER" if winning else "EVALUATION DESIGN"
        cards.append(
            f'<rect x="{x}" y="112" width="{card_width}" height="150" rx="18" class="{card_class}"/>'
            f'<text x="{x + 22}" y="145" class="kicker">{kicker}</text>'
            f'<text x="{x + 22}" y="180" class="design">{html.escape(design)}</text>'
            f'<text x="{x + 22}" y="212" class="small">selected</text>'
            f'<text x="{x + 22}" y="242" class="mechanism">{html.escape(mechanism)}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E012 evaluator meta-improvement</title>
<desc id="desc">Evaluation curricula and the allocation mechanism each selected. The winning curriculum is highlighted.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .card {{ fill: #111b2d; stroke: #34445f; stroke-width: 1.5; }}
  .winner {{ fill: #102722; stroke: #22c55e; stroke-width: 2; }}
  .kicker {{ font: 700 12px Inter,Segoe UI,Arial,sans-serif; fill: #8da3bf; letter-spacing: 1.1px; }}
  .design {{ font: 700 21px Inter,Segoe UI,Arial,sans-serif; fill: #edf5ff; }}
  .small {{ font: 13px Inter,Segoe UI,Arial,sans-serif; fill: #8da3bf; }}
  .mechanism {{ font: 650 18px Inter,Segoe UI,Arial,sans-serif; fill: #9ef0bd; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#172554"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="32" y="42" class="title">E012 · Evaluator Meta-Improvement</text>
<text x="32" y="68" class="sub">Which test curriculum chooses a mechanism that generalizes to an unseen, longer stress holdout?</text>
{''.join(cards)}
<text x="32" y="302" class="sub">Winner: {html.escape(winner)} → {html.escape(str(payload["winner_mechanism"]))}</text>
</svg>
'''


def render_markdown(e011: dict, e012: dict) -> str:
    auc = _rounded_auc(e011)
    knees = e011["knees"]
    order = sorted(auc, key=lambda name: (-auc[name], name))
    rows = "\n".join(
        f"| {name} | {auc[name]:.3f} | {knees.get(name, 'n/a')} |"
        for name in order
    )
    design_rows = "\n".join(
        f"| {row['design_name']} | {row['selected_mechanism']} |"
        for row in e012["results"]
    )
    return f"""# Generated research dashboard

> Generated from E011/E012 report JSON by `scripts/render_research_dashboard.py`.
> Do not hand-edit this file.

## E011 — pressure resilience

![E011 pressure resilience](e011-pressure.svg)

| Mechanism | Survival AUC | Preliminary knee |
| --- | ---: | ---: |
{rows}

## E012 — evaluator meta-improvement

![E012 evaluator meta-improvement](e012-evaluator.svg)

| Evaluation curriculum | Mechanism selected |
| --- | --- |
{design_rows}

**Outer winner:** {e012['winner_design']} → {e012['winner_mechanism']}

These are model-relative synthetic results. They are not real-market recommendations.
"""


def generated_files(e011: dict, e012: dict) -> dict[Path, str]:
    return {
        OUT / "e011-pressure.svg": render_e011(e011),
        OUT / "e012-evaluator.svg": render_e012(e012),
        OUT / "research-dashboard.md": render_markdown(e011, e012),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if committed dashboard files differ from generated experiment output.",
    )
    args = parser.parse_args()

    e011 = _read(E011)
    e012 = _read(E012)
    outputs = generated_files(e011, e012)

    if args.check:
        stale: list[str] = []
        for path, content in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            raise SystemExit(
                "research dashboard is stale; regenerate and commit: "
                + ", ".join(stale)
            )
        print("research dashboard matches experiment output")
        return

    OUT.mkdir(parents=True, exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
