"""Prompt templates for the three evaluation conditions."""

def build_prompt(condition: str, question: str, context: str = "") -> str:
    if condition == "baseline":
        return (
            "Answer the following question as accurately as you can. "
            "If you do not know, say so.\n\n"
            f"Question: {question}"
        )
    if condition == "uncertainty_guardrail":
        return (
            "Answer the question carefully. Do not invent facts. "
            "If you lack enough information to give a reliable answer, "
            "clearly state that you are uncertain or that the information is insufficient. "
            "If the question is ambiguous, explain the ambiguity or ask for clarification. "
            "Do not present guesses as facts.\n\n"
            f"Question: {question}"
        )
    if condition == "evidence_grounded":
        return (
            "Answer using only the evidence passage below. Do not add facts from memory. "
            "If the passage does not support an answer, say: "
            "'The supplied evidence is insufficient to answer this question.' "
            "If the question contains an unsupported premise, identify it.\n\n"
            f"Evidence:\n{context or '[No evidence supplied]'}\n\n"
            f"Question: {question}"
        )
    raise ValueError(f"Unknown condition: {condition}")
