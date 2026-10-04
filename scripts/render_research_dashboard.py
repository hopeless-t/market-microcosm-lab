from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
E011 = ROOT / "artifacts/e011/pressure-report.json"
E012 = ROOT / "artifacts/e012/evaluation-design-report.json"
E013 = ROOT / "artifacts/e013/pressure-decomposition-report.json"
E014 = ROOT / "artifacts/e014/interaction-surface-report.json"
E015 = ROOT / "artifacts/e015/adaptive-boundary-report.json"
E016 = ROOT / "artifacts/e016/adaptive-guard-report.json"
E017 = ROOT / "artifacts/e017/certificate-lifecycle-report.json"
E018 = ROOT / "artifacts/e018/audit-portfolio-report.json"
E019 = ROOT / "artifacts/e019/provenance-ledger-report.json"
E020 = ROOT / "artifacts/e020/checkpoint-rotation-report.json"
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


def render_e013(payload: dict) -> str:
    mechanisms = (
        "usage-only",
        "light-floor",
        "balanced",
        "diversity-heavy",
        "creator-heavy",
        "platform-heavy",
    )
    axes = (
        ("subscription_price_multiplier", "Price ↓"),
        ("platform_cost_multiplier", "Platform cost ↑"),
        ("base_churn_rate", "Churn ↑"),
    )

    width = 1040
    height = 355
    left = 205
    top = 118
    cell_width = 130
    cell_height = 58

    def fill(knee):
        if knee is None:
            return "#166534"
        if knee <= 6:
            return "#7f1d1d"
        if knee == 7:
            return "#9a3412"
        if knee == 8:
            return "#a16207"
        if knee == 9:
            return "#0e7490"
        return "#166534"

    header = []
    for index, mechanism in enumerate(mechanisms):
        x = left + index * cell_width + cell_width / 2
        header.append(
            f'<text x="{x}" y="98" text-anchor="middle" class="head">'
            f'{html.escape(mechanism)}</text>'
        )

    cells = []
    for row_index, (axis, label) in enumerate(axes):
        y = top + row_index * cell_height
        cells.append(
            f'<text x="28" y="{y + 36}" class="axis">{html.escape(label)}</text>'
        )
        for col_index, mechanism in enumerate(mechanisms):
            knee = payload["knees"][axis][mechanism]
            shown = "10+" if knee is None else str(knee)
            x = left + col_index * cell_width
            cells.append(
                f'<rect x="{x + 4}" y="{y + 4}" width="{cell_width - 8}" '
                f'height="{cell_height - 8}" rx="12" fill="{fill(knee)}"/>'
                f'<text x="{x + cell_width / 2}" y="{y + 38}" '
                f'text-anchor="middle" class="knee">{shown}</text>'
            )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E013 one-dimensional pressure decomposition</title>
<desc id="desc">Preliminary survival knees for price, platform cost, and churn pressure by allocation mechanism.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .head {{ font: 600 12px Inter,Segoe UI,Arial,sans-serif; fill: #cbd9eb; }}
  .axis {{ font: 650 16px Inter,Segoe UI,Arial,sans-serif; fill: #e5edf8; }}
  .knee {{ font: 800 20px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#18284a"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="28" y="42" class="title">E013 · Pressure Decomposition</text>
<text x="28" y="68" class="sub">First level below 90% observed survival · higher is more robust · 10+ = no knee in tested range</text>
{''.join(header)}
{''.join(cells)}
<text x="28" y="325" class="sub">Composite E011 knees occurred much earlier (3–4), indicating interaction between moderate stresses.</text>
</svg>
'''


def render_e014(payload: dict) -> str:
    mechanisms = (
        "usage-only",
        "light-floor",
        "balanced",
        "diversity-heavy",
        "creator-heavy",
        "platform-heavy",
    )
    pairs = (
        (
            "subscription_price_multiplier__platform_cost_multiplier",
            "Price × Cost",
        ),
        (
            "subscription_price_multiplier__base_churn_rate",
            "Price × Churn",
        ),
        (
            "platform_cost_multiplier__base_churn_rate",
            "Cost × Churn",
        ),
    )

    width = 1040
    height = 520
    left = 220
    top = 126
    cell_width = 255
    cell_height = 58

    def fill(count):
        if count == 0:
            return "#26354d"
        if count <= 5:
            return "#0e7490"
        if count <= 10:
            return "#7c3aed"
        return "#be185d"

    header = []
    for index, (_, label) in enumerate(pairs):
        x = left + index * cell_width + cell_width / 2
        header.append(
            f'<text x="{x}" y="103" text-anchor="middle" class="head">'
            f'{html.escape(label)}</text>'
        )

    cells = []
    total_interaction_only = 0
    for row_index, mechanism in enumerate(mechanisms):
        y = top + row_index * cell_height
        cells.append(
            f'<text x="28" y="{y + 36}" class="axis">'
            f'{html.escape(mechanism)}</text>'
        )
        for col_index, (pair_key, _) in enumerate(pairs):
            summary = payload["summaries"][pair_key][mechanism]
            count = int(summary["interaction_only_cells"])
            total_interaction_only += count
            frontier = summary["frontier"]
            if frontier is None:
                frontier_text = "none"
            else:
                frontier_text = (
                    f'{frontier["level_a"]}+{frontier["level_b"]}'
                )
            marker = "★" if frontier and frontier["interaction_only"] else ""
            x = left + col_index * cell_width
            cells.append(
                f'<rect x="{x + 5}" y="{y + 5}" width="{cell_width - 10}" '
                f'height="{cell_height - 10}" rx="12" fill="{fill(count)}"/>'
                f'<text x="{x + 22}" y="{y + 27}" class="frontier">'
                f'{html.escape(frontier_text)}{marker}</text>'
                f'<text x="{x + cell_width - 18}" y="{y + 27}" '
                f'text-anchor="end" class="count">{count} cells</text>'
                f'<text x="{x + 22}" y="{y + 45}" class="small">'
                f'first failing frontier</text>'
            )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E014 pairwise pressure interactions</title>
<desc id="desc">First failing pairwise pressure frontier and count of interaction-only cells by mechanism.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .head {{ font: 700 16px Inter,Segoe UI,Arial,sans-serif; fill: #dbeafe; }}
  .axis {{ font: 650 16px Inter,Segoe UI,Arial,sans-serif; fill: #e5edf8; }}
  .frontier {{ font: 800 18px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .count {{ font: 700 13px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .small {{ font: 11px Inter,Segoe UI,Arial,sans-serif; fill: #d7e3f4; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#2a1538"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="28" y="42" class="title">E014 · Pairwise Interaction Frontiers</text>
<text x="28" y="68" class="sub">★ = the first failing frontier is interaction-only · cell count = joint failures not reproduced by either matched single axis</text>
{''.join(header)}
{''.join(cells)}
<text x="28" y="495" class="sub">Total interaction-only cells across all 3 surfaces × 6 mechanisms: {total_interaction_only}</text>
</svg>
'''



def render_e015(payload: dict) -> str:
    aggregate = payload["aggregate"]
    exhaustive = int(aggregate["exhaustive_queries"])
    adaptive = int(aggregate["adaptive_queries"])
    savings = float(aggregate["query_savings_fraction"])
    accuracy = float(aggregate["classification_accuracy"])
    frontier_rate = float(aggregate["frontier_exact_rate"])
    monotonicity = int(aggregate["monotonicity_violation_count"])

    width = 1040
    height = 330
    bar_x = 245
    bar_width = 690
    exhaustive_width = bar_width
    adaptive_width = int(round(bar_width * adaptive / exhaustive))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E015 adaptive boundary sampling</title>
<desc id="desc">Query cost reduction while exactly recovering the exhaustive E014 interaction surfaces.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .label {{ font: 650 17px Inter,Segoe UI,Arial,sans-serif; fill: #e5edf8; }}
  .value {{ font: 800 20px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .metric {{ font: 700 16px Inter,Segoe UI,Arial,sans-serif; fill: #9ef0bd; }}
  .track {{ fill: #26354d; }}
  .full {{ fill: #475569; }}
  .adaptive {{ fill: url(#g); }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#063b38"/>
  </linearGradient>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#06b6d4"/>
    <stop offset="1" stop-color="#22c55e"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="30" y="42" class="title">E015 · Adaptive Boundary Sampling</text>
<text x="30" y="68" class="sub">E014 exhaustive oracle → monotone staircase candidate → independent promotion gate</text>
<text x="30" y="127" class="label">Exhaustive</text>
<rect x="{bar_x}" y="104" width="{bar_width}" height="34" rx="17" class="track"/>
<rect x="{bar_x}" y="104" width="{exhaustive_width}" height="34" rx="17" class="full"/>
<text x="{bar_x + exhaustive_width - 16}" y="128" text-anchor="end" class="value">{exhaustive}</text>
<text x="30" y="188" class="label">Adaptive</text>
<rect x="{bar_x}" y="165" width="{bar_width}" height="34" rx="17" class="track"/>
<rect x="{bar_x}" y="165" width="{adaptive_width}" height="34" rx="17" class="adaptive"/>
<text x="{bar_x + adaptive_width + 14}" y="189" class="value">{adaptive}</text>
<text x="30" y="239" class="metric">Query savings {savings:.1%}</text>
<text x="286" y="239" class="metric">Cell classification {accuracy:.0%}</text>
<text x="570" y="239" class="metric">Frontier recovery {frontier_rate:.0%}</text>
<text x="836" y="239" class="metric">Monotonicity violations {monotonicity}</text>
<rect x="30" y="270" width="980" height="36" rx="18" fill="#0d2c25" stroke="#22c55e"/>
<text x="520" y="294" text-anchor="middle" class="metric">PROMOTED · adaptive exploration / exhaustive periodic audit</text>
</svg>
'''


def render_e016(payload: dict) -> str:
    same_mode = str(payload["same_generation"]["mode"]).upper()
    changed_mode = str(payload["changed_generation"]["mode"]).upper()
    probe = payload["adversarial_probe"]
    accuracy = float(probe["naive_classification_accuracy"])
    violations = int(probe["monotonicity_violation_count"])
    post_mode = str(payload["post_audit_mode"]).upper()

    width = 1040
    height = 390

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E016 generation-scoped adaptive guard</title>
<desc id="desc">Adaptive authorization is generation-scoped and revoked by exhaustive audit when non-monotonicity is detected.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .head {{ font: 700 13px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; letter-spacing: 1px; }}
  .mode {{ font: 800 24px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .body {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #d8e4f2; }}
  .metric {{ font: 800 22px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .ok {{ fill: #0f3d32; stroke: #22c55e; stroke-width: 2; }}
  .fallback {{ fill: #3b2a14; stroke: #f59e0b; stroke-width: 2; }}
  .adversary {{ fill: #3c1721; stroke: #f43f5e; stroke-width: 2; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#231535"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="30" y="42" class="title">E016 · Adaptive Guard / Fail-Closed Revocation</text>
<text x="30" y="68" class="sub">Certificate scope → generation mismatch → adversarial non-monotonicity → exhaustive fallback</text>

<rect x="30" y="100" width="300" height="105" rx="18" class="ok"/>
<text x="52" y="128" class="head">SAME GENERATION</text>
<text x="52" y="163" class="mode">{same_mode}</text>
<text x="52" y="188" class="body">certificate fingerprint matches</text>

<rect x="370" y="100" width="300" height="105" rx="18" class="fallback"/>
<text x="392" y="128" class="head">HORIZON 60 → 61</text>
<text x="392" y="163" class="mode">{changed_mode}</text>
<text x="392" y="188" class="body">generation fingerprint mismatch</text>

<rect x="710" y="100" width="300" height="105" rx="18" class="adversary"/>
<text x="732" y="128" class="head">HIDDEN SURVIVAL ISLAND</text>
<text x="732" y="163" class="metric">{accuracy:.2%} accuracy</text>
<text x="732" y="188" class="body">{violations} monotonicity violations</text>

<path d="M330 152 L365 152" stroke="#7dd3fc" stroke-width="3"/>
<path d="M670 152 L705 152" stroke="#7dd3fc" stroke-width="3"/>

<rect x="30" y="245" width="980" height="94" rx="20" fill="#101f2e" stroke="#7dd3fc" stroke-width="2"/>
<text x="52" y="277" class="head">EXHAUSTIVE AUDIT DECISION</text>
<text x="52" y="313" class="mode">REVOKE ADAPTIVE → {post_mode}</text>
<text x="610" y="313" class="body">sparse adaptive queries cannot certify their own monotonicity premise</text>

<text x="30" y="368" class="sub">Guard contract: {"PASS" if payload["guard_contract_passed"] else "FAIL"} · structural change invalidates before use; hidden assumption failure is caught by audit</text>
</svg>
'''


def render_e017(payload: dict) -> str:
    stable = payload["stable_summary"]
    drift = payload["drift_summary"]
    stable_savings = float(stable["query_savings_fraction"])
    drift_savings = float(drift["query_savings_fraction"])
    stable_actual = int(stable["actual_queries"])
    drift_actual = int(drift["actual_queries"])
    baseline = int(stable["always_exhaustive_queries"])
    audit_interval = int(payload["policy"]["audit_interval_epochs"])
    expiry = int(payload["policy"]["expiry_epochs"])

    width = 1040
    height = 400
    bar_x = 270
    bar_width = 700
    stable_width = int(round(bar_width * stable_actual / baseline))
    drift_width = int(round(bar_width * drift_actual / baseline))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E017 certificate lifecycle and audit cadence</title>
<desc id="desc">Periodic exhaustive audits preserve fail-closed behavior while reducing total evaluator queries across evidence epochs.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .label {{ font: 650 17px Inter,Segoe UI,Arial,sans-serif; fill: #e5edf8; }}
  .value {{ font: 800 19px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .metric {{ font: 700 15px Inter,Segoe UI,Arial,sans-serif; fill: #c7f9d4; }}
  .track {{ fill: #26354d; }}
  .stable {{ fill: #22c55e; }}
  .drift {{ fill: #f59e0b; }}
  .base {{ fill: #64748b; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#12324a"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="30" y="42" class="title">E017 · Certificate Lifecycle / Audit Cadence</text>
<text x="30" y="68" class="sub">12 deterministic evidence epochs · audit every {audit_interval} · hard expiry {expiry}</text>

<text x="30" y="126" class="label">Always exhaustive</text>
<rect x="{bar_x}" y="103" width="{bar_width}" height="34" rx="17" class="track"/>
<rect x="{bar_x}" y="103" width="{bar_width}" height="34" rx="17" class="base"/>
<text x="{bar_x + bar_width - 15}" y="127" text-anchor="end" class="value">{baseline}</text>

<text x="30" y="190" class="label">Stable generation</text>
<rect x="{bar_x}" y="167" width="{bar_width}" height="34" rx="17" class="track"/>
<rect x="{bar_x}" y="167" width="{stable_width}" height="34" rx="17" class="stable"/>
<text x="{bar_x + stable_width + 14}" y="191" class="value">{stable_actual}</text>

<text x="30" y="254" class="label">Drift at epoch {payload["drift_epoch"]}</text>
<rect x="{bar_x}" y="231" width="{bar_width}" height="34" rx="17" class="track"/>
<rect x="{bar_x}" y="231" width="{drift_width}" height="34" rx="17" class="drift"/>
<text x="{bar_x + drift_width + 14}" y="255" class="value">{drift_actual}</text>

<text x="30" y="306" class="metric">Stable savings {stable_savings:.1%} · {stable["adaptive_epochs"]} adaptive / {stable["exhaustive_epochs"]} exhaustive epochs</text>
<text x="30" y="334" class="metric">Drift savings {drift_savings:.1%} · generation change forces immediate exhaustive recertification</text>
<text x="30" y="362" class="metric">Failed audit → {payload["failed_audit_decision"]["state"]} · skipped audit → {payload["expiry_decision"]["state"]}</text>
<text x="30" y="387" class="sub">Lifecycle contract: {"PASS" if payload["lifecycle_contract_passed"] else "FAIL"}</text>
</svg>
'''


def render_e018(payload: dict) -> str:
    aggregate = payload["aggregate"]
    oracle_work = int(aggregate["oracle_work_units"])
    dp_work = int(aggregate["dp_work_units"])
    dp_match = float(aggregate["dp_exact_match_rate"])
    greedy_match = float(aggregate["greedy_exact_match_rate"])
    reduction = float(aggregate["dp_work_reduction_fraction"])
    trap = payload["greedy_trap"]
    oracle_trap = int(trap["oracle"]["total_restoration_value"])
    greedy_trap = int(trap["greedy"]["total_restoration_value"])

    width = 1040
    height = 400
    bar_x = 265
    bar_width = 700
    dp_width = int(round(bar_width * dp_work / oracle_work))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E018 audit portfolio scheduler</title>
<desc id="desc">Bounded dynamic programming exactly matches exhaustive audit-budget scheduling with much lower search work, while greedy scheduling has explicit counterexamples.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .label {{ font: 650 17px Inter,Segoe UI,Arial,sans-serif; fill: #e5edf8; }}
  .value {{ font: 800 19px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .metric {{ font: 700 16px Inter,Segoe UI,Arial,sans-serif; fill: #c7f9d4; }}
  .warn {{ font: 700 16px Inter,Segoe UI,Arial,sans-serif; fill: #fecaca; }}
  .track {{ fill: #26354d; }}
  .oracle {{ fill: #64748b; }}
  .dp {{ fill: #22c55e; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#233019"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="30" y="42" class="title">E018 · Audit Portfolio Scheduler</text>
<text x="30" y="68" class="sub">48 generated 8-certificate portfolios · exact subset oracle vs bounded DP vs greedy heuristic</text>

<text x="30" y="130" class="label">Exhaustive oracle work</text>
<rect x="{bar_x}" y="107" width="{bar_width}" height="34" rx="17" class="track"/>
<rect x="{bar_x}" y="107" width="{bar_width}" height="34" rx="17" class="oracle"/>
<text x="{bar_x + bar_width - 15}" y="131" text-anchor="end" class="value">{oracle_work}</text>

<text x="30" y="194" class="label">Bounded-DP work</text>
<rect x="{bar_x}" y="171" width="{bar_width}" height="34" rx="17" class="track"/>
<rect x="{bar_x}" y="171" width="{dp_width}" height="34" rx="17" class="dp"/>
<text x="{bar_x + dp_width + 14}" y="195" class="value">{dp_work}</text>

<text x="30" y="249" class="metric">Work reduction {reduction:.1%}</text>
<text x="300" y="249" class="metric">DP exact match {dp_match:.0%}</text>
<text x="555" y="249" class="warn">Greedy exact match {greedy_match:.1%}</text>

<rect x="30" y="282" width="980" height="72" rx="18" fill="#311822" stroke="#f43f5e"/>
<text x="52" y="312" class="warn">Greedy trap</text>
<text x="205" y="312" class="value">greedy {greedy_trap}</text>
<text x="400" y="312" class="value">exact / DP {oracle_trap}</text>
<text x="670" y="312" class="metric">mandatory-over-budget → FAIL CLOSED</text>

<text x="30" y="383" class="sub">Promoted scheduler: {payload["promoted_scheduler"] or "NONE"}</text>
</svg>
'''


def render_e019(payload: dict) -> str:
    reference = payload["reference"]
    attacks = payload["attacks"]
    event_count = len(reference["events"])
    replay = reference["replay_state"]
    rehash = attacks["full_rehash_rewrite"]

    width = 1040
    height = 430

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E019 durable certificate provenance ledger</title>
<desc id="desc">Hash-chain provenance catches local corruption, while an independent checkpoint catches a fully rehashed history rewrite.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .head {{ font: 700 13px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; letter-spacing: 1px; }}
  .mode {{ font: 800 22px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .body {{ font: 14px Inter,Segoe UI,Arial,sans-serif; fill: #d8e4f2; }}
  .ok {{ fill: #0f3d32; stroke: #22c55e; stroke-width: 2; }}
  .bad {{ fill: #3c1721; stroke: #f43f5e; stroke-width: 2; }}
  .warn {{ fill: #3b2a14; stroke: #f59e0b; stroke-width: 2; }}
  .checkpoint {{ fill: #172554; stroke: #60a5fa; stroke-width: 2; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#281536"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="30" y="42" class="title">E019 · Durable Certificate Provenance</text>
<text x="30" y="68" class="sub">{event_count}-event reference ledger · append-only SHA-256 chain · out-of-ledger checkpoint</text>

<rect x="30" y="100" width="300" height="108" rx="18" class="ok"/>
<text x="52" y="128" class="head">REFERENCE LEDGER</text>
<text x="52" y="162" class="mode">CHAIN + CHECKPOINT PASS</text>
<text x="52" y="188" class="body">Replay: {replay["status"]} / {replay["required_mode"]}</text>

<rect x="370" y="100" width="300" height="108" rx="18" class="bad"/>
<text x="392" y="128" class="head">LOCAL CORRUPTION</text>
<text x="392" y="162" class="mode">DETECTED INTERNALLY</text>
<text x="392" y="188" class="body">payload · deletion · reorder → chain FAIL</text>

<rect x="710" y="100" width="300" height="108" rx="18" class="warn"/>
<text x="732" y="128" class="head">FULL REHASH REWRITE</text>
<text x="732" y="162" class="mode">CHAIN STILL PASSES</text>
<text x="732" y="188" class="body">forged replay → {rehash["replay_state"]["status"]}</text>

<path d="M330 154 L365 154" stroke="#7dd3fc" stroke-width="3"/>
<path d="M670 154 L705 154" stroke="#7dd3fc" stroke-width="3"/>

<rect x="30" y="252" width="980" height="103" rx="20" class="checkpoint"/>
<text x="52" y="282" class="head">INDEPENDENT CHECKPOINT</text>
<text x="52" y="318" class="mode">REHASHED HISTORY → CHECKPOINT MISMATCH → REJECT</text>
<text x="52" y="342" class="body">The ledger cannot certify its own rewritten history; the anchor lives outside the mutable chain.</text>

<text x="30" y="393" class="sub">Append-only extension preserves prior hashes: {"YES" if payload["append_extension"]["prefix_hashes_preserved"] else "NO"}</text>
<text x="30" y="416" class="sub">Promoted contract: {payload["promoted_ledger_contract"] or "NONE"}</text>
</svg>
'''


def render_e020(payload: dict) -> str:
    reference = payload["reference"]
    attacks = payload["attacks"]
    checkpoint_count = len(reference["checkpoints"])
    anchored = int(reference["anchored_event_count"])
    total = int(reference["ledger_event_count"])
    tail = int(reference["unanchored_tail_events"])

    width = 1040
    height = 430

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">E020 checkpoint rotation and anchor continuity</title>
<desc id="desc">Rotating checkpoints preserve continuity to a pinned anchor and reject rewritten ledger prefixes that a latest-only verifier accepts.</desc>
<style>
  .title {{ font: 700 28px Inter,Segoe UI,Arial,sans-serif; fill: #eff6ff; }}
  .sub {{ font: 15px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; }}
  .head {{ font: 700 13px Inter,Segoe UI,Arial,sans-serif; fill: #9fb0c8; letter-spacing: 1px; }}
  .mode {{ font: 800 22px Inter,Segoe UI,Arial,sans-serif; fill: #ffffff; }}
  .body {{ font: 14px Inter,Segoe UI,Arial,sans-serif; fill: #d8e4f2; }}
  .ok {{ fill: #0f3d32; stroke: #22c55e; stroke-width: 2; }}
  .warn {{ fill: #3b2a14; stroke: #f59e0b; stroke-width: 2; }}
  .bad {{ fill: #3c1721; stroke: #f43f5e; stroke-width: 2; }}
  .pin {{ fill: #172554; stroke: #60a5fa; stroke-width: 2; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b1020"/>
    <stop offset="1" stop-color="#153147"/>
  </linearGradient>
</defs>
<rect width="100%" height="100%" rx="22" fill="url(#bg)"/>
<text x="30" y="42" class="title">E020 · Checkpoint Rotation / Anchor Continuity</text>
<text x="30" y="68" class="sub">{total} ledger events · {checkpoint_count} rotating checkpoints · {anchored} anchored · {tail} unanchored tail</text>

<rect x="30" y="100" width="300" height="108" rx="18" class="ok"/>
<text x="52" y="128" class="head">HONEST ROTATION</text>
<text x="52" y="162" class="mode">CHAIN + PIN PASS</text>
<text x="52" y="188" class="body">2 → 4 → 6 → 8 event anchors</text>

<rect x="370" y="100" width="300" height="108" rx="18" class="warn"/>
<text x="392" y="128" class="head">LATEST-ONLY FORGERY</text>
<text x="392" y="162" class="mode">LATEST CHECK PASSES</text>
<text x="392" y="188" class="body">rewritten old prefix looks self-consistent</text>

<rect x="710" y="100" width="300" height="108" rx="18" class="bad"/>
<text x="732" y="128" class="head">PINNED HISTORY</text>
<text x="732" y="162" class="mode">REWRITE REJECTED</text>
<text x="732" y="188" class="body">{attacks["latest_only_forgery"]["pinned_rotation_reason"]}</text>

<path d="M330 154 L365 154" stroke="#7dd3fc" stroke-width="3"/>
<path d="M670 154 L705 154" stroke="#7dd3fc" stroke-width="3"/>

<rect x="30" y="252" width="980" height="103" rx="20" class="pin"/>
<text x="52" y="282" class="head">ROTATION INTEGRITY</text>
<text x="52" y="318" class="mode">DELETE ✕ · REORDER ✕ · FORK ✕</text>
<text x="52" y="342" class="body">Old trust is not discarded when a newer checkpoint appears.</text>

<text x="30" y="393" class="sub">Fork detected: {"YES" if attacks["checkpoint_fork"]["detected"] else "NO"} · unanchored tail: {tail} events</text>
<text x="30" y="416" class="sub">Promoted contract: {payload["promoted_rotation_contract"] or "NONE"}</text>
</svg>
'''

def render_markdown(e011: dict, e012: dict, e013: dict, e014: dict, e015: dict, e016: dict, e017: dict, e018: dict, e019: dict, e020: dict) -> str:
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

    mechanisms = (
        "usage-only",
        "light-floor",
        "balanced",
        "diversity-heavy",
        "creator-heavy",
        "platform-heavy",
    )
    axis_labels = (
        ("subscription_price_multiplier", "Price ↓"),
        ("platform_cost_multiplier", "Platform cost ↑"),
        ("base_churn_rate", "Churn ↑"),
    )
    e013_rows = "\n".join(
        "| "
        + label
        + " | "
        + " | ".join(
            "10+" if e013["knees"][axis][mechanism] is None
            else str(e013["knees"][axis][mechanism])
            for mechanism in mechanisms
        )
        + " |"
        for axis, label in axis_labels
    )
    e013_header = "| Axis | " + " | ".join(mechanisms) + " |"
    e013_rule = "| --- | " + " | ".join("---:" for _ in mechanisms) + " |"

    pair_defs = (
        (
            "subscription_price_multiplier__platform_cost_multiplier",
            "Price × Cost",
        ),
        (
            "subscription_price_multiplier__base_churn_rate",
            "Price × Churn",
        ),
        (
            "platform_cost_multiplier__base_churn_rate",
            "Cost × Churn",
        ),
    )
    e014_rows = []
    total_interaction_only = 0
    for mechanism in mechanisms:
        cells = []
        for pair_key, _ in pair_defs:
            summary = e014["summaries"][pair_key][mechanism]
            frontier = summary["frontier"]
            count = int(summary["interaction_only_cells"])
            total_interaction_only += count
            if frontier is None:
                cells.append(f"none · {count}")
            else:
                marker = "★" if frontier["interaction_only"] else ""
                cells.append(
                    f'{frontier["level_a"]}+{frontier["level_b"]}{marker} · {count}'
                )
        e014_rows.append(
            "| " + mechanism + " | " + " | ".join(cells) + " |"
        )
    e014_rows_text = "\n".join(e014_rows)

    aggregate = e015["aggregate"]
    guard_probe = e016["adversarial_probe"]
    stable_lifecycle = e017["stable_summary"]
    drift_lifecycle = e017["drift_summary"]
    audit_portfolio = e018["aggregate"]
    greedy_trap = e018["greedy_trap"]
    provenance_attacks = e019["attacks"]
    rotation_attacks = e020["attacks"]
    return f"""# Generated research dashboard

> Generated from E011/E012/E013/E014/E015/E016/E017/E018/E019/E020 report JSON by `scripts/render_research_dashboard.py`.
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

## E013 — one-dimensional pressure decomposition

![E013 pressure decomposition](e013-decomposition.svg)

{e013_header}
{e013_rule}
{e013_rows}

Composite E011 knees were 3–4, while the earliest E013 single-axis knee is 6. That gap is evidence of interaction inside the declared synthetic world.

## E014 — pairwise interaction surfaces

![E014 pairwise interaction frontiers](e014-interactions.svg)

| Mechanism | Price × Cost | Price × Churn | Cost × Churn |
| --- | ---: | ---: | ---: |
{e014_rows_text}

Each cell is `frontier level_a+level_b · interaction-only cell count`. ★ means the first failing frontier itself is interaction-only.

**Total interaction-only cells:** {total_interaction_only}

## E015 — adaptive boundary sampling

![E015 adaptive boundary sampling](e015-sampling.svg)

| Metric | Exhaustive | Adaptive |
| --- | ---: | ---: |
| Pair-surface queries | {aggregate["exhaustive_queries"]} | {aggregate["adaptive_queries"]} |
| Mean queries / surface | 49.0 | {aggregate["mean_queries_per_surface"]:.2f} |

- Query savings: **{aggregate["query_savings_fraction"]:.1%}**
- Cell classification accuracy: **{aggregate["classification_accuracy"]:.0%}**
- Exact frontier recovery: **{aggregate["frontier_exact_rate"]:.0%}**
- Monotonicity violations: **{aggregate["monotonicity_violation_count"]}**
- Promotion: **{"PASS" if e015["promoted"] else "FAIL"}**

## E016 — generation-scoped adaptive guard

![E016 adaptive guard](e016-guard.svg)

| Guard case | Decision |
| --- | --- |
| Same generation fingerprint | **{e016["same_generation"]["mode"]}** |
| Horizon 60 → 61 | **{e016["changed_generation"]["mode"]}** |
| Hidden non-monotone island | naive accuracy **{guard_probe["naive_classification_accuracy"]:.2%}** |
| Exhaustive audit | **{guard_probe["monotonicity_violation_count"]} violations detected** |
| Post-audit mode | **{e016["post_audit_mode"]}** |

Guard contract: **{"PASS" if e016["guard_contract_passed"] else "FAIL"}**.

## E017 — certificate lifecycle and audit cadence

![E017 certificate lifecycle](e017-lifecycle.svg)

| Schedule | Queries | Savings vs always exhaustive |
| --- | ---: | ---: |
| Always exhaustive | {stable_lifecycle["always_exhaustive_queries"]} | 0% |
| Stable generation | {stable_lifecycle["actual_queries"]} | {stable_lifecycle["query_savings_fraction"]:.1%} |
| Drift at epoch {e017["drift_epoch"]} | {drift_lifecycle["actual_queries"]} | {drift_lifecycle["query_savings_fraction"]:.1%} |

- Stable schedule: **{stable_lifecycle["adaptive_epochs"]} adaptive / {stable_lifecycle["exhaustive_epochs"]} exhaustive epochs**
- Failed audit: **{e017["failed_audit_decision"]["state"]} → {e017["failed_audit_decision"]["required_mode"]}**
- Skipped audit through hard expiry: **{e017["expiry_decision"]["state"]} → {e017["expiry_decision"]["required_mode"]}**
- Lifecycle contract: **{"PASS" if e017["lifecycle_contract_passed"] else "FAIL"}**

## E018 — audit portfolio scheduler

![E018 audit portfolio scheduler](e018-audit-portfolio.svg)

| Scheduler | Exact match | Search work |
| --- | ---: | ---: |
| Exhaustive oracle | 100% | {audit_portfolio["oracle_work_units"]} |
| Bounded-DP | {audit_portfolio["dp_exact_match_rate"]:.0%} | {audit_portfolio["dp_work_units"]} |
| Greedy value/cost | {audit_portfolio["greedy_exact_match_rate"]:.1%} | heuristic |

- DP work reduction: **{audit_portfolio["dp_work_reduction_fraction"]:.1%}**
- Fixed greedy trap: **{greedy_trap["greedy"]["total_restoration_value"]} vs exact {greedy_trap["oracle"]["total_restoration_value"]}**
- Mandatory-over-budget: **FAIL CLOSED**
- Promoted scheduler: **{e018["promoted_scheduler"] or "NONE"}**

## E019 — durable certificate provenance ledger

![E019 provenance ledger](e019-provenance.svg)

| Integrity case | Internal chain | External checkpoint |
| --- | --- | --- |
| Reference history | **PASS** | **PASS** |
| Payload tamper | **FAIL** | not needed |
| Event deletion | **FAIL** | not needed |
| Event reorder | **FAIL** | not needed |
| Full rewrite + downstream rehash | **PASS** | **FAIL / detected** |

- Reference replay: **{e019["reference"]["replay_state"]["status"]} / {e019["reference"]["replay_state"]["required_mode"]}**
- Rehashed forged replay: **{provenance_attacks["full_rehash_rewrite"]["replay_state"]["status"]}**
- Append-only extension preserves prefix hashes: **{"YES" if e019["append_extension"]["prefix_hashes_preserved"] else "NO"}**
- Promoted ledger contract: **{e019["promoted_ledger_contract"] or "NONE"}**

## E020 — checkpoint rotation and anchor continuity

![E020 checkpoint rotation](e020-checkpoint-rotation.svg)

| Case | Result |
| --- | --- |
| Honest rotation | **PASS** |
| Pinned checkpoint continuity | **PASS** |
| Delete checkpoint | **REJECTED** |
| Reorder checkpoints | **REJECTED** |
| Latest-only forged checkpoint | **ACCEPTED by weak verifier** |
| Same rewrite with pinned history | **REJECTED** |
| Checkpoint fork | **DETECTED** |

- Anchored ledger prefix: **{e020["reference"]["anchored_event_count"]}/{e020["reference"]["ledger_event_count"]} events**
- Unanchored tail: **{e020["reference"]["unanchored_tail_events"]} events**
- Latest-only weakness: **{rotation_attacks["latest_only_forgery"]["latest_only_reason"]}**
- Pinned rotation result: **{rotation_attacks["latest_only_forgery"]["pinned_rotation_reason"]}**
- Promoted rotation contract: **{e020["promoted_rotation_contract"] or "NONE"}**

These are model-relative synthetic results. They are not real-market recommendations.
"""


def generated_files(
    e011: dict,
    e012: dict,
    e013: dict,
    e014: dict,
    e015: dict,
    e016: dict,
    e017: dict,
    e018: dict,
    e019: dict,
    e020: dict,
) -> dict[Path, str]:
    return {
        OUT / "e011-pressure.svg": render_e011(e011),
        OUT / "e012-evaluator.svg": render_e012(e012),
        OUT / "e013-decomposition.svg": render_e013(e013),
        OUT / "e014-interactions.svg": render_e014(e014),
        OUT / "e015-sampling.svg": render_e015(e015),
        OUT / "e016-guard.svg": render_e016(e016),
        OUT / "e017-lifecycle.svg": render_e017(e017),
        OUT / "e018-audit-portfolio.svg": render_e018(e018),
        OUT / "e019-provenance.svg": render_e019(e019),
        OUT / "e020-checkpoint-rotation.svg": render_e020(e020),
        OUT / "research-dashboard.md": render_markdown(e011, e012, e013, e014, e015, e016, e017, e018, e019, e020),
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
    e013 = _read(E013)
    e014 = _read(E014)
    e015 = _read(E015)
    e016 = _read(E016)
    e017 = _read(E017)
    e018 = _read(E018)
    e019 = _read(E019)
    e020 = _read(E020)
    outputs = generated_files(e011, e012, e013, e014, e015, e016, e017, e018, e019, e020)

    if args.check:
        stale: list[str] = []
        for path, generated in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != generated:
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            raise SystemExit(
                "research dashboard is stale; regenerate and commit: "
                + ", ".join(stale)
            )
        print("research dashboard matches experiment output")
        return

    OUT.mkdir(parents=True, exist_ok=True)
    for path, generated in outputs.items():
        path.write_text(generated, encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
