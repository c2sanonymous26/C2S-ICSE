import tomli
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict
from pathlib import Path
from agno.agent import Agent
from pint import UnitRegistry, Quantity
from lark import Tree
from jinja2 import Environment

from ...utils import log_warning
from .. import LOGGER_NAME
from .prompts import PHASE3_QUERY_UNIT_PROMPT_TEMPLATE

Unit = dict[str, Fraction]

@dataclass
class FieldUnit:
    """Unit information for fields"""
    unit: Unit
    
    @classmethod
    def from_dict(cls, info: dict[str, Any]) -> 'FieldUnit':
        unit = {k: Fraction(v) for k, v in info['unit'].items()}
        return cls(unit=unit)


class UnitPower(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    power: str


LLMUnit = list[UnitPower]


class ConstantUnit(BaseModel):
    """Unit information for constants"""
    model_config = ConfigDict(extra="forbid")

    value: float | int
    unit: LLMUnit
    

class SymbolUnit(BaseModel):
    """Unit information for symbols"""
    model_config = ConfigDict(extra="forbid")

    name: str
    unit: LLMUnit
    

class Units(BaseModel):
    model_config = ConfigDict(extra="forbid")

    constants: list[ConstantUnit]
    symbols: list[SymbolUnit]
    
class UnitManager:
    
    def __init__(self, input_dir: Path, custom_prompt_template: str | None = None):
        self.field_units = self._load_field_units(input_dir)
        self.constant_units_map = {}  # Map from start_pos to ConstantUnit
        self.symbol_units = []
        
        # Initialize pint unit system
        self.ureg = UnitRegistry()
        
        # Define custom dimensions for id-like fields
        # These are dimensionless but have distinct "units" to prevent mixing
        self.ureg.define('record_id = [record_id]')  # For 'id' field
        self.ureg.define('group_id = [group_id]')    # For 'grpid' field
        
        self.Q_ = self.ureg.Quantity
        
        # Store custom prompt template for validation scenarios
        self.custom_prompt_template = custom_prompt_template
    
    def _load_field_units(self, input_dir: Path) -> dict[str, FieldUnit]:
        field_units = {}
        
        dataset_path = input_dir / 'context_schema.toml'
        with open(dataset_path, 'rb') as f:
            fields = tomli.load(f)['context_definitions']['fields']
            for field_name, field_info in fields.items():
                if field_info['type'] in ['int', 'float']:
                    field_units[field_name] = FieldUnit.from_dict(field_info)
        return field_units

    def query_constant_and_symbol_units(self, agno_agent: Agent, tree: Tree, semantics: str, implementation: str) -> bool:
        # Clear old constant and symbol information
        self._reset()
        
        # Collect constants and symbols from tree
        const_nodes, symbols = self._collect_constants_and_symbols(tree)
        
        if len(const_nodes) == 0 and len(symbols) == 0:
            return True
        
        # Extract values for prompt (keep order)
        const_values = [value for _, value in const_nodes]
        
        # Render user prompt
        user_prompt = self._render_query_unit_prompt(const_values, symbols, semantics, implementation)
        
        try_times = 0
        while try_times < 5:
            # Update and call agent
            agno_agent.response_model = Units
            response = agno_agent.run(user_prompt, stream=False)
            units = response.content
            if not isinstance(units, Units):
                try_times += 1
                user_prompt = "Your output is not an expected json object, please fix it."
                continue
            
            # Check if the order of constants is consistent
            index = -1
            for i, (const_unit, const_value) in enumerate(zip(units.constants, const_values)):
                if const_unit.value != const_value:
                    index = i
                    break
            
            if index != -1:
                try_times += 1
                user_prompt = f'The {index}-th constant in your output is not consistent with the input, please fix it.'
                continue
            # Check if the number of symbols is consistent
            if len(units.symbols) != len(symbols):
                try_times += 1
                user_prompt = "The number of symbols in your output is not consistent with the input, please fix it."
                continue
            
            # Check if all returned symbol names are in the expected symbols list
            returned_symbol_names = {symbol.name for symbol in units.symbols}
            expected_symbol_names = set(symbols)
            if returned_symbol_names != expected_symbol_names:
                unexpected_symbols = returned_symbol_names - expected_symbol_names
                missing_symbols = expected_symbol_names - returned_symbol_names
                error_msg = "Symbol names in your output are not consistent with the input."
                if unexpected_symbols:
                    error_msg += f" Unexpected symbols: {unexpected_symbols}."
                if missing_symbols:
                    error_msg += f" Missing symbols: {missing_symbols}."
                error_msg += " Please fix it."
                try_times += 1
                user_prompt = error_msg
                continue

            invalid_unit_error = self._validate_unit_powers(units)
            if invalid_unit_error is not None:
                try_times += 1
                user_prompt = invalid_unit_error
                continue
            
            break
        
        # Check if units is still not a valid Units object after all retries
        if not isinstance(units, Units):
            log_warning(LOGGER_NAME, f"Failed to get valid units after {try_times} attempts")
            return False
        
        # Build constant_units_map using start_pos as key
        for (start_pos, _), const_unit in zip(const_nodes, units.constants):
            self.constant_units_map[start_pos] = const_unit
            
        self.symbol_units = units.symbols
                
        return True
    
    def _validate_unit_powers(self, units: Units) -> str | None:
        for const_unit in units.constants:
            for unit_power in const_unit.unit:
                try:
                    Fraction(unit_power.power)
                except (ValueError, ZeroDivisionError):
                    return (
                        f"The unit power '{unit_power.power}' for unit '{unit_power.name}' is not a valid integer "
                        "or fraction string. Please fix it."
                    )
        for symbol_unit in units.symbols:
            for unit_power in symbol_unit.unit:
                try:
                    Fraction(unit_power.power)
                except (ValueError, ZeroDivisionError):
                    return (
                        f"The unit power '{unit_power.power}' for unit '{unit_power.name}' in symbol "
                        f"'{symbol_unit.name}' is not a valid integer or fraction string. Please fix it."
                    )
        return None

    def _reset(self) -> None:
        self.constant_units_map.clear()
        self.symbol_units.clear()
        
    def _collect_constants_and_symbols(self, tree: Tree) -> tuple[list[tuple[int, float | int]], list[str]]:
        """
        Collect constants and symbols from left to right

        Use const_token.start_pos to ensure left-to-right order
        
        Returns:
            - const_nodes: List of (start_pos, value) tuples for constants
            - symbols: List of symbol names (deduplicated, in left-to-right order)
        """
        const_nodes = []
        symbol_nodes = []
        
        for node in tree.iter_subtrees():
            if node.data == 'prod_num_factor_literal':
                assert len(node.children) == 1
                const_token = node.children[0]
                value = int(const_token.value) if '.' not in const_token.value else float(const_token.value)
                # Save (position, value) tuple - use token's start_pos directly
                const_nodes.append((const_token.start_pos, value))
                
            elif node.data == 'prod_num_target_threshold':
                assert len(node.children) == 2
                symbol_name = f"{node.children[0].value}{node.children[1].value}"
                # Save (position, symbol name) tuple, use position for deduplication
                symbol_nodes.append((node.meta.start_pos, symbol_name))

        # Sort by position
        const_nodes.sort(key=lambda x: x[0])
        
        # Symbols are also sorted by position, and deduplicated (keep first occurrence)
        symbol_nodes.sort(key=lambda x: x[0])
        symbols = []
        symbols_seen = set()
        for _, symbol_name in symbol_nodes:
            if symbol_name not in symbols_seen:
                symbols.append(symbol_name)
                symbols_seen.add(symbol_name)
        
        return const_nodes, symbols
    
    def _render_query_unit_prompt(self, consts: list[float | int], symbols: list[str], semantics: str, implementation: str) -> str:
        env = Environment(trim_blocks=True, lstrip_blocks=True)
        
        # Use custom prompt if provided, otherwise use default
        template_str = self.custom_prompt_template if self.custom_prompt_template else PHASE3_QUERY_UNIT_PROMPT_TEMPLATE
        user_prompt_template = env.from_string(template_str)
        
        # Prepare template variables
        template_vars = {
            'constants': consts,
            'symbols': symbols,
            'semantics': semantics,
            'implementation': implementation
        }
        
        # If using custom prompt, also provide field units information
        if self.custom_prompt_template:
            # Use the original unit dictionary format (like in PHASE1)
            field_units_info = []
            for field_name, field_unit in self.field_units.items():
                # Convert Fraction back to string for display
                unit_dict = {k: str(v) for k, v in field_unit.unit.items()}
                field_units_info.append({'field': field_name, 'unit': unit_dict})
            template_vars['field_units'] = field_units_info
        
        user_prompt = user_prompt_template.render(**template_vars)
        return user_prompt
    
    def get_field_unit(self, field_name: str) -> Optional[Quantity]:
        """
        Get unit information based on field name and convert to pint Quantity object
        
        Args:
            field_name: Field name (e.g., 'speed')
            
        Returns:
            If corresponding field information is found, return pint Quantity object, otherwise return None
        """
        if field_name in self.field_units:
            field_info = self.field_units[field_name]
            return self._convert_to_pint_quantity(field_info.unit)
        return None
    
    def get_constant_unit(self, start_pos: int, value: float | int) -> Optional[Quantity]:
        """
        Get unit information based on start_pos and convert to pint Quantity object
        
        Use start_pos to uniquely identify each constant, supporting multiple constants with same value but different units
        
        Args:
            start_pos: The start position of the constant in the source code (from node.meta.start_pos)
            value: Constant value (for defensive checking)
            
        Returns:
            If corresponding constant information is found, return pint Quantity object, otherwise return None
        """
        # Look up constant by start_pos
        if start_pos in self.constant_units_map:
            const = self.constant_units_map[start_pos]
            
            # Defensive check to ensure value matches
            if const.value != value:
                return None
            
            return self._convert_to_pint_quantity(const.unit, value)
        
        # If constant not found in map, return None
        return None
    
    def get_symbol_unit(self, name: str) -> Optional[Quantity]:
        """
        Get unit information based on symbol name and convert to pint Quantity object
        
        Args:
            name: Symbol name (e.g., 'NTHRESHOLD1')
            
        Returns:
            If corresponding symbol information is found, return pint Quantity object, otherwise return None
        """
        for symbol in self.symbol_units:
            if symbol.name == name:
                return self._convert_to_pint_quantity(symbol.unit)
        return None
    
    def _convert_to_pint_quantity(self, unit: Unit | LLMUnit, value: float | int = 1.0) -> Quantity:
        """
        Convert internal Unit dictionary format to pint Quantity object
        
        Hybrid approach:
        - Integer powers: handled programmatically (efficient)
        - Fractional powers: handled via string parsing (precise)
        
        Args:
            unit: Internal unit dict or LLM unit list, e.g., {'m': Fraction(1, 1)} or [{'name': 'm', 'power': '1'}]
            value: Magnitude value for the quantity
            
        Returns:
            Corresponding pint Quantity object
        """
        
        # If unit is empty, return dimensionless quantity with unit
        if not unit:
            return self.Q_(value, '')

        # Initialize accumulator with the value
        result_quantity = self.Q_(value)

        # Separate integer and fractional powers
        frac_power_units_str = []

        unit_items = unit.items() if isinstance(unit, dict) else (
            (unit_power.name, unit_power.power) for unit_power in unit
        )
        for unit_symbol, power_value in unit_items:
            power = Fraction(power_value)
            # Integer power: handle programmatically
            if power.denominator == 1:
                result_quantity *= self.ureg(unit_symbol) ** power.numerator
            # Fractional power: build string fragment
            else:
                frac_power_units_str.append(f"{unit_symbol}**({power.numerator}/{power.denominator})")

        # If fractional powers exist, parse string and multiply
        if frac_power_units_str:
            frac_part_quantity = self.ureg("*".join(frac_power_units_str))
            result_quantity *= frac_part_quantity
                
        return result_quantity
        
