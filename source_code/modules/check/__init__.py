from ..utils import CHCK_LOGGER_NAME as LOGGER_NAME # noqa: F401
from ..utils import OUTPUT_DIR

CHECK_OUTPUT_DIR = OUTPUT_DIR / "check"
INCS_FILE_NAME = "incs.csv"

INDENT = 4

Link = frozenset[tuple[str, str]]
CheckResult = tuple[bool, frozenset[Link]]