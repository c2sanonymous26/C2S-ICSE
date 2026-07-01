# Source Code for $\mathrm{C}^2\mathrm{S}$

This repository is the source code for $\mathrm{C}^2\mathrm{S}$, an approach that systematically synthesizes useful context constraints by integrating LLM-based semantic interpretation with context symbolic computation.

For convenience, $\mathrm{C}^2\mathrm{S}$ is written as `C2S` in directory names and generated files in this repository.

## Repository Structure

- `inputs/`
  - Scenario inputs.
  - `inputs/taxi/` contains the necessary inputs for the taxi-management scenario. It includes the scenario description, context schema, collected context data, perturbation data, and few-shot examples.
    > **Privacy Note.** 
    > To avoid privacy leakage, the context data in `inputs/taxi/data` has been obfuscated. Although some values may still appear to correspond to the physical world, such correspondence should not be taken seriously and should not be interpreted as reflecting the real world.
    >
    > For the modern mobile communication scenario (case study), due to privacy and permission restrictions, we are not allowed to release the original data or the intermediate outputs.
- `modules/`
  - Core modules of $\mathrm{C}^2\mathrm{S}$.
  - `modules.invention`: Intent and semantics generation (stage 1) and template synthesis (stage 2).
  - `modules.instantiation`: Parameter instantiation (stage 3).
  - `modules.check`: Constraint-checking algorithm for RQ2 perturbation signaling.
  - `modules.utils`: Utility code and scripts.
  - `modules.baseline`: Extended $\mathrm{AR+}$ implementation.
- `.gitignore`
- `README.md`

Runtime directories such as `outputs/`, `constraints/`, and `evaluation/` are generated when commands are executed and are not included in the initial source-code directory.

## Requirements

Before running commands in this directory, please follow the environment setup and LLM-configuration instructions in the root [`README.md`](../README.md). The shared dependency files `.python-version`, `pyproject.toml`, and `uv.lock` are provided in the artifact root directory.

After the environment is configured, run the source-code commands from this `source_code/` directory.

## Quick Start

> **Note**: In commands, values enclosed in angle brackets, such as `<run_dir>` or `<constraint_dir>`, are placeholders that should be replaced with concrete values for your run.

For a quick end-to-end run in the taxi-management scenario, execute the following steps.

1. Generate a constraint template. This step corresponds to stage 1 (intent and semantics generation) and stage 2 (template synthesis) in the paper:

```bash
uv run -m modules.invention --scenario taxi --invent-times 1 --scope 1
```

On the first run, $\mathrm{C}^2\mathrm{S}$ downloads the embedding model from Hugging Face, so please ensure that your environment can access Hugging Face.

2. Find the generated directory under `outputs/invention/converter/taxi/`, denoted below as `<run_dir>`, and run parameter instantiation (stage 3):

```bash
uv run -m modules.instantiation --scenario taxi --run-dir <run_dir> --data 5000 --concurrent
```

The instantiation results can then be found under:

- `outputs/instantiation/<run_dir>/`

3. Extract constraints:

```bash
uv run -m modules.utils.scripts.extract_constraints --scenario taxi --run-dir <run_dir> --output-dir <constraint_dir>
```

Here `<constraint_dir>` is a user-specified output directory name under `constraints/`.

The extracted constraints can then be found under:

- `constraints/<constraint_dir>/C2S/`

## Detailed Instructions

### Constraint Template Synthesis

Use the following command:

```bash
uv run -m modules.invention \
  --scenario taxi \
  --invent-times <invent_times> \
  [--scope <scope>] \
  [--existing-dirs <dir1,dir2,...>] \
  [--disable-similarity-check] \
  [--disable-semantic-validation] \
  [--disable-parameter-domain-discretization] \
  [--disable-predicate-sensitivity-promotion]
```

Required arguments:
- `--scenario`: scenario name, e.g. `taxi`.
- `--invent-times`: number of synthesis attempts in one run.

Optional arguments:
- `--scope`: controls the scope of constraint synthesis. For a quick start, we recommend `--scope 1`, as it leads to simpler constraints with a single quantifier layer. **The experiments in the paper were conducted without restricting the scope.**
- `--existing-dirs`: comma-separated `run-dir` names used as existing history to avoid repeated synthesis. Each `run-dir` must already exist under `outputs/invention/inventor/<scenario>/`.
- `--disable-*`: disable `similarity-checking`, `semantic-validation`, `parameter-domain-discretization`, and `predicate-sensitivity-promotion`.

The results are written to:

- `outputs/invention/inventor/taxi/<run_dir>/`
- `outputs/invention/converter/taxi/<run_dir>/`

Here `<run_dir>` is the generated directory name under `outputs/invention/inventor/<scenario>/` and `outputs/invention/converter/<scenario>/`. It includes a four-bit configuration code for the four internal mechanisms in the following order:

- similarity-checking
- semantic-validation
- parameter-domain-discretization
- predicate-sensitivity-promotion

For example, `1111` means that all four mechanisms are enabled.

For the paper experiments, we use six configurations built from these mechanisms. The abbreviations are: SC for similarity checking, UV for the unit validation mechanism controlled by `--disable-semantic-validation`, PD for parameter-domain discretization, and PP for predicate-sensitivity promotion.

| Config | SC | UV | PD | PP | Invention args |
| --- | --- | --- | --- | --- | --- |
| `Base` |  |  |  |  | `--disable-similarity-check --disable-semantic-validation --disable-parameter-domain-discretization --disable-predicate-sensitivity-promotion` |
| `+SC` | yes |  |  |  | `--disable-semantic-validation --disable-parameter-domain-discretization --disable-predicate-sensitivity-promotion` |
| `+UV` |  | yes |  |  | `--disable-similarity-check --disable-parameter-domain-discretization --disable-predicate-sensitivity-promotion` |
| `+PD` |  |  | yes |  | `--disable-similarity-check --disable-semantic-validation --disable-predicate-sensitivity-promotion` |
| `+PP` |  |  |  | yes | `--disable-similarity-check --disable-semantic-validation --disable-parameter-domain-discretization` |
| `Full` | yes | yes | yes | yes | no disable flags |

The generated four-bit code follows the same mechanism order: SC, UV, PD, and PP. Thus `0000` corresponds to `Base`, `1000` to `+SC`, `0100` to `+UV`, `0010` to `+PD`, `0001` to `+PP`, and `1111` to `Full`.

For configurations where PD or PP is disabled during template synthesis, use the matching disable flag again during parameter instantiation so that the instantiation stage follows the same configuration.

### Parameter Instantiation

Use the following command:

```bash
uv run -m modules.instantiation \
  --scenario taxi \
  --run-dir <run_dir> \
  --data 5000 \
  [--concurrent] \
  [--disable-parameter-domain-discretization] \
  [--disable-predicate-sensitivity-promotion]
```

Required arguments:
- `--scenario`: scenario name, e.g. `taxi`.
- `--run-dir`: one or more `run-dir` names under `outputs/invention/converter/<scenario>/`. If multiple `run-dir`s are given, their instantiated constraints are extracted and merged in the given order.
- `--data`: context data file name, e.g. `5000`.

Optional arguments:
- `--concurrent`: enable concurrent solving and validation.
- `--disable-parameter-domain-discretization`: disable parameter-domain discretization.
- `--disable-predicate-sensitivity-promotion`: disable predicate-sensitivity promotion.

The results are written to:

- `outputs/instantiation/<run_dir>/`

### Constraint Extraction

Use the following command:

```bash
uv run -m modules.utils.scripts.extract_constraints \
  --scenario taxi \
  --run-dir <run_dir> \
  --output-dir <constraint_dir>
```

Required arguments:
- `--scenario`: scenario name, e.g. `taxi`.
- `--run-dir`: one or more `run-dir` names under `outputs/instantiation/`.
- `--output-dir`: output directory name under `constraints/`.

The results are written to:

- `constraints/<constraint_dir>/<method_dir>/`

Here `<method_dir>` is `C2S` for the `1111` configuration, and `C2S_<config>` for other configurations.

## Auxiliary Modules and Scripts

### Constraint Checking and Result Analysis

$\mathrm{C}^2\mathrm{S}$ also provides a constraint-checking algorithm and a script for analyzing perturbation-signal results.

Constraint checking:

```bash
uv run -m modules.check \
  --scenario taxi \
  --constraint-dir constraints/<constraint_dir>/<method_dir> \
  --perturbation-prob <perturbation_prob>
```

Here `<perturbation_prob>` denotes a perturbation-probability setting, such as `5000_pp_0.1`, whose corresponding data is under `inputs/taxi/data/<perturbation_prob>/`.

The results are written to:

- `outputs/check/<constraint_dir>/<method_dir>/<perturbation_prob>/...`

Result analysis:

```bash
uv run -m modules.utils.scripts.evaluate_perturbation_signal \
  --scenario taxi \
  --constraint-dir constraints/<constraint_dir>/<method_dir> \
  --check-dir outputs/check/<constraint_dir>/<method_dir> \
  --perturbation-data-prob <perturbation_prob>
```

The results are written to:

- `evaluation/perturbation_signal/<constraint_dir>/<method_dir>/<perturbation_prob>/`

### Auxiliary Scripts

$\mathrm{C}^2\mathrm{S}$ also provides auxiliary scripts for duplicate checking and semantic checking on $\mathrm{C}^2\mathrm{S}$ synthesized constraints. They support `C2S` and `C2S_<config>` constraint directories, but not AR+.

Duplicate checking:

```bash
uv run -m modules.utils.scripts.duplicate_check \
  --scenario taxi \
  --constraint-dir constraints/<constraint_dir>/C2S
```

The results are written to:

- `evaluation/duplicate_check/<constraint_dir>/C2S/`

Semantic checking for unit validation:

```bash
uv run -m modules.utils.scripts.semantic_check \
  --scenario taxi \
  --constraint-dir constraints/<constraint_dir>/C2S
```

The results are written to:

- `evaluation/unit_validation/<constraint_dir>/C2S/results.json`

This script reports whether each extracted $\mathrm{C}^2\mathrm{S}$ constraint is semantically well-formed for unit validation, including parameter scope, signature consistency, implementation consistency, and unit compatibility.

### Baseline

AR+ baseline:

```bash
uv run -m modules.baseline.ar_plus \
  --data-file inputs/taxi/data/5000.csv \
  --run-times <run_times> \
  --output-dir constraints/<constraint_dir>/AR+ \
  [--scope single]
```

The optional `--scope single` flag is only for artifact trial runs. It fixes AR+ to single-context assertion mining, making a quick trial easier to inspect. **The paper experiments did not use this restriction.**

The command above writes AR+ raw outputs under `constraints/<constraint_dir>/AR+/raw/`. Convert them to XML/Python constraint files and generate the analysis report with:

```bash
uv run -m modules.baseline.ar_plus.convert_and_analyze \
  --input-dir constraints/<constraint_dir>/AR+
```

After conversion, the AR+ constraints and report are available under `constraints/<constraint_dir>/AR+/`.


The AR+ unit-validation script is available as:

```bash
uv run -m modules.baseline.scripts.ar_plus_unit_validation \
  <constraint_dir> \
  --scenario taxi
```

The AR+ unit-validation results are written to `evaluation/unit_validation/<constraint_dir>/AR+/results.json`.

