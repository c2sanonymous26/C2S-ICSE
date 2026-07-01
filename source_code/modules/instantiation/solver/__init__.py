from fractions import Fraction
from z3 import z3

# Types
EFormulaDict = dict[tuple[str, int, int], tuple[str, str]] # ((node_id, depth, rlayer), (left_node_id, right_node_id))
EStruct = frozenset[str] # set of node_ids
EStructList = list[EStruct]
VEConstraint = tuple[z3.BoolRef, int] # (constraint, weight) if weight is -1, it means strong constraint

SymbolInequalities = dict[tuple[str, str], set[Fraction] | set[str]] # (op, symbol, values)
SymbolDomains = dict[str, list[Fraction] | list[str]] # (symbol, domains)

TruthValueInfo = dict[str, list[int]] # (node_id, truth_values)


# Constants
TACTICS_BATCH_SIZE: int = 10

SOLVED_MODEL_NUM: int = 3

CONSECUTIVE_BACKTRACKING_NUM: int = 3

from .solve import solve, SOLVE_TIMEOUT # noqa: E402

__all__ = [
    "solve",
    "SOLVE_TIMEOUT"
]
