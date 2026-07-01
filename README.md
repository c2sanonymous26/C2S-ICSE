# Artifacts of the submission "Crafting Data-Grounded Environmental Constraints via LLM-Symbolic Stepwise Refinement"

This repository contains the source code, evaluation results, and supplementary materials for the submission.

## Directory Structure

The dependency files `.python-version`, `pyproject.toml`, and `uv.lock` are placed in this root directory and shared by both `source_code/` and `evaluation_results/`.

### `source_code/`

This directory is the runnable source-code package of $\mathrm{C}^2\mathrm{S}$. It contains the scenario inputs and the implementation of the main pipeline:

- constraint invention, including intent and semantics generation and template synthesis;
- parameter instantiation;
- constraint extraction;
- constraint checking;
- auxiliary scripts for semantic checking, duplicate checking, perturbation generation, and result analysis;
- the $\mathrm{AR+}$ baseline implementation.

The source-code package is intended for users who want to run $\mathrm{C}^2\mathrm{S}$ on the provided taxi scenario or inspect the implementation details. Runtime directories such as `outputs/`, `constraints/`, and `evaluation/` are created inside `source_code/` when commands are executed.

To run the source code, first enter this directory and follow `source_code/README.md`.

### `evaluation_results/`

This directory contains the released experimental artifacts used for the paper evaluation. It includes:

- synthesized constraints used in RQ1, RQ2, RQ3, the case study, and the preliminary LLM tests;
- intermediate outputs retained for reproducing the final results;
- final result files, figures, and tables reported in the paper;
- scripts for regenerating the released figures, tables, and summary JSON files from the included intermediate outputs;
- the input data needed by the evaluation scripts.

This package is intended for users who want to inspect the reported results or verify the result-generation scripts without rerunning the full synthesis pipeline. The full source-code pipeline is provided separately under `source_code/`.

To rerun the evaluation scripts, first enter this directory and follow `evaluation_results/README.md`.

### `supplementary_materials/`

This directory contains additional materials that support the methodology and evaluation but are not required for running the source code. It includes:

- prompt files documenting the main LLM-facing instructions used by the approach;
- unit-inference rules used by the unit validation mechanism;
- human-evaluation guidelines for RQ1, including evaluator instructions, background materials, example constraints, and blank questionnaire forms.

These materials are intended for readers who want to inspect the prompts, understand the unit-validation rule set, or review how the human evaluation was conducted.

See `supplementary_materials/README.md` for details.

## Requirements

- Operating system
  - The artifacts have been prepared and tested on macOS 26.2 and Ubuntu 24.04 LTS.

- Python
  - The source code and evaluation scripts require Python `>=3.10.12, <3.11`.
  - We prepared and tested the artifacts with Python `3.10.12`, which we recommend for reproduction.

- `uv`
  - Required for dependency installation and command execution.
  - If Python `3.10.12` is not available on your machine, install it first with `uv`:

    ```bash
    uv python install 3.10.12
    ```

  - Then install the dependencies from this artifact root directory with the provided lock file:

    ```bash
    uv sync --python 3.10.12 --locked
    ```

    > **Reproducibility Note.**
    > Use `uv sync --python 3.10.12 --locked` from the artifact root directory when setting up the environment. The `--locked` flag forces `uv` to install exactly the dependency versions recorded in `uv.lock`; without it, `uv` may resolve newer dependency versions from `pyproject.toml`, which can introduce API-incompatible changes.

## LLM Configuration

Running the $\mathrm{C}^2\mathrm{S}$ source code requires the following environment variables:

```bash
export C2S_MODEL="provider:model_id"
export C2S_API_KEY="your-api-key"
export C2S_LLM_OUTPUT_MODE="schema"  # one of: json, schema, prompt
```

At present, $\mathrm{C}^2\mathrm{S}$ supports two model providers:

- `openrouter`
- `ark`

Example model values:

| Model | Example `C2S_MODEL` |
| --- | --- |
| GPT-5.5 | `openrouter:openai/gpt-5.5` |
| Claude Sonnet 4.6 | `openrouter:anthropic/claude-sonnet-4.6` |
| DeepSeek V3.2 | `ark:deepseek-v3-2-251201` |
| DeepSeek V4 Flash | `ark:deepseek-v4-flash-260425` |

`C2S_LLM_OUTPUT_MODE` controls how structured LLM outputs are requested:

- `schema`: use the provider's native JSON-schema structured-output interface.
- `json`: use the provider's JSON mode.
- `prompt`: do not request provider-side structured output; $\mathrm{C}^2\mathrm{S}$ asks for JSON in the prompt and parses the returned text locally.

Tested output-mode support:

| Model | Supported `C2S_LLM_OUTPUT_MODE` |
| --- | --- |
| GPT-5.5 | `schema`, `json`, `prompt` |
| Claude Sonnet 4.6 | `schema`, `json`, `prompt` |
| DeepSeek V3.2 | `schema`, `json`, `prompt` |
| DeepSeek V4 Flash | `prompt` |
