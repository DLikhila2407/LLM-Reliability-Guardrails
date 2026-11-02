# Evaluating LLM Reliability and Uncertainty-Aware Guardrails

**Research project starter kit**  
Research focus: hallucination, abstention, evidence grounding, and uncertainty-aware response behaviour.

## Research question

Can uncertainty-aware response instructions and evidence-grounded guardrails reduce unsupported claims in LLM answers while preserving the ability to answer when adequate evidence is available?

This repository is an experimental scaffold, not a completed study. It contains no claimed findings. Run the experiments, inspect outputs, annotate responses, and report only observed results.

## Experimental conditions

1. `baseline`: ordinary question answering, with no special uncertainty instruction.
2. `uncertainty_guardrail`: asks the model to express uncertainty and abstain when it lacks sufficient knowledge.
3. `evidence_grounded`: supplies a context passage and instructs the model to answer only from that passage, or abstain if the passage does not support an answer.

For a fair comparison, use the same model version, question set, and generation settings across conditions wherever possible. Note that the evidence-grounded condition includes supplied context, so it tests a different information setting; explain this limitation in your report.

## Quick start

### 1. Environment

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your Gemini API key to `.env` if using live model calls. Keep `.env` private and never commit credentials.

### 2. Prepare the dataset

Edit `data/questions_template.csv`. Use one row per question:

- `id`: unique identifier
- `category`: `answerable`, `unanswerable`, `ambiguous`, or `misleading_premise`
- `question`: question sent to the model
- `context`: evidence passage supplied to the evidence-grounded condition; leave empty if none
- `reference_answer`: concise answer key for human evaluation
- `answerability`: `answerable`, `unanswerable`, or `needs_clarification`
- `notes`: source or annotation rationale

Use reliable sources to create the reference answers. Record source URLs in `notes` or maintain a separate source log. Do not use private or sensitive data.

### 3. Run model responses

```bash
python -m src.run_experiments --input data/questions_template.csv --output results/responses.jsonl
```

The script calls Gemini when `GEMINI_API_KEY` is set. Without a key, it runs in `--dry-run` mode only if explicitly requested:

```bash
python -m src.run_experiments --input data/questions_template.csv --output results/demo_responses.jsonl --dry-run
```

Dry-run responses are placeholders for checking the pipeline. They are not model results and must never be included in research findings.

### 4. Human annotation

Review `results/responses.jsonl` and create `results/annotations_template.csv` with one row per response. Annotate:

- `correct`: `1` if substantively correct, otherwise `0`
- `unsupported_claim`: `1` if the answer contains at least one material factual claim not supported by the permitted information, otherwise `0`
- `abstained`: `1` if the model declined to answer or explicitly said it could not determine the answer, otherwise `0`
- `confidence`: optional model-stated confidence from 0 to 1, only if the model explicitly provides it. Treat self-reported confidence as uncalibrated.
- `reviewer_notes`: brief reason for the labels

Prefer two independent reviewers for a subset of responses. Resolve disagreements using a written annotation guide. Do not treat an LLM judge as ground truth.

### 5. Calculate metrics

```bash
python -m src.analyze_results --annotations results/annotations.csv --output-dir results/analysis
```

The analysis script calculates accuracy, unsupported-claim rate, abstention rate, and false-abstention rate, and generates basic comparison plots. It does not automatically establish whether a claim is hallucinated; that requires careful annotation against the reference evidence.

## Metrics and definitions

- **Accuracy among all items:** correct responses / all evaluated responses. Abstentions count as not correct.
- **Unsupported-claim rate:** responses marked as containing a material unsupported claim / all evaluated responses.
- **Abstention rate:** abstentions / all evaluated responses.
- **False-abstention rate:** abstentions on items labelled `answerable` / all items labelled `answerable`.
- **Answer rate:** non-abstentions / all evaluated responses.

Report denominators and confidence intervals. Consider reporting metrics separately by question category. Avoid a single aggregate score that hides trade-offs.

## Research integrity and limitations

- Pre-register hypotheses and evaluation rules before inspecting comparative results.
- Keep model name, version, date, temperature, prompts, and API settings in the experiment log.
- Use identical question wording across conditions.
- Repeat runs if stochasticity is part of the research question; otherwise set a consistent low temperature where supported.
- The baseline and uncertainty-guardrail conditions may rely on model parametric knowledge, while the evidence-grounded condition receives external context. This is not a perfectly controlled comparison.
- A model's verbal confidence is not a calibrated probability. Proper calibration requires confidence estimates tied to correctness over a sufficiently large labelled sample.
- A small hand-built dataset supports a pilot study, not broad claims about all LLMs.
- Do not claim to solve AI alignment or guarantee safety.

## Repository map

```text
.
├── data/
│   └── questions_template.csv
├── notebooks/
├── research_paper/
│   ├── proposal.md
│   └── paper_template.md
├── results/
│   └── annotations_template.csv
├── src/
│   ├── prompts.py
│   ├── run_experiments.py
│   └── analyze_results.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## Suggested first milestone

Build and manually verify a pilot dataset of 30 questions (balanced across categories) before scaling to 200–300. Test the annotation guide on 10 responses, revise ambiguous definitions, then freeze the protocol before running the full evaluation.
