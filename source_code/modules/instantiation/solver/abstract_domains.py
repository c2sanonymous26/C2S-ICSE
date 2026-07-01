from fractions import Fraction
from z3 import z3
import re
from pathlib import Path

from ...utils import STRING_SYMBOLIC_PREFIX
from . import SymbolInequalities, SymbolDomains
from .construct_restriction_constraints import construct_restriction_constraints_per_symbol


def abstract_symbol_domains(symbol_inequalities: SymbolInequalities, restrictions_path: Path | None,) -> SymbolDomains:
            
    def is_string_symbol(symbol: str) -> bool:
        """Check if the symbol is a string symbolic expression"""
        return bool(re.match(f'^{STRING_SYMBOLIC_PREFIX}\\d+$', symbol))
    
    def get_boundary_value(v: Fraction, is_upper: bool, symbol: str, constraint: z3.BoolRef | None) -> Fraction | None: 
        opt = z3.Optimize()
        k = z3.Int('k')
        var = z3.Real(symbol)
        opt.add(var == z3.ToReal(k) * 1e-6)
        if constraint is not None:
            opt.add(constraint)
        if is_upper:
            opt.add(var > v)
            opt.minimize(k)
        else:
            opt.add(var < v)
            opt.maximize(k)    
    
        frac_val = None
        if opt.check() == z3.sat:
            model = opt.model()
            z3_val = model[var]
            frac_val = Fraction(z3_val.numerator().as_long(), z3_val.denominator().as_long())
        
        return frac_val
        
    abstract_domains = {}
    restriction_dict = construct_restriction_constraints_per_symbol(restrictions_path)
    for (op, symbol), threshold_set in symbol_inequalities.items():
        assert len(threshold_set) != 0, 'threshold_set cannot be empty'
            
        if symbol in abstract_domains:
            domains = set(abstract_domains[symbol])
        else:
            domains = set()
            
        if is_string_symbol(symbol):
            if op not in ['==', '!=']:
                raise ValueError(f"Unsupported operator {op} for string symbolic expression")

            domains.update(threshold_set)   
            
            solver = z3.Solver()
            var = z3.String(symbol)
            solver.add(z3.And([var != t for t in threshold_set]))
            if symbol in restriction_dict:
                solver.add(restriction_dict[symbol])
            if solver.check() == z3.sat:
                model = solver.model()
                domains.add(model[var])
            
            abstract_domains[symbol] = list(domains)
        else:    
            sorted_thresholds = sorted(threshold_set)   
            if op in ['==', '!=']:
                domains.update(sorted_thresholds)
                
                solver = z3.Solver()
                var = z3.Real(symbol)
                solver.add(z3.And([var != t for t in sorted_thresholds]))
                if symbol in restriction_dict:
                    solver.add(restriction_dict[symbol])
                if solver.check() == z3.sat:
                    model = solver.model()
                    z3_val = model[var]
                    frac_val = Fraction(z3_val.numerator().as_long(), z3_val.denominator().as_long())
                    domains.add(frac_val)
    
            else:
                enhanced_thresholds = sorted_thresholds.copy()
                if op in ['<', '>=']:
                    bound_value = get_boundary_value(sorted_thresholds[0], False, symbol,  None if symbol not in restriction_dict else restriction_dict[symbol])
                    if bound_value is not None:
                        enhanced_thresholds.insert(0, bound_value)
                elif op in ['>', "<="]:
                    bound_value = get_boundary_value(sorted_thresholds[-1], True, symbol, None if symbol not in restriction_dict else restriction_dict[symbol])
                    if bound_value is not None:
                        enhanced_thresholds.append(bound_value)
                else:
                    raise ValueError(f"Unsupported operator: {op}")
                
                domains.update(enhanced_thresholds)
                
            abstract_domains[symbol] = sorted(list(domains))

    handled_symbols = {s for (_, s), _ in symbol_inequalities.items()}
    for symbol, constraint in restriction_dict.items():
        if symbol not in handled_symbols:
            solver = z3.Solver()
            solver.add(constraint)
            domains = set()
            for i in range(5):
                if solver.check() == z3.sat:
                    model = solver.model()
                    if symbol.startswith("_N_THRESHOLD_"):
                        var = z3.Real(symbol)
                        z3_val = model[var]
                        frac_val = Fraction(z3_val.numerator().as_long(), z3_val.denominator().as_long())
                        domains.add(frac_val)
                        solver.add(var != frac_val)
                    else:
                        var = z3.String(symbol)
                        z3_val = model[var]
                        domains.add(z3_val)
                        solver.add(var != z3_val)
                else:
                    break
            if len(domains) != 0:
                abstract_domains[symbol] = sorted(list(domains))
            
    return abstract_domains


def get_symbol_domains_size(symbol_domains: SymbolDomains) -> dict[str, Fraction]:
    """
    Calculate the size of symbol domain, for numeric domain return the difference between the maximum and minimum values, for string domain return the number of elements in the domain
    """
    def is_string_symbol(symbol: str) -> bool:
        return bool(re.match(f'^{STRING_SYMBOLIC_PREFIX}\\d+$', symbol))
        
    result = {}
    for symbol, domain in symbol_domains.items():
        if is_string_symbol(symbol):
            # string domain size is always 0
            result[symbol] = Fraction(0)
        else:
            # numeric domain size is represented by the range
            result[symbol] = domain[-1] - domain[0]
    
    return result