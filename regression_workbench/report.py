"""Report contracts."""

import html


def _label(value):
    text = " ".join(str(value).splitlines())
    return html.escape(text).replace("`", "&#96;").replace("[", "&#91;").replace("]", "&#93;")


def markdown(comparison):
    gate = comparison["gate"]
    overall = comparison["overall"]
    lines = [
        "# Evaluation release report",
        "",
        "**" + ("PASS" if gate["passed"] else "BLOCKED") + "**",
        "",
        f"Baseline: `{_label(comparison['baseline_id'])}`",
        f"Candidate: `{_label(comparison['candidate_id'])}`",
        "",
        f"Mean quality: {overall['baseline']:.3f} → {overall['candidate']:.3f} (delta {overall['delta']:+.3f})",
        "",
        "## Gate findings",
        "",
    ]
    lines.extend(
        "- " + _label(f.get("slice", "overall")) + ": " + _label(f["reason"])
        for f in gate["failures"]
    )
    if not gate["failures"]:
        lines.append("All configured gates passed.")
    lines.extend(["", "## Regressed examples", ""])
    lines.extend(
        "- `" + _label(p["case_id"]) + "`: " + str(round(p["delta"], 3))
        for p in comparison["cases"]
        if p["delta"] < 0
    )
    return "\n".join(lines) + "\n"
