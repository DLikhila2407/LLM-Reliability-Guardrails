"""Calculate descriptive metrics from human annotations and create plots."""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

REQUIRED = {"id", "condition", "category", "answerability",
            "correct", "unsupported_claim", "abstained"}

def safe_rate(numerator, denominator):
    return numerator / denominator if denominator else float("nan")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.annotations)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise SystemExit(f"Missing annotation columns: {sorted(missing)}")

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for condition, group in df.groupby("condition"):
        answerable = group[group["answerability"] == "answerable"]
        rows.append({
            "condition": condition,
            "n": len(group),
            "accuracy": safe_rate(group["correct"].sum(), len(group)),
            "unsupported_claim_rate": safe_rate(group["unsupported_claim"].sum(), len(group)),
            "abstention_rate": safe_rate(group["abstained"].sum(), len(group)),
            "false_abstention_rate": safe_rate(answerable["abstained"].sum(), len(answerable)),
            "answer_rate": safe_rate((1 - group["abstained"]).sum(), len(group)),
        })

    summary = pd.DataFrame(rows)
    summary.to_csv(outdir / "summary_metrics.csv", index=False)
    print(summary.to_string(index=False))

    for metric in ["accuracy", "unsupported_claim_rate", "abstention_rate",
                   "false_abstention_rate", "answer_rate"]:
        ax = summary.plot(x="condition", y=metric, kind="bar", legend=False)
        ax.set_ylabel(metric.replace("_", " ").title())
        ax.set_xlabel("Experimental condition")
        ax.set_ylim(0, 1)
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(outdir / f"{metric}.png", dpi=160)
        plt.close()

    if "reviewer_id" in df.columns:
        print("Reviewer IDs found. Consider reporting inter-annotator agreement separately.")
    print(f"Saved analysis to {outdir}")

if __name__ == "__main__":
    main()
