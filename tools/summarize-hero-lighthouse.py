"""Summarize the PR preview Lighthouse A/B runs without claiming causal certainty."""
import json
from pathlib import Path
from statistics import median
root=Path("hero-review-output/lighthouse")
summary={}
for variant in ("live","preview"):
    runs=[]
    for trial in (1,2):
        f=root/f"{variant}-{trial}.json"
        report=json.loads(f.read_text())
        audits=report["audits"]
        runs.append({
            "performance":round(report["categories"]["performance"]["score"]*100),
            "accessibility":round(report["categories"]["accessibility"]["score"]*100),
            "seo":round(report["categories"]["seo"]["score"]*100),
            "tbtMs":round(audits["total-blocking-time"]["numericValue"]),
            "lcpMs":round(audits["largest-contentful-paint"]["numericValue"]),
            "cls":round(audits["cumulative-layout-shift"]["numericValue"],4)
        })
    summary[variant]={"runs":runs,"medianTbtMs":median(x["tbtMs"] for x in runs),"medianLcpMs":median(x["lcpMs"] for x in runs),"medianPerformance":median(x["performance"] for x in runs)}
out={"results":summary,"caveat":"Only two lab runs each; production network versus localhost preview are not equivalent. Check full reports and screenshots. Do not infer field CWV or deploy based on scores alone."}
Path("hero-review-output/lighthouse-summary.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
