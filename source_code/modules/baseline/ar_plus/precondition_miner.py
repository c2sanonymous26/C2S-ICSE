# -*- coding: utf-8 -*-
"""
Association rule mining module

Uses FP-Growth algorithm from mlxtend library to mine preconditions of data constraints
"""

import logging
from typing import Dict, Any
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

from .config import PreconditionMinerConfig, BaseConfig


class PreconditionMiner:
    """Association rule miner
    
    Uses FP-Growth algorithm to mine preconditions:
    1. Mine association rules with fit=1 as consequent
    2. Set minimum confidence as reliability threshold
    3. Select preconditions with highest support and shortest length
    """
    
    def __init__(self, mode):
        self.config = PreconditionMinerConfig.get_config(mode)
        
    def mine_preconditions(self, onehot_data: pd.DataFrame, fit_rate: float) -> Dict[str, Any]:
        """Discover preconditions of data constraints using association rule mining
        
        Uses FP-Growth algorithm to mine frequent itemsets, then generates high-confidence association rules,
        and filters rules with fit_1 as consequent as preconditions.
        
        Args:
            onehot_data: One-hot encoded data, must contain fit_1 column
            fit_rate: Assertion fit rate
        Returns:
            Dict: Result dictionary containing the following fields
            - predm_status: Mining status ('success', 'no_rules_found', 'error')
            - best_precondition: Best precondition
            - total_preconditions: Total number of preconditions
            - preconditions: List of all preconditions
            Returns None if mining fails
        """
        logging.info("Starting association rule mining")
        
        if fit_rate >= BaseConfig.CONSTRAINT_RELIABILITY_THRESHOLD:
            logging.info(f"Assertion holds for over {BaseConfig.CONSTRAINT_RELIABILITY_THRESHOLD*100:.1f}% of samples, skipping precondition mining")
            return {
                'predm_status': 'skip_perfect_fit',
                'best_precondition': None
            }
        elif fit_rate < self.config['MIN_SUPPORT']:
            logging.warning(f"fit_rate({fit_rate:.4f}) is below minimum support for precondition mining ({self.config['MIN_SUPPORT']}), cannot mine preconditions")
            return {
                'predm_status': 'support_too_low',
                'best_precondition': None
            }
            
        if onehot_data.empty:
            logging.warning("Input data is empty, cannot perform association rule mining")
            return {
                'predm_status': 'no_data',
                'best_precondition': None
            }
        
        try:
            assert 'fit_1' in onehot_data.columns, "fit_1 column does not exist in data, cannot perform association rule mining"
            
            min_support = self.config['MIN_SUPPORT']
            
            # Mine frequent itemsets
            frequent_itemsets = self._mine_frequent_itemsets(onehot_data, min_support)
            if frequent_itemsets.empty:
                logging.warning("No frequent itemsets found")
                return {
                    'predm_status': 'no_frequent_itemsets',
                    'best_precondition': None
                }
            
            # Generate association rules
            rules = self._generate_association_rules(frequent_itemsets)
            if rules.empty:
                logging.warning("No association rules found")
                return {
                    'predm_status': 'no_rules_found',
                    'best_precondition': None
                }
            
            # Filter rules with fit_1 as consequent
            fit_rules = self._filter_fit_rules(rules)
            if fit_rules.empty:
                logging.warning("No rules with fit_1 as consequent found")
                return {
                    'predm_status': 'no_fit_rules',
                    'best_precondition': None
                }
            
            # Sort and format preconditions
            best_precondition = self._sort_and_format_preconditions(fit_rules)
            best_precondition['predm_status'] = 'success'
            return best_precondition
            
        except Exception as e:
            logging.error(f"Association rule mining failed: {e}")
            return None
    
    def _mine_frequent_itemsets(self, data: pd.DataFrame, min_support: float) -> pd.DataFrame:
        """Mine frequent itemsets using FP-Growth"""
        try:
            frequent_itemsets = fpgrowth(
                data, 
                min_support=min_support, 
                use_colnames=True,
                max_len=self.config['MAX_PRECONDITION_LENGTH']
            )
            
            logging.info(f"Found {len(frequent_itemsets)} frequent itemsets (support>={min_support})")
            return frequent_itemsets
            
        except Exception as e:
            logging.error(f"Frequent itemset mining failed: {e}")
            return pd.DataFrame()
    
    def _generate_association_rules(self, frequent_itemsets: pd.DataFrame) -> pd.DataFrame:
        """Generate association rules"""        
        try:
            rules = association_rules(
                frequent_itemsets, 
                metric="confidence", 
                min_threshold=self.config['MIN_CONFIDENCE']
            )
            
            logging.info(f"Generated {len(rules)} association rules (confidence>={self.config['MIN_CONFIDENCE']})")
            return rules
            
        except Exception as e:
            logging.error(f"Association rule generation failed: {e}")
            return pd.DataFrame()
    
    def _filter_fit_rules(self, rules: pd.DataFrame) -> pd.DataFrame:
        """Filter rules with fit_1 as consequent and satisfying overall fit rate requirements"""
        if rules.empty:
            return rules
        
        # Filter rules with fit_1 as consequent
        fit_rules = rules[rules['consequents'].apply(
            lambda x: 'fit_1' in [str(item) for item in x]
        )]
        logging.info(f"Filtered {len(fit_rules)} rules with fit_1 as consequent")
        return fit_rules
    
    def _sort_and_format_preconditions(self, fit_rules: pd.DataFrame) -> Dict[str, Any]:
        """Select and format preconditions
        
        Selection strategy:
        1. Prioritize higher overall fit rate (rule_fit_rate)
        2. When rule_fit_rate is the same, select higher confidence
        3. When both are the same, select higher support
        4. When all three are the same, select shorter length
        
        Returns:
            Dict: Best precondition
        """        
        # Add rule_fit_rate column
        # rule_fit_rate = 1 - violation rate
        #  = 1 -  P(precondition=true AND assertion=false)
        #  = 1 - (antecedent_support × (1 - confidence))
        #  = 1 - (antecedent_support - antecedent_support × confidence)
        #  = 1 - (antecedent_support - support)
        fit_rules = fit_rules.copy()
        fit_rules['rule_fit_rate'] = fit_rules.apply(
            lambda row: 1 - (row['antecedent support'] - row['support']), axis=1
        )
        fit_rules['antecedent_length'] = fit_rules['antecedents'].apply(len)
        
        # Sort by rule_fit_rate desc, confidence desc, support desc, length asc
        fit_rules = fit_rules.sort_values(['rule_fit_rate', 'confidence', 'support', 'antecedent_length'], 
                                        ascending=[False, False, False, True])
        
        first_fit_rule = fit_rules.iloc[0]
        best_precondition = {
            'best_precondition': first_fit_rule['antecedents'],
            'rule_fit_rate': first_fit_rule['rule_fit_rate'],
            'rule_confidence': first_fit_rule['confidence'],
            'rule_support': first_fit_rule['support'],
            'precondition_length': first_fit_rule['antecedent_length'],
            'description': f"{' AND '.join(first_fit_rule['antecedents'])}"
        }    
        
        return best_precondition 