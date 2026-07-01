# ----- Structure Grammar -----

STRUCTURE_GRAMMAR = """
?start: structure

structure: implies_expr                                     -> prod_structure_expr

implies_expr: or_expr "implies" implies_expr                -> prod_implies
        | or_expr                                           -> prod_or_expr

or_expr: and_expr "or" or_expr                              -> prod_or
        | and_expr                                          -> prod_and_expr

and_expr: not_expr "and" and_expr                           -> prod_and
        | not_expr                                          -> prod_not_expr

not_expr: "not" not_expr                                    -> prod_not
        | atom_expr                                         -> prod_atom_expr

atom_expr: "forall" variable "in dataset" "(" structure ")" -> prod_forall
        | "exists" variable "in dataset" "(" structure ")"  -> prod_exists
        | "(" structure ")"                                 -> prod_paren
        | bfunc_signature                                   -> prod_bfunc

variable: "v" NATURAL                                       -> prod_variable
bfunc_signature: "bfunc" NATURAL "(" variable_list ")"      -> prod_bfunc_signature
variable_list: variable ("," variable)*                     -> prod_variable_list

NATURAL: /0|[1-9]\d*/

%import common.WS
%ignore WS
"""

# ----- Body Grammar -----

BG_LOGIC_PRODS = """
?start: body

body: implies_expr                                      -> prod_body_expr

implies_expr: or_expr "->" implies_expr                 -> prod_body_implies
        | or_expr                                       -> prod_body_or_expr

or_expr: and_expr "||" or_expr                          -> prod_body_or
        | and_expr                                      -> prod_body_and_expr

and_expr: not_expr "&&" and_expr                        -> prod_body_and
        | not_expr                                      -> prod_body_not_expr

not_expr: "!" not_expr                                  -> prod_body_not
        | atom_expr                                     -> prod_body_atom_expr

atom_expr: "(" body ")"                                 -> prod_body_paren
        | _cmp_expr                                     -> prod_body_cmp_expr

_cmp_expr: str_cmp_expr
        | num_cmp_expr
"""

BG_STR_CMP_PRODS = """
str_cmp_expr: str_field STR_CMP_OP str_target_expr       -> prod_str_cmp_expr_1
        | str_target_expr STR_CMP_OP str_field           -> prod_str_cmp_expr_2
                
str_field: "v" NATURAL "." CUSTOM_STR_FIELD_NAME         -> prod_str_field

str_target_expr: ESCAPED_STRING                          -> prod_str_target_literal
        | STR_SYMBOL_PREFIX NATURAL                      -> prod_str_target_threshold
        | str_field                                      -> prod_str_target_field
"""

BG_STR_CMP_TERMINALS = """
NATURAL: /0|[1-9]\d*/

ESCAPED_STRING: "\'" (_STRING_ESC_INNER | /^/) "\'"

STR_CMP_OP: /==|!=/
STR_SYMBOL_PREFIX: /STHRESHOLD/
CUSTOM_STR_FIELD_NAME: /{str_field_name_regex}/

%import common._STRING_ESC_INNER
%import common.WS
%ignore WS
"""

BG_NUM_CMP_PRODS = """
num_cmp_expr: num_expr NUM_CMP_OP num_target_expr        -> prod_num_cmp_expr_2
        | num_target_expr NUM_CMP_OP num_expr            -> prod_num_cmp_expr_1

num_expr: num_term "+" num_expr                          -> prod_num_add
        | num_term "-" num_expr                          -> prod_num_sub
        | num_term                                       -> prod_num_term_single

num_term: num_factor "\u00d7" num_term                   -> prod_num_mul
        | num_factor "\u00f7" num_term                   -> prod_num_div
        | num_factor "%" num_term                        -> prod_num_mod
        | num_factor                                     -> prod_num_factor_single

num_factor: "-" num_expr                                 -> prod_num_factor_neg
        | "(" num_expr ")"                               -> prod_num_factor_paren
        | math_func_expr                                 -> prod_num_factor_math_func
        | num_field                                      -> prod_num_factor_field
        | SIGNED_NUMBER                                  -> prod_num_factor_literal

math_func_expr: "abs" "(" num_expr ")"                   -> prod_math_func_abs
        | "sin" "(" num_expr ")"                         -> prod_math_func_sin
        | "asin" "(" num_expr ")"                        -> prod_math_func_asin
        | "cos" "(" num_expr ")"                         -> prod_math_func_cos
        | "acos" "(" num_expr ")"                        -> prod_math_func_acos
        | "tan" "(" num_expr ")"                         -> prod_math_func_tan
        | "atan" "(" num_expr ")"                        -> prod_math_func_atan
        | "atan2" "(" num_expr "," num_expr ")"          -> prod_math_func_atan2
        | "degrees" "(" num_expr ")"                     -> prod_math_func_degrees
        | "radians" "(" num_expr ")"                     -> prod_math_func_radians
        | "pow" "(" num_expr "," SIGNED_NUMBER ")"       -> prod_math_func_pow
        | "sqrt" "(" num_expr ")"                        -> prod_math_func_sqrt
        | "cbrt" "(" num_expr ")"                        -> prod_math_func_cbrt
        | "exp" "(" num_expr ")"                         -> prod_math_func_exp
        | "log" "(" num_expr ")"                         -> prod_math_func_log
        | "log10" "(" num_expr ")"                       -> prod_math_func_log10
        | "log1p" "(" num_expr ")"                       -> prod_math_func_log1p
        | "min" "(" num_expr "," num_expr ")"            -> prod_math_func_min
        | "max" "(" num_expr "," num_expr ")"            -> prod_math_func_max

num_field: "v" NATURAL "." CUSTOM_NUM_FIELD_NAME         -> prod_num_field

num_target_expr: num_target_term "+" num_target_expr     -> prod_num_target_add
        | num_target_term "-" num_target_expr            -> prod_num_target_sub
        | num_target_term                                -> prod_num_target_term
                
num_target_term: num_target_factor "\u00d7" num_target_term     -> prod_num_target_mul
        | num_target_factor "\u00f7" num_target_term            -> prod_num_target_div
        | num_target_factor "%" num_target_term                 -> prod_num_target_mod
        | num_target_factor                                     -> prod_num_target_factor

num_target_factor: NUM_SYMBOL_PREFIX NATURAL        -> prod_num_target_threshold
        | num_expr                                  -> prod_num_target_num_expr
        | "(" num_target_expr ")"                   -> prod_num_target_paren
        | "-" num_target_expr                       -> prod_num_target_neg
"""

BG_NUM_CMP_TERMINALS =  """
NATURAL: /0|[1-9]\d*/
NUM_CMP_OP: /==|!=|<=|>=|<|>/
NUM_SYMBOL_PREFIX: /NTHRESHOLD/
CUSTOM_NUM_FIELD_NAME: /{num_field_name_regex}/

%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
"""

# * Attention: When defining `NUM_CMP_OP`, ">=" and "<=" must be placed before ">" and "<"
BODY_GRAMMAR = (
    BG_LOGIC_PRODS
    + "\n"
    + BG_STR_CMP_PRODS
    + "\n"
    + BG_NUM_CMP_PRODS
    + "\n"
    + """
NATURAL: /0|[1-9]\d*/
ESCAPED_STRING: "\'" (_STRING_ESC_INNER | /^/) "\'"

STR_CMP_OP: /==|!=/
STR_SYMBOL_PREFIX: /STHRESHOLD/
CUSTOM_STR_FIELD_NAME: /{str_field_name_regex}/

NUM_CMP_OP: /==|!=|<=|>=|<|>/
NUM_SYMBOL_PREFIX: /NTHRESHOLD/
CUSTOM_NUM_FIELD_NAME: /{num_field_name_regex}/

%import common._STRING_ESC_INNER
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
"""
)

# ----- Symbol Restrictions Grammar -----


# * Attention: When defining `LT_SYMBOLS` and `GT_SYMBOLS`, ">=" and "<=" must be placed before ">" and "<"
RESTRICTION_GRAMMAR = """
?start: restriction

restriction: num_restriction                            -> prod_num_restriction
        | str_restriction                               -> prod_str_restriction

num_restriction: num_value_restriction                  -> prod_num_value_restriction
        | num_range_restriction                         -> prod_num_range_restriction

num_value_restriction: num_symbol "==" SIGNED_NUMBER    -> prod_num_value_eq
        | num_symbol "!=" SIGNED_NUMBER                 -> prod_num_value_neq

num_range_restriction: (SIGNED_NUMBER LT_SYMBOLS)? num_symbol LT_SYMBOLS SIGNED_NUMBER        -> prod_num_range_lt
        | (SIGNED_NUMBER GT_SYMBOLS)? num_symbol GT_SYMBOLS SIGNED_NUMBER                     -> prod_num_range_gt

num_symbol: NUM_SYMBOL_PREFIX NATURAL                   -> prod_num_symbol

str_restriction: str_value_restriction                  -> prod_str_value_restriction

str_value_restriction: str_symbol "==" ESCAPED_STRING   -> prod_str_value_eq
        | str_symbol "!=" ESCAPED_STRING                -> prod_str_value_neq

str_symbol: STR_SYMBOL_PREFIX NATURAL                   -> prod_str_symbol


NATURAL: /0|[1-9]\d*/
ESCAPED_STRING: "\'" (_STRING_ESC_INNER | /^/) "\'"
STR_SYMBOL_PREFIX: /STHRESHOLD/
NUM_SYMBOL_PREFIX: /NTHRESHOLD/
LT_SYMBOLS: /<=|</
GT_SYMBOLS: />=|>/


%import common._STRING_ESC_INNER
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
"""
