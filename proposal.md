# Research Proposal

## Title
**Evaluating LLM Reliability and Uncertainty-Aware Guardrails: A Comparative Study of Hallucination, Abstention, and Evidence Grounding**

## 1. Abstract
Large language models (LLMs) can produce fluent answers even when information is incomplete, ambiguous, or unavailable. This project proposes a controlled evaluation of three response conditions: a baseline model, an uncertainty-aware instruction condition, and an evidence-grounded guardrail condition. The study will measure answer accuracy, unsupported-claim rate, abstention behaviour, and the trade-off between avoiding unsupported answers and answering answerable questions. A curated dataset will include answerable, unanswerable, ambiguous, and misleading-premise questions. Model outputs will be evaluated against documented reference evidence using a transparent annotation protocol. The project is designed as a reproducible pilot study; conclusions will be limited to the tested model, prompts, dataset, and settings.

## 2. Motivation
Reliability is an important component of safe AI deployment. A system that answers confidently without adequate support can mislead users. Conversely, a system that refuses too often may be unhelpful. Evaluating both unsupported claims and unnecessary abstention makes it possible to study this trade-off rather than optimizing refusal behaviour alone.

## 3. Research questions
1. Does an uncertainty-aware instruction reduce unsupported claims compared with a baseline condition?
2. Does evidence grounding reduce unsupported claims when relevant context is provided?
3. What effect do these interventions have on accuracy and abstention?
4. How do results differ across answerable, unanswerable, ambiguous, and misleading-premise questions?
5. Do any observed gains come with an increase in false abstentions?

## 4. Hypotheses
- H1: The uncertainty-aware condition will have a lower unsupported-claim rate than baseline.
- H2: The evidence-grounded condition will have a lower unsupported-claim rate on questions whose answers are or are not contained in the supplied context.
- H3: Guardrails may increase abstention, including false abstention on answerable questions.
- H4: Performance will vary by question category.

These are hypotheses, not expected or established findings.

## 5. Experimental design
Use the same underlying model and question set across three conditions:

### A. Baseline
The model receives the question and answers normally.

### B. Uncertainty-aware guardrail
The model receives the question and instructions to state uncertainty clearly and abstain if it cannot provide a reliable answer.

### C. Evidence-grounded guardrail
The model receives a context passage and question. It must answer only if the passage supports the answer; otherwise it must state that the information is insufficient.

**Important design qualification:** Condition C receives additional evidence. Therefore, it is not a pure prompt-only comparison with A and B. The report must describe it as an evidence-assisted condition and avoid attributing all differences solely to guardrail wording.

## 6. Dataset
Target size: 200–300 items after a pilot.

Categories:
- Answerable: evidence supports a clear answer.
- Unanswerable: available information does not support an answer.
- Ambiguous: multiple interpretations are plausible or clarification is needed.
- Misleading premise: the question presupposes something not established by the evidence.

Each item should contain an ID, category, question, context, reference answer, answerability label, and source/annotation notes. Use public, reputable sources and retain source records. Avoid sensitive personal data and questions requiring current facts unless the source snapshot date is recorded.

## 7. Procedure
1. Draft a protocol and annotation guide before collecting results.
2. Build a 30-item pilot balanced across categories.
3. Check that questions and evidence are clear; revise the annotation guide.
4. Freeze the dataset and prompts.
5. Run each item under all three conditions using the same model version and documented settings.
6. Save raw outputs, timestamps, model identifier, and prompt condition.
7. Have human reviewers label correctness, unsupported claims, and abstention.
8. Double-annotate a subset and report agreement or disagreements.
9. Calculate metrics and category-wise results.
10. Conduct error analysis and document limitations.

## 8. Metrics
- Accuracy: correct responses divided by all evaluated responses; abstentions count as not correct.
- Unsupported-claim rate: responses with at least one material unsupported claim divided by all evaluated responses.
- Abstention rate: abstentions divided by all evaluated responses.
- False-abstention rate: abstentions on answerable items divided by all answerable items.
- Answer rate: non-abstentions divided by all evaluated responses.

If model-stated confidence is collected, report it descriptively only. Do not call it calibrated confidence unless calibration is evaluated using an appropriate method and sufficient labelled data.

## 9. Analysis plan
Report numerator, denominator, and rate for every metric. Provide category-wise breakdowns. Use paired comparisons because the same questions are evaluated under each condition. Consider paired bootstrap confidence intervals and an appropriate paired test for binary outcomes. State the test, assumptions, effect size, and uncertainty. Avoid overclaiming statistical significance from a small pilot.

## 10. Risks to validity and limitations
- The dataset may not represent real-world user queries.
- Human annotation involves judgment; clear rules and double annotation help but do not eliminate subjectivity.
- A single model and snapshot do not support generalization to all LLMs.
- Model updates or API changes may affect reproducibility.
- Evidence-grounded condition has extra context, confounding a direct prompt-only comparison.
- Self-reported confidence may not correspond to actual correctness.
- A 200–300 item dataset is a modest study and may have limited statistical power.

## 11. Expected contribution
The project will produce a documented dataset, reproducible evaluation pipeline, transparent annotation guide, comparative analysis, and an honest account of the reliability–helpfulness trade-off for the tested setup. No outcome is assumed in advance.
