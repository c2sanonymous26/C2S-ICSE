# -*- coding: utf-8 -*-
"""AR+ constraint converter.

Converts AR+ generated JSON constraints to cminer-format Python functions and XML constraints.
"""

import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from fractions import Fraction  # Still needed for fraction calculation

# Use built-in expression parsing method


@dataclass
class ConversionResult:
    """Conversion result"""
    constraint_id: int
    python_code: str
    xml_code: str
    bfunc_count: int
    conversion_success: bool
    error_message: Optional[str] = None


class ExpressionParser:
    """Expression parser - converts functional expressions to Python code"""
    
    # Function mapping - implements gplearn's protected function logic
    FUNCTION_MAP = {
        'add': lambda a, b: f"({a} + {b})",
        'sub': lambda a, b: f"({a} - {b})",  
        'mul': lambda a, b: f"({a} * {b})",
        # Protected division: returns 1 if denominator in [-1/1000, 1/1000]
        'div': lambda a, b: f"(1 if -1/1000 <= ({b}) <= 1/1000 else ({a}) / ({b}))",
        # Protected square root: square root of absolute value
        'sqrt': lambda a: f"sqrt(abs({a}))",
        # Protected logarithm: log of absolute value, returns 0 for small values
        'log': lambda a: f"(0 if abs({a}) < 1/1000 else log(abs({a})))",
        # Protected inverse: returns 0 if argument in [-1/1000, 1/1000]
        'inverse': lambda a: f"(0 if -1/1000 <= ({a}) <= 1/1000 else 1 / ({a}))",
        'abs': lambda a: f"abs({a})",
        'neg': lambda a: f"(-{a})",
        'max': lambda a, b: f"max({a}, {b})",
        'min': lambda a, b: f"min({a}, {b})",
        'sin': lambda a: f"sin({a})",
        'cos': lambda a: f"cos({a})",
        'tan': lambda a: f"tan({a})",
        'pow': lambda a, b: f"pow({a}, {b})"
    }
    
    def __init__(self, mode: str):
        self.mode = mode
    
    def parse_expression(self, expr: str) -> str:
        """Parse functional expression and convert to Python code
        
        Args:
            expr: Functional expression, e.g. "add(mul(latitude, timestamp), 5.0)"
            
        Returns:
            str: Python expression, e.g. "((var_bindings['v1']['latitude'] * var_bindings['v1']['timestamp']) + 5.0)"
        """
        return self._parse_recursive(expr.strip())
    
    def _parse_recursive(self, expr: str) -> str:
        """Recursively parse expression"""
        expr = expr.strip()
        
        # Check if it's a numeric constant
        if self._is_number(expr):
            return self._number_to_fraction(expr)
            
        # Check if it's a variable
        if self._is_variable(expr):
            return self._parse_variable(expr)
            
        # Parse function call
        return self._parse_function_call(expr)
    
    def _is_number(self, s: str) -> bool:
        """Check if it's a number"""
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def _number_to_fraction(self, s: str) -> str:
        """Convert number string to fraction form"""
        try:
            num = float(s)
            frac = Fraction(num).limit_denominator()
            if frac.denominator == 1:
                return str(frac.numerator)
            else:
                return f"{frac.numerator}/{frac.denominator}"
        except ValueError:
            return s
    
    def _is_variable(self, s: str) -> bool:
        """Check if it's a variable"""
        # Variable pattern: starts with letter, may contain underscores and digits
        return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', s))
    
    def _parse_function_call(self, expr: str) -> str:
        """Parse function call"""
        # Match function name and parameters
        match = re.match(r'^(\w+)\((.*)\)$', expr)
        if not match:
            raise ValueError(f"Cannot parse expression: {expr}")
            
        func_name, args_str = match.groups()
        
        if func_name not in self.FUNCTION_MAP:
            raise ValueError(f"Unsupported function: {func_name}")
            
        # Parse arguments
        args = self._parse_arguments(args_str)
        
        # Apply function mapping
        func_mapper = self.FUNCTION_MAP[func_name]
        if len(args) == 1:
            return func_mapper(args[0])
        elif len(args) == 2:
            return func_mapper(args[0], args[1])
        else:
            raise ValueError(f"Wrong number of arguments for function {func_name}")
    
    def _parse_arguments(self, args_str: str) -> List[str]:
        """Parse function arguments"""
        if not args_str.strip():
            return []
            
        args = []
        current_arg = ""
        paren_count = 0
        
        for char in args_str:
            if char == ',' and paren_count == 0:
                args.append(self._parse_recursive(current_arg.strip()))
                current_arg = ""
            else:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                current_arg += char
        
        if current_arg.strip():
            args.append(self._parse_recursive(current_arg.strip()))
            
        return args
    
    def _parse_variable(self, var_name: str) -> str:
        """Parse variable name and map to correct var_bindings path
        
        Args:
            var_name: Variable name, e.g. "latitude", "latitude_1", "latitude_2"
            
        Returns:
            str: var_bindings path, e.g. "var_bindings['v1']['latitude']"
        """
        # Check if has suffix
        if var_name.endswith('_1'):
            base_var = var_name[:-2]
            return f"var_bindings['v1']['{base_var}']"
        elif var_name.endswith('_2'):
            base_var = var_name[:-2]  
            return f"var_bindings['v2']['{base_var}']"
        else:
            # No suffix, decide based on mode
            if self.mode == 'single':
                return f"var_bindings['v1']['{var_name}']"
            else:
                # In pairwise, carid_join, and carid_diff modes, variables without suffix default to v1
                return f"var_bindings['v1']['{var_name}']"


class PreconditionParser:
    """Precondition parser"""
    
    def __init__(self, mode: str):
        self.mode = mode
    
    def parse_preconditions(self, precondition_str: str) -> List[str]:
        """Parse precondition string
        
        Args:
            precondition_str: e.g. "frozenset({'speed_bin_0_5.7', 'direction_bin_0_15.75'})"
            
        Returns:
            List[str]: Python condition expression list
        """
        # Extract conditions from frozenset
        match = re.search(r"frozenset\(\{([^}]+)\}\)", precondition_str)
        if not match:
            raise ValueError(f"Cannot parse precondition: {precondition_str}")
            
        conditions_str = match.group(1)
        
        # Split individual conditions
        conditions = []
        for condition in conditions_str.split(','):
            condition = condition.strip().strip("'\"")
            if condition:
                conditions.append(self._parse_bin_condition(condition))
        
        return conditions
    
    def _parse_bin_condition(self, bin_str: str) -> str:
        """Parse single bin condition
        
        Args:
            bin_str: e.g. "speed_bin_0_5.7"
            
        Returns:
            str: Python condition, e.g. "(0 <= var_bindings['v1']['speed'] <= 5.7)"
        """
        # Parse bin format: {variable}_bin_{min}_{max}
        match = re.match(r'^(.+)_bin_(.+)_(.+)$', bin_str)
        if not match:
            raise ValueError(f"Cannot parse bin condition: {bin_str}")
            
        var_name, min_val, max_val = match.groups()
        
        # Determine variable path based on variable name suffix and mode
        if var_name.endswith('_1'):
            base_var = var_name[:-2]
            var_path = f"var_bindings['v1']['{base_var}']"
        elif var_name.endswith('_2'):
            base_var = var_name[:-2]
            var_path = f"var_bindings['v2']['{base_var}']"
        else:
            var_path = f"var_bindings['v1']['{var_name}']"
            
        return f"({min_val} <= {var_path} <= {max_val})"


class ConstraintConverter:
    """Main converter"""
    
    def __init__(self):
        self.expr_parser = None  # Will be initialized according to mode
        self.precond_parser = None  # Will be initialized according to mode
    
    def convert_constraint(self, json_data: Dict[str, Any], constraint_id: int) -> ConversionResult:
        """Convert single constraint
        
        Args:
            json_data: AR+ constraint JSON data
            constraint_id: Constraint ID
            
        Returns:
            ConversionResult: Conversion result
        """
        try:
            mode = json_data['mode']
            self.expr_parser = ExpressionParser(mode)
            self.precond_parser = PreconditionParser(mode)
            
            # Generate Python code
            python_code = self._generate_python_code(json_data, constraint_id)
            
            # Generate XML code
            xml_code = self._generate_xml_code(json_data, constraint_id)
            
            return ConversionResult(
                constraint_id=constraint_id,
                python_code=python_code,
                xml_code=xml_code,
                bfunc_count=self._count_bfuncs(json_data),
                conversion_success=True
            )
            
        except Exception as e:
            logging.error(f"Failed to convert constraint {constraint_id}: {e}")
            return ConversionResult(
                constraint_id=constraint_id,
                python_code="",
                xml_code="",
                bfunc_count=0,
                conversion_success=False,
                error_message=str(e)
            )
    
    def _generate_python_code(self, json_data: Dict[str, Any], constraint_id: int) -> str:
        """Generate Python code"""
        mode = json_data['mode']
        cmp = json_data['cmp']
        target_col = json_data['target_col']
        assertion = json_data['assertion']
        status = json_data['status']
        
        lines = [
            "from math import *",
            "from typing import Any",
            ""
        ]
        
        bfunc_id = 1
        
        # Handle fixed precondition for carid_join mode
        if mode == 'carid_join':
            lines.append(f"def bfunc_{bfunc_id}_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:")
            lines.append("    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']")
            lines.append("")
            bfunc_id += 1
        
        # Handle fixed precondition for carid_diff mode
        if mode == 'carid_diff':
            lines.append(f"def bfunc_{bfunc_id}_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:")
            lines.append("    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']")
            lines.append("")
            bfunc_id += 1
        
        # Handle user-defined preconditions
        if status == "success_with_preconditions":
            precondition_str = json_data['precondition']
            preconditions = self.precond_parser.parse_preconditions(precondition_str)
            
            for i, precond in enumerate(preconditions, 1):
                lines.append(f"def bfunc_{bfunc_id}_c{i}(var_bindings: dict[str, dict[str, Any]]) -> bool:")
                lines.append(f"    return {precond}")
                lines.append("")
            bfunc_id += 1
        
        # Generate assertion bfunc
        assertion_expr = self.expr_parser.parse_expression(assertion)
        target_var = self.expr_parser._parse_variable(target_col)
        
        # Comparison operator mapping
        cmp_map = {
            'eq': '==',
            'le': '<=', 
            'lt': '<',
            'ge': '>=',
            'gt': '>'
        }
        
        cmp_op = cmp_map[cmp]
        
        lines.append(f"def bfunc_{bfunc_id}_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:")
        lines.append(f"    return {target_var} {cmp_op} {assertion_expr}")
        lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_xml_code(self, json_data: Dict[str, Any], constraint_id: int) -> str:
        """Generate XML code"""  
        mode = json_data['mode']
        status = json_data['status']
        
        lines = ["<?xml version='1.0' encoding='UTF-8'?>", "<formula>"]
        
        # Determine forall structure based on mode
        if mode == 'single':
            lines.append('  <forall var="v1" in="ctx1">')
            indent = "    "
        else:  # pairwise, carid_join, or carid_diff
            lines.append('  <forall var="v1" in="ctx1">')
            lines.append('    <forall var="v2" in="ctx1">')
            indent = "      "
        
        # Build logical structure
        bfunc_id = 1
        bfunc_refs = []
        
        # Fixed precondition for carid_join
        if mode == 'carid_join':
            bfunc_refs.append(f'<bfunc id="{bfunc_id}_c1"/>')
            bfunc_id += 1
        
        # Fixed precondition for carid_diff
        if mode == 'carid_diff':
            bfunc_refs.append(f'<bfunc id="{bfunc_id}_c1"/>')
            bfunc_id += 1
        
        # User-defined preconditions
        if status == "success_with_preconditions":
            precondition_str = json_data['precondition']
            preconditions = self.precond_parser.parse_preconditions(precondition_str)
            
            for i in range(len(preconditions)):
                bfunc_refs.append(f'<bfunc id="{bfunc_id}_c{i+1}"/>')
            bfunc_id += 1
        
        # Assertion bfunc
        assertion_ref = f'<bfunc id="{bfunc_id}_c1"/>'
        
        # Build logical expression
        if not bfunc_refs:
            # No preconditions, use assertion directly
            lines.append(f"{indent}{assertion_ref}")
        else:
            # Has preconditions, use implies structure
            lines.append(f"{indent}<implies>")
            
            if len(bfunc_refs) == 1:
                # Single precondition
                lines.append(f"{indent}  {bfunc_refs[0]}")
            else:
                # Multiple preconditions, use and
                lines.append(f"{indent}  <and>")
                for ref in bfunc_refs:
                    lines.append(f"{indent}    {ref}")
                lines.append(f"{indent}  </and>")
            
            lines.append(f"{indent}  {assertion_ref}")
            lines.append(f"{indent}</implies>")
        
        # Close forall tags
        if mode == 'single':
            lines.append("  </forall>")
        else:
            lines.append("    </forall>")
            lines.append("  </forall>")
        
        lines.append("</formula>")
        
        return '\n'.join(lines)
    
    def _count_bfuncs(self, json_data: Dict[str, Any]) -> int:
        """Count number of bfuncs"""
        mode = json_data['mode']
        status = json_data['status']
        
        count = 0
        
        # Fixed precondition for carid_join mode
        if mode == 'carid_join':
            count += 1
        
        # Fixed precondition for carid_diff mode
        if mode == 'carid_diff':
            count += 1
        
        # User-defined preconditions
        if status == "success_with_preconditions":
            precondition_str = json_data['precondition']
            preconditions = self.precond_parser.parse_preconditions(precondition_str)
            count += len(preconditions)
        
        # Assertion bfunc (always has one)
        count += 1
        
        return count


class LogParser:
    """Log file parser"""
    
    def parse_log_file(self, log_file: Path) -> Dict[str, Any]:
        """Parse single log file and extract run parameters and time information
        
        Args:
            log_file: Log file path
            
        Returns:
            Dict: Dictionary containing mode, cmp, target_col, start_time, end_time, duration, success
        """
        from datetime import datetime
        
        result = {
            'mode': 'unknown',
            'cmp': 'unknown', 
            'target_col': 'unknown',
            'start_time': None,
            'end_time': None,
            'duration': 0.0,
            'success': False
        }
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line in lines:
                # Parse mode and comparison operator
                if 'Mode:' in line and 'Comparison:' in line:
                    # Format: "2025-07-28 11:16:29,341 - INFO - Mode: single, Comparison: lt"
                    parts = line.split('Mode:')[1].strip()
                    mode_cmp = parts.split('Comparison:')
                    if len(mode_cmp) == 2:
                        result['mode'] = mode_cmp[0].strip().rstrip(',')
                        result['cmp'] = mode_cmp[1].strip()
                
                # Parse target field
                elif 'Target field:' in line:
                    # Format: "2025-07-28 11:16:29,350 - INFO - Target field: latitude (selected from 5 candidates)"
                    parts = line.split('Target field:')[1].strip()
                    target_col = parts.split('(')[0].strip()
                    result['target_col'] = target_col
                
                # Parse start time
                elif 'Starting run' in line:
                    # Format: "2025-07-30 14:16:35,667 - INFO - Starting run 1/50"
                    timestamp_str = line.split(' - ')[0]
                    try:
                        result['start_time'] = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                    except ValueError:
                        pass
            
            # Parse end time (search backwards from last line)
            for line in reversed(lines):
                if ('successfully generated constraint' in line) or ('failed to generate constraint' in line):
                    # Format: "2025-07-30 14:16:37,019 - INFO - Run 1 successfully generated constraint"
                    # Or: "2025-07-30 14:19:12,188 - WARNING - Run 3 failed to generate constraint"
                    timestamp_str = line.split(' - ')[0]
                    try:
                        result['end_time'] = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                        result['success'] = 'successfully generated constraint' in line
                    except ValueError:
                        pass
                    break
            
            # Calculate duration
            if result['start_time'] and result['end_time']:
                duration = result['end_time'] - result['start_time']
                result['duration'] = duration.total_seconds()
                        
        except Exception as e:
            logging.warning(f"Error parsing log file {log_file}: {e}")
            
        return result
    
    def parse_all_logs(self, raw_dir: Path) -> List[Dict[str, Any]]:
        """Parse all log files
        
        Args:
            raw_dir: raw directory path
            
        Returns:
            List[Dict]: List of parameters and time information for all runs
        """
        log_files = list(raw_dir.glob("*.log"))
        all_runs = []
        
        for log_file in log_files:
            run_params = self.parse_log_file(log_file)
            # Add filename information for debugging
            run_params['log_file'] = log_file.name
            all_runs.append(run_params)
            
        return all_runs


class ConstraintAnalyzer:
    """Constraint statistics analyzer"""
    
    def analyze_constraints(self, json_files: List[Path], raw_dir: Path) -> Dict[str, Any]:
        """Analyze constraint statistics
        
        Args:
            json_files: List of JSON file paths
            raw_dir: raw directory path, used for counting log files
            
        Returns:
            Dict: Statistics information
        """
        # Parse all log files to get distribution of all runs
        log_parser = LogParser()
        all_runs = log_parser.parse_all_logs(raw_dir)
        total_runs = len(all_runs)
        successful_constraints = len(json_files)
        
        # Count distribution of all runs
        all_runs_stats = {
            'mode_distribution': {},
            'cmp_distribution': {},
            'target_col_distribution': {}
        }
        
        for run in all_runs:
            mode = run.get('mode', 'unknown')
            cmp = run.get('cmp', 'unknown')
            target_col = run.get('target_col', 'unknown')
            
            all_runs_stats['mode_distribution'][mode] = all_runs_stats['mode_distribution'].get(mode, 0) + 1
            all_runs_stats['cmp_distribution'][cmp] = all_runs_stats['cmp_distribution'].get(cmp, 0) + 1
            all_runs_stats['target_col_distribution'][target_col] = all_runs_stats['target_col_distribution'].get(target_col, 0) + 1
        
        # Calculate time statistics for all runs (from log files)
        all_runs_total_time = sum(run.get('duration', 0.0) for run in all_runs)
        successful_runs_from_log = sum(1 for run in all_runs if run.get('success', False))
        
        # Initialize statistics structure
        stats = {
            'total_runs': total_runs,
            'all_runs_stats': all_runs_stats,
            'successful_constraints': successful_constraints,
            'success_rate': successful_constraints / total_runs if total_runs > 0 else 0.0,
            
            # Time statistics for all runs (from log files)
            'all_runs_time_stats': {
                'total_time_from_logs': all_runs_total_time,
                'avg_time_from_logs': all_runs_total_time / total_runs if total_runs > 0 else 0.0,
                'successful_runs_from_logs': successful_runs_from_log
            },
            
            # Detailed statistics for successful constraints
            'successful_constraints_stats': {
            'status_distribution': {},
                'mode_distribution': {},
                'cmp_distribution': {},
            'target_col_distribution': {},
            'fit_rate_stats': {
                'perfect_fit_count': 0,
                'avg_fit_rate': 0.0,
                'min_fit_rate': 1.0,
                    'max_fit_rate': 0.0,
                    'fit_rates': []
                },
                'time_stats': {
                    'total_time': 0.0,
                    'avg_time_among_successful': 0.0,
                    'avg_asrtm_time_among_successful': 0.0,
                    'avg_predm_time_among_successful': 0.0
                }
            }
        }
        
        if json_files:
            total_fit_rate = 0.0
            total_time = 0.0
            total_asrtm_time = 0.0
            total_predm_time = 0.0
            
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Mode distribution of successful constraints
                    mode = data.get('mode', 'unknown')
                    stats['successful_constraints_stats']['mode_distribution'][mode] = stats['successful_constraints_stats']['mode_distribution'].get(mode, 0) + 1
                    
                    # Comparison operator distribution of successful constraints
                    cmp = data.get('cmp', 'unknown')
                    stats['successful_constraints_stats']['cmp_distribution'][cmp] = stats['successful_constraints_stats']['cmp_distribution'].get(cmp, 0) + 1
                    
                    # Status distribution of successful constraints
                    status = data.get('status', 'unknown')
                    stats['successful_constraints_stats']['status_distribution'][status] = stats['successful_constraints_stats']['status_distribution'].get(status, 0) + 1
                    
                    # Target column distribution of successful constraints
                    target_col = data.get('target_col', 'unknown')
                    stats['successful_constraints_stats']['target_col_distribution'][target_col] = stats['successful_constraints_stats']['target_col_distribution'].get(target_col, 0) + 1
                    
                    # Fit rate statistics
                    fit_rate = data.get('rule_fit_rate', 0.0)
                    total_fit_rate += fit_rate
                    stats['successful_constraints_stats']['fit_rate_stats']['fit_rates'].append(fit_rate)
                    
                    if fit_rate == 1.0:
                        stats['successful_constraints_stats']['fit_rate_stats']['perfect_fit_count'] += 1
                        
                    if fit_rate < stats['successful_constraints_stats']['fit_rate_stats']['min_fit_rate']:
                        stats['successful_constraints_stats']['fit_rate_stats']['min_fit_rate'] = fit_rate
                        
                    if fit_rate > stats['successful_constraints_stats']['fit_rate_stats']['max_fit_rate']:
                        stats['successful_constraints_stats']['fit_rate_stats']['max_fit_rate'] = fit_rate
                    
                    # Time statistics
                    overall_time = data.get('overall_time', 0.0)
                    asrtm_time = data.get('asrtm_time', 0.0)
                    predm_time = data.get('predm_time', 0.0)
                    
                    total_time += overall_time
                    total_asrtm_time += asrtm_time
                    total_predm_time += predm_time
                    
                except Exception as e:
                    logging.warning(f"Error analyzing file {json_file}: {e}")
                    continue
            
            # Calculate averages
            count = len(json_files)
            if count > 0:
                stats['successful_constraints_stats']['fit_rate_stats']['avg_fit_rate'] = total_fit_rate / count
                stats['successful_constraints_stats']['time_stats']['total_time'] = total_time
                # Average time of successful constraints (only count successful ones)
                stats['successful_constraints_stats']['time_stats']['avg_time_among_successful'] = total_time / count
                stats['successful_constraints_stats']['time_stats']['avg_asrtm_time_among_successful'] = total_asrtm_time / count
                stats['successful_constraints_stats']['time_stats']['avg_predm_time_among_successful'] = total_predm_time / count
        
        return stats


def get_project_paths(script_file: Path):
    """Get project paths"""
    script_dir = script_file.parent.resolve()
    proj_dir = next(
        parent for parent in [script_dir, *script_dir.parents]
        if (parent / "modules").is_dir()
    )
    return script_dir, proj_dir


def convert_and_analyze(
    analyze_only: bool = False,
    input_dir: Path | str | None = None,
) -> Dict[str, Any]:
    """Main function: convert constraints and analyze statistics
    
    Args:
        analyze_only: If True, only analyze without converting
        
    Returns:
        Dict: Dictionary containing conversion results and statistics
    """
    if input_dir is None:
        raise ValueError("input_dir must be specified")

    input_path = Path(input_dir)
    if not input_path.is_absolute():
        _, proj_dir = get_project_paths(Path(__file__))
        input_path = proj_dir / input_path

    output_path = input_path
    
    # Ensure input directory exists
    if not input_path.exists():
        raise ValueError(f"Input directory does not exist: {input_path}")
    
    # JSON files are in raw subdirectory
    raw_dir = input_path / "raw"
    if not raw_dir.exists():
        raise ValueError(f"raw directory does not exist: {raw_dir}")
    
    logging.info(f"Starting to process directory: {raw_dir}")
    
    # Find all JSON files
    json_files = list(raw_dir.glob("*.json"))
    
    if not json_files:
        logging.warning(f"No JSON files found in directory {raw_dir}")
        return {"error": "No JSON files found"}
    
    logging.info(f"Found {len(json_files)} JSON files")
    
    # Analyze statistics
    analyzer = ConstraintAnalyzer()
    stats = analyzer.analyze_constraints(json_files, raw_dir)
    
    result = {
        "statistics": stats,
        "conversion_results": []
    }
    
    # If analyze only, save analysis report and return directly
    if analyze_only:
        logging.info("Analyze-only mode, skipping conversion")
        
        # Save analysis report
        analysis_file = input_path / "analysis_report.json"
        stats = result["statistics"]
        analysis_data = {
            "total_runs": stats["total_runs"],
            "all_runs_stats": stats["all_runs_stats"],
            "all_runs_time_stats": stats["all_runs_time_stats"],
            "successful_constraints": stats["successful_constraints"],
            "success_rate": stats["success_rate"],
            "successful_constraints_stats": stats["successful_constraints_stats"]
        }
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2, default=str)
        
        logging.info(f"Analysis report saved: {analysis_file}")
        return result
    
    # Convert constraints
    converter = ConstraintConverter()
    successful_conversions = 0
    failed_conversions = 0
    
    py_dir = output_path / "py"
    xml_dir = output_path / "xml"
    
    if not analyze_only:
        py_dir.mkdir(parents=True, exist_ok=True)
        xml_dir.mkdir(parents=True, exist_ok=True)
    
    for json_file in json_files:
        try:
            # Extract constraint ID (from filename)
            constraint_id = int(re.search(r'constraint_(\d+)', json_file.stem).group(1))
            
            # Load JSON data
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Convert constraint
            conversion_result = converter.convert_constraint(json_data, constraint_id)
            result["conversion_results"].append(conversion_result)
            
            if conversion_result.conversion_success:
                successful_conversions += 1
                
                # Save conversion result
                if not analyze_only:
                    # Save Python file
                    py_filename = f"bfuncs_{constraint_id}.py"
                    py_filepath = py_dir / py_filename
                    with open(py_filepath, 'w', encoding='utf-8') as f:
                        f.write(conversion_result.python_code)
                    
                    # Save XML file
                    xml_filename = f"constraint_{constraint_id}.xml"
                    xml_filepath = xml_dir / xml_filename
                    with open(xml_filepath, 'w', encoding='utf-8') as f:
                        f.write(conversion_result.xml_code)
                    
                    logging.info(f"Constraint {constraint_id} conversion successful: {py_filename}, {xml_filename}")
            else:
                failed_conversions += 1
                logging.error(f"Constraint {constraint_id} conversion failed: {conversion_result.error_message}")
                
        except Exception as e:
            failed_conversions += 1
            logging.error(f"Error processing file {json_file}: {e}")
            continue
    
    # Add conversion statistics
    result["conversion_stats"] = {
        "total_processed": len(json_files),
        "successful_conversions": successful_conversions,
        "failed_conversions": failed_conversions,
        "success_rate": successful_conversions / len(json_files) if json_files else 0.0
    }
    
    # Save analysis report
    analysis_file = output_path / "analysis_report.json"
    stats = result["statistics"]
    analysis_data = {
        "total_runs": stats["total_runs"],
        "all_runs_stats": stats["all_runs_stats"],
        "all_runs_time_stats": stats["all_runs_time_stats"],
        "successful_constraints": stats["successful_constraints"],
        "success_rate": stats["success_rate"],
        "successful_constraints_stats": stats["successful_constraints_stats"],
        "conversion_stats": result.get("conversion_stats", {})
    }
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2, default=str)
    
    logging.info(f"Analysis report saved: {analysis_file}")
    logging.info(f"Conversion complete: {successful_conversions}/{len(json_files)} successful")
    return result


def main():
    """Main function - command line entry"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AR+ constraint converter and analyzer")
    parser.add_argument("--analyze-only", action="store_true", help="Only analyze statistics without converting")
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="AR+ constraint directory containing raw/.",
    )
    args = parser.parse_args()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Call main function
    try:
        result = convert_and_analyze(
            analyze_only=args.analyze_only,
            input_dir=args.input_dir,
        )
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Print statistics
    if "statistics" in result:
        stats = result["statistics"]
        all_runs_stats = stats['all_runs_stats']
        all_runs_time_stats = stats['all_runs_time_stats']
        succ_stats = stats['successful_constraints_stats']
        
        print("\n=== AR+ Constraint Analysis Report ===")
        print(f"Total runs: {stats['total_runs']}")
        print(f"All runs mode distribution: {all_runs_stats['mode_distribution']}")
        print(f"All runs comparison operator distribution: {all_runs_stats['cmp_distribution']}")
        print(f"All runs target column distribution: {all_runs_stats['target_col_distribution']}")
        print(f"All runs total time: {all_runs_time_stats['total_time_from_logs']:.2f}s")
        print(f"All runs average time: {all_runs_time_stats['avg_time_from_logs']:.2f}s")
        print(f"Successful runs from log statistics: {all_runs_time_stats['successful_runs_from_logs']}")
        
        print("\n=== Successful Constraint Statistics ===")
        print(f"\nSuccessfully generated constraints: {stats['successful_constraints']}")
        print(f"Success rate: {stats['success_rate']:.2%}")
        print(f"Successful constraint status distribution: {succ_stats['status_distribution']}")
        print(f"Successful constraint mode distribution: {succ_stats['mode_distribution']}")
        print(f"Successful constraint comparison operator distribution: {succ_stats['cmp_distribution']}")
        print(f"Successful constraint target column distribution: {succ_stats['target_col_distribution']}")
        print(f"Successful constraint average fit rate: {succ_stats['fit_rate_stats']['avg_fit_rate']:.4f}")
        print(f"Perfect fit constraint count: {succ_stats['fit_rate_stats']['perfect_fit_count']}")
        print(f"Successful constraint total time (JSON): {succ_stats['time_stats']['total_time']:.2f}s")
        print(f"Successful constraint average time (JSON): {succ_stats['time_stats']['avg_time_among_successful']:.2f}s")
        print(f"Successful constraint average assertion mining time: {succ_stats['time_stats']['avg_asrtm_time_among_successful']:.2f}s")
        print(f"Successful constraint average precondition mining time: {succ_stats['time_stats']['avg_predm_time_among_successful']:.2f}s")
    
    if "conversion_stats" in result:
        conv_stats = result["conversion_stats"]
        print("\n=== Conversion Statistics ===")
        print(f"Processed files: {conv_stats['total_processed']}")
        print(f"Successful conversions: {conv_stats['successful_conversions']}")
        print(f"Failed conversions: {conv_stats['failed_conversions']}")
        print(f"Success rate: {conv_stats['success_rate']:.2%}")
    
    print("\nProcessing complete!")
    
    
if __name__ == "__main__":
    main()
