from pathlib import Path

from .. import INPUT_DIR

def construct_ctx_data(scenario: str, data: str, is_symbolic: bool) -> tuple[dict[str, Path] | None, dict[str, Path] | None]:
    
    data_dir = INPUT_DIR / scenario / "data" / f'{data}.csv'
    if not data_dir.exists() or not data_dir.is_file():
        raise FileNotFoundError(f"Data {data_dir} not found")
    
    if is_symbolic:
        solve_ctx2data = {'ctx1': data_dir}
        validate_ctx2data = None
    else:
        solve_ctx2data = None
        validate_ctx2data = {'ctx1': data_dir}
    
    return solve_ctx2data, validate_ctx2data

