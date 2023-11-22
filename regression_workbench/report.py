"""Report contracts."""


def markdown(comparison):
    gate = comparison["gate"]
    overall = comparison["overall"]
    lines = [
        "# Evaluation release report",
        "",
        "**" + ("PASS" if gate["passed"] else "BLOCKED") + "**",
        "",
        f"Baseline: `{comparison['baseline_id']}`",
        f"Candidate: `{comparison['candidate_id']}`",
        "",
        f"Mean quality: {overall['baseline']:.3f} → {overall['candidate']:.3f} (delta {overall['delta']:+.3f})",
        "",
        "## Gate findings",
        "",
    ]
    lines.extend(
        "- " + str(f.get("slice", "overall")) + ": " + f["reason"]
        for f in gate["failures"]
    )
    if not gate["failures"]:
        lines.append("All configured gates passed.")
    lines.extend(["", "## Regressed examples", ""])
    lines.extend(
        "- `" + p["case_id"] + "`: " + str(round(p["delta"], 3))
        for p in comparison["cases"]
        if p["delta"] < 0
    )
    return "\n".join(lines) + "\n"
