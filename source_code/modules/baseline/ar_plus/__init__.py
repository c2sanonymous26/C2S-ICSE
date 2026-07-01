# AR+ adapts and enhances the core constraint-generation pipeline of the
# original AutoReconciler (AR):
# 1. It adapts data preparation and data source construction to the taxi
#    dataset.
# 2. It extends assertion mining from equality-only assertions to both equality
#    and inequality assertions.
# 3. It expands the expression search space from basic arithmetic operators to
#    basic operators plus common mathematical functions.

LEVEL1_SEPARATOR = "=" * 70
LEVEL2_SEPARATOR = "*" * 70

SCENARIO = "taxi"

# Available options for random sampling
AVAILABLE_MODES = ["single", "pairwise", "carid_join", "carid_diff"]
AVAILABLE_CMPS = ["eq", "le", "lt", "ge", "gt"]
