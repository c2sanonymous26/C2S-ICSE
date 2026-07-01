import random
from z3 import z3
from collections import deque

from ...utils import CTreeNode
from . import EFormulaDict, VEConstraint


BASE_WEIGHT = 1
GOAL1_RATE = 0.2
GOAL2_RATE = 0.02

def find_Eformulas(ctree_root: CTreeNode, rlayers: set[int]) -> EFormulaDict:
    """Find Eformulas (undecidable formulas meet the rlayers)
    
    Args:
        ctree_root: Constraint tree root node
        
    Returns:
        EFormulaDict
    """
        
    def _is_undecidable_formula(node: CTreeNode, is_under_quantifier: bool) -> bool:
        node_type = node[0]
        node_goal = node[2]['goal_truth']
        children = node[3]
        assert len(children) == 2, f"Expect 2 children, but got {len(children)}"
        left_has_symbol = children[0][2]['has_symbol']
        right_has_symbol = children[1][2]['has_symbol']
        
        return ((node_type == 'and' and not node_goal and left_has_symbol and right_has_symbol) or \
            (node_type == 'or' and node_goal and left_has_symbol and right_has_symbol) or \
            (node_type == 'implies' and node_goal and left_has_symbol and right_has_symbol)) \
            and is_under_quantifier
    
    def _get_undecidable_formula_rlayer_dict() -> dict[str, int]:
        cur_rlayer = 1
        depth_rlayer_dict = {}
        undecidable_formula_rlayer_dict = {}
        queue = deque([(ctree_root, False)])
        
        while queue:
            node, is_under_quantifier = queue.popleft()
            if node[0] in ('forall', 'exists'):
                subnode = node[3][0]
                queue.append((subnode, True))
            elif node[0] in ('and', 'or', 'implies'):
                if _is_undecidable_formula(node, is_under_quantifier):
                    node_depth = node[2]['depth']
                    node_id = f'{node[0]}_{node[1]}'
                    if node_depth not in depth_rlayer_dict:
                        node_rlayer = cur_rlayer
                        depth_rlayer_dict[node_depth] = node_rlayer
                        cur_rlayer += 1
                    else:
                        node_rlayer = depth_rlayer_dict[node_depth]
                    undecidable_formula_rlayer_dict[node_id] = node_rlayer
                
                left_node, right_node = node[3][0], node[3][1]
                queue.append((left_node, is_under_quantifier))
                queue.append((right_node, is_under_quantifier))
            elif node[0] == 'not':
                subnode = node[3][0]
                queue.append((subnode, is_under_quantifier))
            else:
                pass
        
        return undecidable_formula_rlayer_dict
    
    eformulas = {}
    undecidable_formula_rlayer_dict = _get_undecidable_formula_rlayer_dict()
    queue = deque([ctree_root])
    
    while queue:
        node = queue.popleft()
        
        if node[0] in ('forall', 'exists'):
            queue.append(node[3][0])
        elif node[0] in ('and', 'or', 'implies'):
            left_node, right_node = node[3][0], node[3][1]
            node_id = f'{node[0]}_{node[1]}'
            if node_id in undecidable_formula_rlayer_dict \
                and undecidable_formula_rlayer_dict[node_id] in rlayers:
                
                node_rlayer = undecidable_formula_rlayer_dict[node_id]
                node_depth = node[2]['depth']
                eformulas[(node_id, node_depth, node_rlayer)] = (f"{left_node[0]}_{left_node[1]}", f"{right_node[0]}_{right_node[1]}")
                
            queue.append(left_node)
            queue.append(right_node)
        elif node[0] == 'not':
            queue.append(node[3][0])
        else:
            pass
                
    return eformulas

def construct_ve_constraints(
    ctree_root: CTreeNode, 
    cct_node_id_dict: dict[str, list[str]], 
    eformulas: EFormulaDict, 
    slv_data_num_dict: dict[str, int]
    ) -> list[VEConstraint]:
    
    ve_constraints = []
    if len(eformulas) == 0:
        return ve_constraints

    outer_quantifiers = _get_outer_quantifiers(ctree_root)
    
    for (node_id, _, _), (left_node_id, right_node_id) in eformulas.items():
        
        formula_id = node_id.split('_(')[0]
        outer_ctxs = outer_quantifiers[formula_id]
                
        if node_id.startswith('and'):
            
            tp0_num, tp1_num, tp2_num = _count_truth_pairs(
                _create_node_id_pairs(cct_node_id_dict[left_node_id], cct_node_id_dict[right_node_id]), 
                [(False, False), (False, True), (True, False)]
            ) 
            
            # goal1
            ve_constraints.append((tp0_num >= 1, BASE_WEIGHT * 2))
            ve_constraints.append((tp1_num >= 1, BASE_WEIGHT * 2))
            ve_constraints.append((tp2_num >= 1, BASE_WEIGHT * 2))
            
            # goal2
            goal2_target = 1
            for ctx in outer_ctxs:
                goal2_target *= slv_data_num_dict[ctx]
            goal2_target = goal2_target * GOAL2_RATE
            
            ve_constraints.append((tp0_num >= goal2_target, BASE_WEIGHT))
            ve_constraints.append((tp1_num >= goal2_target, BASE_WEIGHT))
            ve_constraints.append((tp2_num >= goal2_target, BASE_WEIGHT))
        
        elif node_id.startswith('or'):
            
            tp0_num, tp1_num, tp2_num = _count_truth_pairs(
                _create_node_id_pairs(cct_node_id_dict[left_node_id], cct_node_id_dict[right_node_id]), 
                [(True, True), (True, False), (False, True)]
            ) 
            
            # goal1
            ve_constraints.append((tp0_num >= 1, BASE_WEIGHT * 2))
            ve_constraints.append((tp1_num >= 1, BASE_WEIGHT * 2))
            ve_constraints.append((tp2_num >= 1, BASE_WEIGHT * 2))
            
            # goal2
            goal2_target = 1
            for ctx in outer_ctxs:
                goal2_target *= slv_data_num_dict[ctx]
            goal2_target = goal2_target * GOAL2_RATE
            
            ve_constraints.append((tp0_num >= goal2_target, BASE_WEIGHT))
            ve_constraints.append((tp1_num >= goal2_target, BASE_WEIGHT))
            ve_constraints.append((tp2_num >= goal2_target, BASE_WEIGHT))
            
        elif node_id.startswith('implies'):
            
            tp0_num, tp1_num, tp2_num = _count_truth_pairs(
                _create_node_id_pairs(cct_node_id_dict[left_node_id], cct_node_id_dict[right_node_id]), 
                [(False, True), (True, True), (False, False)]
            ) 
            
            # goal1
            ve_constraints.append((tp0_num >= 1, BASE_WEIGHT * 2))
            ve_constraints.append((tp1_num >= 1, BASE_WEIGHT * 2))
            ve_constraints.append((tp2_num >= 1, BASE_WEIGHT * 2))
            
            # goal2
            goal2_target = 1
            for ctx in outer_ctxs:
                goal2_target *= slv_data_num_dict[ctx]
            goal2_target = goal2_target * GOAL2_RATE
            
            ve_constraints.append((tp0_num >= goal2_target, BASE_WEIGHT))
            ve_constraints.append((tp1_num >= goal2_target, BASE_WEIGHT))
            ve_constraints.append((tp2_num >= goal2_target, BASE_WEIGHT))
            
        else:
            raise ValueError(f"Invalid VE structure: {node_id}")
        
    return ve_constraints

def _get_outer_quantifiers(ctree_root: CTreeNode) -> dict[str, set[str]]:
    outer_quantifiers = {}
    queue = deque([(ctree_root, set())])
    
    while queue:
        node, oq_set = queue.popleft()
        
        if node[0] in ('forall', 'exists'):
            new_oq_set = oq_set | {node[2]['in']}
            queue.append((node[3][0], new_oq_set))
        elif node[0] in ('and', 'or', 'implies'):
            node_id = f'{node[0]}_{node[1]}'
            outer_quantifiers[node_id] = set(oq_set)            
            queue.append((node[3][0], oq_set.copy()))
            queue.append((node[3][1], oq_set.copy()))
        elif node[0] == 'not':
            queue.append((node[3][0], oq_set.copy()))
    
    return outer_quantifiers
    
def _create_node_id_pairs(left_node_id_list: list[str], right_node_id_list: list[str]) -> list[tuple[str, str]]:
    # Ensure both lists have the same length
    assert len(left_node_id_list) == len(right_node_id_list), f"Left and right node lists must have the same length, left length: {len(left_node_id_list)} right length: {len(right_node_id_list)}"
    
    # Extract suffix for each node
    def get_suffix(node_id: str) -> str:
        return node_id[node_id.index('_(') + 2 : node_id.rindex(')')]
    
    # Sort both lists by suffix
    left_sorted = sorted(left_node_id_list, key=get_suffix)
    right_sorted = sorted(right_node_id_list, key=get_suffix)
    
    # Direct pairing
    ret = list(zip(left_sorted, right_sorted))
    return ret

def _count_truth_pairs(node_id_pairs: list[tuple[str, str]], truth_pairs: list[tuple[bool, bool]]) -> z3.ArithRef:
    assert len(truth_pairs) == 3, f"truth_pairs must be a list of 3 tuples, instead of {len(truth_pairs)}"
    
    sampled_num = int(len(node_id_pairs) * GOAL1_RATE)
    random.shuffle(node_id_pairs)
    
    tp0_sample_start_index = random.randint(0, len(node_id_pairs) - sampled_num)
    tp0_sampled_node_id_pairs = node_id_pairs[tp0_sample_start_index: tp0_sample_start_index + sampled_num]
    tp0_index_ref_pairs = [(z3.Bool(node_id_pair[0]), z3.Bool(node_id_pair[1])) for node_id_pair in tp0_sampled_node_id_pairs]
    tp0_num = z3.Sum([z3.If(z3.And(index_ref_pair[0] == truth_pairs[0][0], index_ref_pair[1] == truth_pairs[0][1]), 1, 0) for index_ref_pair in tp0_index_ref_pairs])
    
    tp1_sample_start_index = random.randint(0, len(node_id_pairs) - sampled_num)
    tp1_sampled_node_id_pairs = node_id_pairs[tp1_sample_start_index: tp1_sample_start_index + sampled_num]
    tp1_index_ref_pairs = [(z3.Bool(node_id_pair[0]), z3.Bool(node_id_pair[1])) for node_id_pair in tp1_sampled_node_id_pairs]
    tp1_num = z3.Sum([z3.If(z3.And(index_ref_pair[0] == truth_pairs[1][0], index_ref_pair[1] == truth_pairs[1][1]), 1, 0) for index_ref_pair in tp1_index_ref_pairs])
    
    tp2_sample_start_index = random.randint(0, len(node_id_pairs) - sampled_num)
    tp2_sampled_node_id_pairs = node_id_pairs[tp2_sample_start_index: tp2_sample_start_index + sampled_num]
    tp2_index_ref_pairs = [(z3.Bool(node_id_pair[0]), z3.Bool(node_id_pair[1])) for node_id_pair in tp2_sampled_node_id_pairs]
    tp2_num = z3.Sum([z3.If(z3.And(index_ref_pair[0] == truth_pairs[2][0], index_ref_pair[1] == truth_pairs[2][1]), 1, 0) for index_ref_pair in tp2_index_ref_pairs])
        
    return tp0_num, tp1_num, tp2_num