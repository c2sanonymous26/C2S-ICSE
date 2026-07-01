from pathlib import Path
from lark import Tree, Token
from agno.agent import Agent
from pint import Quantity

from ...utils import log_debug
from .. import LOGGER_NAME
from .UnitManager import UnitManager
from .errors import ImplSemanticError

class UnitAnalyzer:
    """
    Analyze unit compatibility in expressions using the pint library for unit checking.
    """
    
    def __init__(self, input_dir: Path, custom_prompt_template: str | None = None):
        self.manager = UnitManager(input_dir, custom_prompt_template=custom_prompt_template)
        self.bfunc_id = None
        
    def analyze(self, agno_agent: Agent, bfunc_id: str, tree: Tree, semantics: str, implementation: str) -> tuple[bool, str | None]:
        """
        Analyze unit compatibility in expressions
        
        Args:
            agno_agent: Agent for querying unit information
            bfunc_id: Function ID
            tree: Parse tree
            semantics: Function semantics
            implementation: Function implementation
            
        Returns:
            (True, None): Analysis passed, no errors
            (False, error_message): Analysis failed, return error message
        """
        log_debug(LOGGER_NAME, f"unit analyzer starts for {bfunc_id}", center=True, symbol="~")
        
        self.bfunc_id = bfunc_id
        
        # Initial query for constant and symbol units
        query_success = self.manager.query_constant_and_symbol_units(agno_agent, tree, semantics, implementation)
        if not query_success:
            return True, None  # If query fails, conservatively return success
        
        log_debug(LOGGER_NAME, f"constants units map: {self.manager.constant_units_map}")
        log_debug(LOGGER_NAME, f"symbols units: {self.manager.symbol_units}")

        # Analyze all num_cmp_expr nodes in the tree
        errors = []
        for node in tree.iter_subtrees():
            if node.data in ['prod_num_cmp_expr_1', 'prod_num_cmp_expr_2']:
                success, result = self._analyze_num_cmp_expr(node)
                if not success and isinstance(result, str):
                    errors.append(result)
                                
        log_debug(LOGGER_NAME, f"unit analyzer done for {bfunc_id}", center=True, symbol="~")
        if errors:
            return False, "\n".join(errors)
        else:
            return True, None
    
    def _check_angle_unit_mismatch(self, left_result: Quantity, right_result: Quantity) -> bool:
        """
        Check if there's a mismatch between angle units
        
        Two angle units match only if:
        - Same base unit (degree or radian or steradian)
        - Same power/exponent
        
        Examples:
        - radian vs degree → mismatch (different base)
        - radian**2 vs degree**2 → mismatch (different base)
        - radian vs radian**2 → mismatch (different power)
        - steradian vs degree**2 → mismatch (steradian ≠ radian**2 in pint)
        
        Args:
            left_result: Left operand quantity
            right_result: Right operand quantity
            
        Returns:
            True if incompatible angle units are mixed, False otherwise
        """
        def _get_angle_signature(quantity: Quantity) -> tuple[str, int] | None:
            """
            Get the angle unit signature (base_unit, power)
            
            Normalizes angle units to base unit + power:
            - steradian → ('radian', 2) since steradian = radian²
            - square_degree → ('degree', 2) since square_degree = degree²
            - radian**n → ('radian', n)
            - degree**n → ('degree', n)
            
            Returns:
                ('degree', power): for degree-based units
                ('radian', power): for radian-based units
                None: not an angle unit
            """
            try:
                # Access pint's internal units container
                unit_dict = getattr(quantity.units, '_units', None)
                if unit_dict is None:
                    unit_dict = getattr(quantity.units, '_inner', None)
                
                if unit_dict is None:
                    return None
                
                # Only check pure angle units (no compound units like deg/m)
                if len(unit_dict) != 1:
                    return None
                
                # Normalize angle units to base unit + power
                
                # steradian is radian²
                if 'steradian' in unit_dict:
                    power = unit_dict['steradian']
                    # steradian with power n means radian^(2n)
                    return ('radian', 2 * power)
                
                # square_degree is degree²
                if 'square_degree' in unit_dict:
                    power = unit_dict['square_degree']
                    # square_degree with power n means degree^(2n)
                    return ('degree', 2 * power)
                
                # degree with any power
                if 'degree' in unit_dict:
                    return ('degree', unit_dict['degree'])
                
                # radian with any power
                if 'radian' in unit_dict:
                    return ('radian', unit_dict['radian'])
                
                return None
                
            except Exception:
                return None
        
        # Get angle signatures for both quantities
        left_sig = _get_angle_signature(left_result)
        right_sig = _get_angle_signature(right_result)
        
        # If either is not a pure angle unit, no mismatch
        if left_sig is None or right_sig is None:
            return False
        
        # Mismatch if signatures are different
        # (different base unit OR different power)
        return left_sig != right_sig
        
    def _analyze_expr(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze expression node and return result
        
        Return values:
            - (True, quantity): Successfully analyzed unit
            - (True, None): Unable to analyze, but not an error
            - (False, error_message): Analysis error, return error message
        """
        if node.data == 'prod_num_term_single':
            return self._analyze_expr(node.children[0])
        elif node.data == 'prod_num_add':
            return self._analyze_num_add(node)
        elif node.data == 'prod_num_sub':
            return self._analyze_num_sub(node)
        elif node.data == 'prod_num_factor_single':
            return self._analyze_expr(node.children[0])
        elif node.data == 'prod_num_mul':
            return self._analyze_num_mul(node)
        elif node.data == 'prod_num_div':
            return self._analyze_num_div(node)
        elif node.data == 'prod_num_mod':
            return self._analyze_num_mod(node)
        elif node.data == 'prod_num_factor_neg':
            return self._analyze_expr(node.children[0])
        elif node.data == 'prod_num_factor_paren':
            return self._analyze_expr(node.children[0])
        elif node.data == 'prod_num_factor_math_func':
            return self._analyze_math_func(node.children[0])
        elif node.data == 'prod_num_factor_field':
            # handle prod_num_field inside
            return self._analyze_field(node)
        elif node.data == 'prod_num_factor_literal':
            return self._analyze_constant(node.children[0])

        elif node.data == 'prod_num_target_add':
            return self._analyze_num_target_add(node)
        elif node.data == 'prod_num_target_sub':
            return self._analyze_num_target_sub(node)
        elif node.data == 'prod_num_target_term':
            return self._analyze_expr(node.children[0])
        elif node.data == 'prod_num_target_mul':
            return self._analyze_num_target_mul(node)
        elif node.data == 'prod_num_target_div':
            return self._analyze_num_target_div(node)
        elif node.data == 'prod_num_target_mod':
            return self._analyze_num_target_mod(node)
        elif node.data == 'prod_num_target_factor':
            return self._analyze_expr(node.children[0])
        elif node.data == 'prod_num_target_threshold':
            return self._analyze_symbol(node)
        elif node.data == 'prod_num_target_num_expr':
            return self._analyze_expr(node.children[0])
        elif node.data == 'prod_num_target_paren':
            return self._analyze_expr(node.children[0])
        elif node.data == 'prod_num_target_neg':
            return self._analyze_expr(node.children[0])
        
        return True, None
    
    # num_cmp_expr: num_expr NUM_CMP_OP num_target_expr -> prod_num_cmp_expr_2
    # num_cmp_expr: num_target_expr NUM_CMP_OP num_expr -> prod_num_cmp_expr_1
    def _analyze_num_cmp_expr(self, node: Tree) -> tuple[bool, str | None]:
        """
        Analyze numerical comparison expressions
        
        Return values:
            - (True, None): Comparison expression is correct, or cannot be determined
            - (False, error_message): Comparison expression has errors
        """
        left_expr = node.children[0]
        cmp_op = node.children[1]
        right_expr = node.children[2]
        
        # Analyze left and right operands
        success_left, left_result = self._analyze_expr(left_expr)
        if not success_left:
            return False, left_result
        
        success_right, right_result = self._analyze_expr(right_expr)
        if not success_right:
            return False, right_result
        
        # If units cannot be analyzed, handle conservatively
        if left_result is None or right_result is None:
            return True, None
        
        # Check unit compatibility
        try:
            # is_compatible_with requires dimensionality is the same (as left and right are both Quantity)
            if not left_result.is_compatible_with(right_result):
                # 1. Both have dimensions --> Error
                # 2. One has dimensions, other is dimensionless but has units --> Error
                if (left_result.dimensionality and right_result.dimensionality) \
                    or (not left_result.dimensionality and left_result.units != '') \
                    or (not right_result.dimensionality and right_result.units != ''):
                        
                    error = ImplSemanticError(
                        f"Unit compatibility error in comparison: " \
                        f"({left_result.dimensionality}, {left_result.units}) and " \
                        f"({right_result.dimensionality}, {right_result.units}) are not compatible",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        f"{left_expr.pretty()} {cmp_op.value} {right_expr.pretty()}"
                    )
                    return False, str(error)
            
            # Ad-hoc check: detect degree and radian mismatch
            if self._check_angle_unit_mismatch(left_result, right_result):
                error = ImplSemanticError(
                    f"Angle unit mismatch in comparison: " \
                    f"mixing degree and radian ({left_result.units} vs {right_result.units}). " \
                    f"Consider explicit unit conversion.",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    f"{left_expr.pretty()} {cmp_op.value} {right_expr.pretty()}"
                )
                return False, str(error)
                    
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Unit check error: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                f"{left_expr.pretty()} {cmp_op.value} {right_expr.pretty()}"
            )
            return False, str(error)
        
        return True, None
    
    # num_expr: num_term "+" num_expr -> prod_num_add
    def _analyze_num_add(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze addition expressions
        
        Detection rules:
            - If two quantities are compatible (strictly same dimensions), then detection passes.
                - Special ad-hoc check: reject degree + radian mixing
                - Dimensionless quantities in SI can all be converted to each other.
            - If two quantities are not compatible
                - If any quantity is dimensionless and unitless, then detection passes.
                - If any quantity is dimensionless but has units, then detection fails.
                - If both quantities have dimensions, then detection fails.
                
        Return values:
            - (True, quantity): Successfully analyzed unit
            - (True, None): Unable to analyze, but not an error
            - (False, error_message): Analysis error, return error message
        """
        # Get left operand
        success, left_result = self._analyze_expr(node.children[0])
        if not success:
            return success, left_result
        if left_result is None:
            return True, None
            
        # Get right operand
        success, right_result = self._analyze_expr(node.children[1])
        if not success:
            return success, right_result
        if right_result is None:
            return True, None
        
        try:
            # Check compatibility
            if not left_result.is_compatible_with(right_result):
                if (left_result.dimensionality and right_result.dimensionality) \
                    or (not left_result.dimensionality and left_result.units != '') \
                    or (not right_result.dimensionality and right_result.units != ''):
                        
                    error = ImplSemanticError(
                        f"Addition unit compatibility error: " \
                        f"({left_result.dimensionality}, {left_result.units}) and " \
                        f"({right_result.dimensionality}, {right_result.units}) are not compatible",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
            
            # Ad-hoc check: detect degree and radian mismatch
            if self._check_angle_unit_mismatch(left_result, right_result):
                error = ImplSemanticError(
                    f"Angle unit mismatch in addition: " \
                    f"mixing degree and radian ({left_result.units} vs {right_result.units}). " \
                    f"Consider explicit unit conversion.",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    node.pretty()
                )
                return False, str(error)
                
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Unit check error in addition: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)

        return True, left_result
    
    # num_expr: num_term "-" num_expr -> prod_num_sub
    def _analyze_num_sub(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze subtraction expressions
        
        Detection rules are same as addition with ad-hoc degree/radian check
        """
        # Get left operand
        success, left_result = self._analyze_expr(node.children[0])
        if not success:
            return success, left_result
        if left_result is None:
            return True, None
            
        # Get right operand
        success, right_result = self._analyze_expr(node.children[1])
        if not success:
            return success, right_result
        if right_result is None:
            return True, None
            
        try:
            # Check compatibility
            if not left_result.is_compatible_with(right_result):
                if (left_result.dimensionality and right_result.dimensionality) \
                    or (not left_result.dimensionality and left_result.units != '') \
                    or (not right_result.dimensionality and right_result.units != ''):
                        
                    error = ImplSemanticError(
                        f"Subtraction unit compatibility error: " \
                        f"({left_result.dimensionality}, {left_result.units}) and " \
                        f"({right_result.dimensionality}, {right_result.units}) are not compatible",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
            
            # Ad-hoc check: detect degree and radian mismatch
            if self._check_angle_unit_mismatch(left_result, right_result):
                error = ImplSemanticError(
                    f"Angle unit mismatch in subtraction: " \
                    f"mixing degree and radian ({left_result.units} vs {right_result.units}). " \
                    f"Consider explicit unit conversion.",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    node.pretty()
                )
                return False, str(error)
                
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Unit check error in subtraction: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
            
        return True, left_result
    
    # num_term: num_factor "\u00d7" num_term -> prod_num_mul
    def _analyze_num_mul(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze multiplication expressions
        
        Detection rules: Units of two quantities are multiplied, no need to consider compatibility
        """
        # Get left operand
        success, left_result = self._analyze_expr(node.children[0])
        if not success:
            return success, left_result
        if left_result is None:
            return True, None
                    
        success, right_result = self._analyze_expr(node.children[1])
        if not success:
            return success, right_result
        if right_result is None:
            return True, None
            
        try:
            # Multiplication: units multiply
            result = left_result * right_result
            
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Unit calculation error in multiplication: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
        
        return True, result
    
    # num_term: num_factor "\u00f7" num_term -> prod_num_div
    def _analyze_num_div(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze division expressions
        
        Detection rules: Units of two quantities are divided, no need to consider compatibility
        """
        # Get left operand
        success, left_result = self._analyze_expr(node.children[0])
        if not success:
            return success, left_result
        if left_result is None:
            return True, None
            
        success, right_result = self._analyze_expr(node.children[1])
        if not success:
            return success, right_result
        if right_result is None:
            return True, None
            
        try:
            # Division: units divide
            result = left_result / right_result
            
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Unit calculation error in division: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
        
        return True, result
    
    # num_term: num_factor "%" num_term -> prod_num_mod
    def _analyze_num_mod(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze modulo expressions
        
        Detection rules: Right operand must be dimensionless
            - If right operand has dimensions, report error
            - If right operand is dimensionless but has units (e.g., angle units), also report error
        """
        # Get left operand
        success, left_result = self._analyze_expr(node.children[0])
        if not success:
            return success, left_result
        if left_result is None:
            return True, None
            
        success, right_result = self._analyze_expr(node.children[1])
        if not success:
            return success, right_result
        if right_result is None:
            return True, None
                
        try:
            # Modulo operation: right operand must be dimensionless and unitless
            if right_result.dimensionality or right_result.units != '':
                error = ImplSemanticError(
                    f"Modulo operation error: Right operand must be dimensionless without unit, " \
                    f"but got ({right_result.dimensionality}, {right_result.units})",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    node.pretty()
                )
                return False, str(error)
                
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Unit check error in modulo operation: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
        
        # Modulo operation result keeps the unit of left operand
        return True, left_result
    
    # num_factor: math_func_expr -> prod_num_factor_math_func
    # math_func_expr: "abs" "(" num_expr ")" | "sin" "(" num_expr ")" | ... 
    def _analyze_math_func(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze mathematical functions
        """
        # Get function name
        func_type = node.data
        func_name = func_type[len('prod_math_func_'):]
    
        # Get parameters
        params = []
        if func_name == 'pow':
            success, result = self._analyze_expr(node.children[0])
            if not success:
                return success, result
            if result is None:
                return True, None
            params.append(result)
            
            success, result = self._analyze_constant(node.children[1])
            if not success:
                return success, result
            if result is None:
                return True, None
            params.append(result)
        else:
            for child in node.children:
                success, result = self._analyze_expr(child)
                if not success:
                    return success, result
                if result is None:
                    return True, None
                params.append(result)
                
        def analyze_trig_func(func_name: str, params: list[Quantity]) -> tuple[bool, str | None | Quantity]:

            if func_name in ['sin', 'cos', 'tan']:
                # Require parameter in radian units
                if params[0].units != self.manager.ureg.radian:
                    error = ImplSemanticError(
                        f"Function {func_name} strictly requires radian unit, "\
                        f"but got ({params[0].dimensionality}, {params[0].units})",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
                # Return unitless
                return True, self.manager.Q_(1.0, '')
                
            elif func_name in ['asin', 'acos', 'atan']:
                # Require parameter dimensionless and unitless
                if params[0].units != self.manager.ureg.dimensionless:
                    error = ImplSemanticError(
                        f"Function {func_name} requires dimensionless parameter without unit, "\
                        f"but got ({params[0].dimensionality}, {params[0].units})",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
                # Return radian units
                return True, self.manager.Q_(1.0, 'radian')
                
            # Special handling for atan2
            elif func_name == 'atan2':
                
                # Two parameters must have compatible units
                if not params[0].is_compatible_with(params[1]):
                    error = ImplSemanticError(
                        f"Function {func_name} requires compatible units for parameters: " \
                        f"({params[0].dimensionality}, {params[0].units}) vs " \
                        f"({params[1].dimensionality}, {params[1].units})",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
                
                # Ad-hoc check: detect angle unit mismatch
                if self._check_angle_unit_mismatch(params[0], params[1]):
                    error = ImplSemanticError(
                        f"Angle unit mismatch in {func_name}: " \
                        f"mixing degree and radian ({params[0].units} vs {params[1].units}). " \
                        f"Consider explicit unit conversion.",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
                
                # Return radian units
                return True, self.manager.Q_(1.0, 'radian')

        def analyze_angle_conversion_func(func_name: str, params: list[Quantity]) -> tuple[bool, str | None | Quantity]:
            
            if func_name == 'degrees':
                # Check if parameter is in radians
                if params[0].units != self.manager.ureg.radian:
                    error = ImplSemanticError(
                        f"Function {func_name} requires radian unit input, "\
                        f"but got ({params[0].dimensionality}, {params[0].units})",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
                # Return degree units
                return True, self.manager.Q_(1.0, 'degree')
            
            elif func_name == 'radians':
                # Check if parameter is in degrees
                if params[0].units != self.manager.ureg.degree:
                    error = ImplSemanticError(
                        f"Function {func_name} requires degree unit input, "\
                        f"but got ({params[0].dimensionality}, {params[0].units})",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
                # Return radian units
                return True, self.manager.Q_(1.0, 'radian')

        def analyze_power_func(func_name: str, params: list[Quantity]) -> tuple[bool, str | None | Quantity]:
        
            if func_name == 'pow':

                # Exponent must be dimensionless and unitless
                if params[1].dimensionality or params[1].units != '':
                    error = ImplSemanticError(
                        f"Function {func_name} requires dimensionless and unitless exponent, "\
                        f"but got ({params[1].dimensionality}, {params[1].units})",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
                
                # Use pint's ** operator to calculate units
                exponent = float(params[1].magnitude)
                return True, params[0] ** exponent
            
            elif func_name == 'sqrt':
                # Square root
                return True, params[0] ** 0.5
            
            elif func_name == 'cbrt':
                # Cube root
                return True, params[0] ** (1/3)

        def analyze_exp_log_func(func_name: str, params: list[Quantity]) -> tuple[bool, str | None | Quantity]:
        
            # Require parameter to be dimensionless and unitless
            if params[0].dimensionality or params[0].units != '':
                error = ImplSemanticError(
                    f"Function {func_name} requires dimensionless and unitless parameter, but got {params[0].units}",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    node.pretty()
                )
                return False, str(error)
            # Return dimensionless
            return True, self.manager.Q_(1.0, '')

        def analyze_minmax_func(func_name: str, params: list[Quantity]) -> tuple[bool, str | None | Quantity]:
            
            # Compatibility check, use same logic as addition and subtraction
            if not params[0].is_compatible_with(params[1]):
                if (params[0].dimensionality and params[1].dimensionality) \
                    or (not params[0].dimensionality and params[0].units != '') \
                    or (not params[1].dimensionality and params[1].units != ''):
                        
                    error = ImplSemanticError(
                        f"Function {func_name} requires compatible units for parameters: " \
                        f"({params[0].dimensionality}, {params[0].units}) vs " \
                        f"({params[1].dimensionality}, {params[1].units})",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
            
            # Ad-hoc check: detect angle unit mismatch
            if self._check_angle_unit_mismatch(params[0], params[1]):
                error = ImplSemanticError(
                    f"Angle unit mismatch in {func_name}: " \
                    f"mixing degree and radian ({params[0].units} vs {params[1].units}). " \
                    f"Consider explicit unit conversion.",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    node.pretty()
                )
                return False, str(error)
            
            # Return the unit of the side that has units
            if params[0].dimensionality:
                return True, params[0]
            else:
                return True, params[1]

        def analyze_abs_func(params: list[Quantity]) -> tuple[bool, str | None | Quantity]:
            return True, params[0]
        
        
        try:
            # Process by function type classification
            if func_name in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2']:
                return analyze_trig_func(func_name, params)
            elif func_name in ['degrees', 'radians']:
                return analyze_angle_conversion_func(func_name, params)
            elif func_name in ['pow', 'sqrt', 'cbrt']:
                return analyze_power_func(func_name, params)
            elif func_name in ['exp', 'log', 'log10', 'log1p']:
                return analyze_exp_log_func(func_name, params)
            elif func_name in ['min', 'max']:
                return analyze_minmax_func(func_name, params)
            elif func_name == 'abs':
                return analyze_abs_func(params)

        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Math function unit calculation error: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
    
    # num_factor: num_field -> prod_num_factor_field
    # num_target_expr: num_field -> prod_num_target_field
    def _analyze_field(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze fields
        """
        # Get prod_num_field node
        node = node.children[0]
                    
        # CUSTOM_NUM_FIELD_NAME
        field_name = node.children[1].value  
        
        # Use UnitManager to get field units
        quantity = self.manager.get_field_unit(field_name)
        if quantity:
            return True, quantity
        
        # If field unit information cannot be found, handle conservatively as None
        return True, None
    
    # SIGNED_NUMBER (prod_num_factor_literal, prod_math_func_pow)
    def _analyze_constant(self, const_token: Token) -> tuple[bool, str | None | Quantity]:
        """
        Analyze constants
        
        Args:
            const_token: SIGNED_NUMBER token (Lark Token type, not Tree)
        """
        # Parse value from token
        value = float(const_token.value) if '.' in const_token.value else int(const_token.value)
        
        # Use const_token.start_pos to uniquely identify this constant
        start_pos = const_token.start_pos
        
        # Use UnitManager to get constant units by start_pos
        quantity = self.manager.get_constant_unit(start_pos, value)
        if quantity:
            return True, quantity
        
        # If constant unit information cannot be found, return None
        return True, None
    
    # num_target_factor: NUM_SYMBOL NATURAL -> prod_num_target_threshold
    def _analyze_symbol(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze symbols (e.g., NTHRESHOLD1)
        """
        symbol_name = f"{node.children[0].value}{node.children[1].value}"
        
        # Use UnitManager to get symbol units
        quantity = self.manager.get_symbol_unit(symbol_name)
        if quantity:
            return True, quantity
        
        # If symbol unit information cannot be found, handle conservatively as None
        return True, None
    
    # num_target_expr: num_target_term "+" num_target_expr -> prod_num_target_add
    def _analyze_num_target_add(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze addition operations in target expressions
        
        Detection rules with ad-hoc degree/radian check:
            - Check dimensional compatibility
            - Special check: reject degree + radian mixing
        """
        # Analyze left and right operands
        success_left, left_result = self._analyze_expr(node.children[0])
        if not success_left:
            return False, left_result
        
        success_right, right_result = self._analyze_expr(node.children[1])
        if not success_right:
            return False, right_result
        
        # If units cannot be analyzed, handle conservatively
        if left_result is None or right_result is None:
            return True, None
            
        left_quantity = left_result
        right_quantity = right_result
        
        try:
            # Check dimensional compatibility
            if not left_quantity.is_compatible_with(right_quantity):
                if (left_quantity.dimensionality and right_quantity.dimensionality) \
                    or (not left_quantity.dimensionality and left_quantity.units != '') \
                    or (not right_quantity.dimensionality and right_quantity.units != ''):
                        
                    error = ImplSemanticError(
                        f"Addition unit compatibility error in target expression: " \
                        f"({left_result.dimensionality}, {left_result.units}) and " \
                        f"({right_result.dimensionality}, {right_result.units}) are not compatible",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
            
            # Ad-hoc check: detect degree and radian mismatch
            if self._check_angle_unit_mismatch(left_quantity, right_quantity):
                error = ImplSemanticError(
                    f"Angle unit mismatch in target expression addition: " \
                    f"mixing degree and radian ({left_result.units} vs {right_result.units}). " \
                    f"Consider explicit unit conversion.",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    node.pretty()
                )
                return False, str(error)
            
            # Addition result uses the unit of the side with dimensions
            if left_quantity.dimensionality:
                return True, left_quantity
            else:
                return True, right_quantity
                
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Target addition unit calculation error: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
    
    # num_target_expr: num_target_term "-" num_target_expr -> prod_num_target_sub
    def _analyze_num_target_sub(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze subtraction operations in target expressions
        
        Detection rules with ad-hoc degree/radian check:
            - Check dimensional compatibility
            - Special check: reject degree - radian mixing
        """
        # Analyze left and right operands
        success_left, left_result = self._analyze_expr(node.children[0])
        if not success_left:
            return False, left_result
        
        success_right, right_result = self._analyze_expr(node.children[1])
        if not success_right:
            return False, right_result
        
        # If units cannot be analyzed, handle conservatively
        if left_result is None or right_result is None:
            return True, None
            
        left_quantity = left_result
        right_quantity = right_result
        
        try:
            # Check dimensional compatibility
            if not left_quantity.is_compatible_with(right_quantity):
                if (left_quantity.dimensionality and right_quantity.dimensionality) \
                    or (not left_quantity.dimensionality and left_quantity.units != '') \
                    or (not right_quantity.dimensionality and right_quantity.units != ''):
                        
                    error = ImplSemanticError(
                        f"Subtraction unit compatibility error in target expression: " \
                        f"({left_quantity.dimensionality}, {left_quantity.units}) and " \
                        f"({right_quantity.dimensionality}, {right_quantity.units}) are not compatible",
                        self.bfunc_id,
                        node.meta.line,
                        node.meta.column,
                        node.pretty()
                    )
                    return False, str(error)
            
            # Ad-hoc check: detect degree and radian mismatch
            if self._check_angle_unit_mismatch(left_quantity, right_quantity):
                error = ImplSemanticError(
                    f"Angle unit mismatch in target expression subtraction: " \
                    f"mixing degree and radian ({left_result.units} vs {right_result.units}). " \
                    f"Consider explicit unit conversion.",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    node.pretty()
                )
                return False, str(error)
            
            # Subtraction result uses the unit of the side with dimensions
            if left_quantity.dimensionality:
                return True, left_quantity
            else:
                return True, right_quantity
                
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Target subtraction unit calculation error: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
    
    # num_target_term: num_target_factor "\u00d7" num_target_term -> prod_num_target_mul
    def _analyze_num_target_mul(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze multiplication operations in target expressions
        
        Detection rules: Units multiply directly, no need to consider compatibility
        """
        # Analyze left and right operands
        success_left, left_result = self._analyze_expr(node.children[0])
        if not success_left:
            return False, left_result
        
        success_right, right_result = self._analyze_expr(node.children[1])
        if not success_right:
            return False, right_result
        
        # If units cannot be analyzed, handle conservatively
        if left_result is None or right_result is None:
            return True, None
            
        left_quantity = left_result
        right_quantity = right_result
        
        try:
            # Multiplication: units multiply
            return True, left_quantity * right_quantity
                
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Target multiplication unit calculation error: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
    
    # num_target_term: num_target_factor "\u00f7" num_target_term -> prod_num_target_div
    def _analyze_num_target_div(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze division operations in target expressions
        
        Detection rules: Units divide directly, no need to consider compatibility
        """
        # Analyze left and right operands
        success_left, left_result = self._analyze_expr(node.children[0])
        if not success_left:
            return False, left_result
        
        success_right, right_result = self._analyze_expr(node.children[1])
        if not success_right:
            return False, right_result
        
        # If units cannot be analyzed, handle conservatively
        if left_result is None or right_result is None:
            return True, None
            
        left_quantity = left_result
        right_quantity = right_result
        
        try:
            # Division: units divide
            return True, left_quantity / right_quantity
                
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Target division unit calculation error: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
    
    # num_target_term: num_target_factor "%" num_target_term -> prod_num_target_mod
    def _analyze_num_target_mod(self, node: Tree) -> tuple[bool, str | None | Quantity]:
        """
        Analyze modulo operations in target expressions
        
        Detection rules: Right operand must be dimensionless and unitless
        """
        # Analyze left and right operands
        success_left, left_result = self._analyze_expr(node.children[0])
        if not success_left:
            return False, left_result
        
        success_right, right_result = self._analyze_expr(node.children[1])
        if not success_right:
            return False, right_result
        
        # If units cannot be analyzed, handle conservatively
        if left_result is None or right_result is None:
            return True, None
            
        left_quantity = left_result
        right_quantity = right_result
        
        try:
            # Modulo operation: right operand must be dimensionless and unitless
            if right_quantity.dimensionality or right_quantity.units != '':
                error = ImplSemanticError(
                    f"Modulo operation error in target expression: Right operand must be dimensionless without unit, " \
                    f"but got ({right_quantity.dimensionality}, {right_quantity.units})",
                    self.bfunc_id,
                    node.meta.line,
                    node.meta.column,
                    node.pretty()
                )
                return False, str(error)
            
            # Result keeps the unit of left operand
            return True, left_quantity
                
        except Exception as e:
            # Handle other possible errors
            error = ImplSemanticError(
                f"Target modulo unit calculation error: {str(e)}",
                self.bfunc_id,
                node.meta.line,
                node.meta.column,
                node.pretty()
            )
            return False, str(error)
