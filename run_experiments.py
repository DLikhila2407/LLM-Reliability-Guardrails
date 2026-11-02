"""Run the three prompt conditions using the Gemini API or a clearly labelled dry run."""
import argparse
import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from src.prompts import build_prompt

CONDITIONS = ["baseline", "uncertainty_guardrail", "evidence_grounded"]

def call_gemini(prompt: str, model_name: str) -> str:
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Install requirements.txt to use the Gemini API.") from exc
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text or ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not args.dry_run and not api_key:
        raise SystemExit("GEMINI_API_KEY not found. Add it to .env or use --dry-run.")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(args.input, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    required = {"id", "category", "question", "context", "reference_answer", "answerability"}
    if not rows or not required.issubset(rows[0].keys()):
        raise SystemExit(f"Input CSV must contain columns: {sorted(required)}")

    with output.open("w", encoding="utf-8") as out:
        for row in rows:
            for condition in CONDITIONS:
                prompt = build_prompt(condition, row["question"], row.get("context", ""))
                if args.dry_run:
                    answer = "[DRY RUN ONLY: no model was called]"
                else:
                    answer = call_gemini(prompt, model_name)
                    time.sleep(float(os.getenv("REQUEST_DELAY_SECONDS", "1")))
                record = {
                    "id": row["id"],
                    "category": row["category"],
                    "answerability": row["answerability"],
                    "condition": condition,
                    "question": row["question"],
                    "context": row.get("context", ""),
                    "reference_answer": row.get("reference_answer", ""),
                    "response": answer,
                    "model": "DRY_RUN" if args.dry_run else model_name,
                    "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "is_dry_run": args.dry_run,
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
                print(f"Completed {row['id']} / {condition}")

if __name__ == "__main__":
    main()
