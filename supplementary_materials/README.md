# Supplementary Materials

This directory contains supplementary materials for the paper. These files provide additional details that support the reported methodology and evaluation, but are not required for running the source code.

## Directory Structure

- `prompts/`
  - Prompt texts used in the constraint synthesis process.
  - These files document the main LLM-facing instructions used by the approach.

- `unit_inference_rules.pdf`
  - The unit-inference rules used by the unit validation mechanism.

- `human_evaluation_guidelines/`
  - Materials used for the RQ1 human evaluation of constraint quality.
  - This includes evaluator instructions, background materials, example constraints, and blank questionnaire forms.

## Human Evaluation Materials

The human-evaluation materials are organized under `human_evaluation_guidelines/`.

- `guide.md`: evaluator-facing instructions, including the two evaluation questions and Level A/B/C criteria.
- `background/`: scenario and context-field background materials.
- `example.md`: example constraints with reference explanations for Level A, Level B, and Level C.
- `questionnaire/`: blank evaluation forms used by evaluators.

The corresponding constraint files used in the human evaluation are provided under:

```text
../evaluation_results/results/RQ1/effectiveness_humanEvaluation/unique_constraints/
```
