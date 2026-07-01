"""
AR+ pipeline orchestration module

Coordinates the execution flow of all components to implement the complete data constraint mining pipeline
"""

import json
import logging
import signal
import time
import random
from pathlib import Path
from typing import Optional
import pandas as pd

from .data_processor import create_data_processor
from .assertion_miner import AssertionMiner
from .assertion_validator import AssertionValidator
from .precondition_miner import PreconditionMiner
from .config import BaseConfig
from . import LEVEL2_SEPARATOR


class TargetTimeoutException(Exception):
    """Target processing timeout exception"""
    pass


def target_timeout_handler(signum, frame):
    """Target processing timeout signal handler"""
    raise TargetTimeoutException("Target processing timeout")


class ARPlusPipeline:
    """AR+ main pipeline
    
    Executes different mining processes based on mode:
    - single mode: assertion mining + assertion validation + precondition mining
    - carid_join mode: assertion mining + assertion validation + precondition mining
    - carid_diff mode: assertion mining + assertion validation + precondition mining
    - pairwise mode: assertion mining + assertion validation (only obtain fit rate)
    """
    
    def __init__(self, mode: str, cmp: str, output_dir: Optional[Path] = None):
        self.mode = mode
        self.cmp = cmp
        self.output_dir = output_dir
        
        # Initialize components
        self.data_processor = create_data_processor(mode)
        self.asrt_miner = AssertionMiner(mode, cmp)
        
        # All modes need assertion validator
        self.asrt_validator = AssertionValidator()
        
        # Only single, carid_join, and carid_diff modes need precondition miner
        if mode in ['single', 'carid_join', 'carid_diff']:
            self.pred_miner = PreconditionMiner(mode)
        else:
            self.pred_miner = None

    def run_once(self, data_file_path: Path, run_id: int) -> bool:
        """Randomly select a single target for constraint mining and save as constraint_i.json
        
        Args:
            data_file_path: Data file path
            run_id: Run ID, used to generate filename
            
        Returns:
            bool: Whether completed successfully
        """
        logging.info(LEVEL2_SEPARATOR)
        # Data preprocessing, generate two specialized DataFrames
        asrtm_df, predm_df = self._load_data(data_file_path)
        logging.info(LEVEL2_SEPARATOR)
        
        logging.info(LEVEL2_SEPARATOR)
        # Get targets
        available_targets = self.data_processor.get_asrtm_targets()
        if not available_targets:
            logging.error("No available target fields")
            return False
    
        # Randomly select target
        target_col = random.choice(available_targets)
        logging.info(f"Target field: {target_col} (selected from {len(available_targets)} candidates)")
        logging.info(LEVEL2_SEPARATOR)
        
        # Process single target
        asrt_result, pred_result, overall_time, asrtm_time, predm_time = self._process_single_target(target_col, asrtm_df, predm_df)

        # Combine results
        final_result = self._combine_results(asrt_result, pred_result, target_col, overall_time, asrtm_time, predm_time)
        if final_result is None:
            return False
        else:
            self._save_constraint(final_result, run_id)
            return True
    
    def _save_constraint(self, constraint_result: dict, run_id: int):
        """Save single constraint result to constraint_i.json
        
        Args:
            constraint_result: Constraint result dictionary
            run_id: Run ID
        """
        filename = f"constraint_{run_id}.json"
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(constraint_result, f, ensure_ascii=False, indent=2, default=str)
            
            logging.info(f"Constraint result saved: {filepath}")
                
        except Exception as e:
            logging.error(f"Failed to save constraint result: {e}")
    
    def _load_data(self, data_file_path: Path):
        """Data preprocessing, generate two specialized DataFrames"""
        asrtm_df, predm_df = self.data_processor.load_and_preprocess_data(data_file_path)       
        return asrtm_df, predm_df
    
    def _process_single_target(self, target_col: str, asrtm_df, predm_df):
        """Complete mining process for a single target: assertion mining + validation + precondition mining
        
        Args:
            target_col: Target column name
            asrtm_df: DataFrame for assertion mining
            predm_df: DataFrame for precondition mining
        
        Returns:
            tuple: (asrt_result, pred_result, overall_time, asrtm_time, predm_time)
            - asrt_result: Assertion mining result, None indicates failure
            - pred_result: Precondition mining result, None indicates failure or not executed
            - overall_time: Target processing time (seconds)
            - asrtm_time: Assertion mining time (seconds)
            - predm_time: Precondition mining time (seconds)
        """

        start_time = time.time()
        
        # Initialize variables to ensure accessibility during exception handling
        asrt_result = None
        asrtm_time = 0
        predm_time = 0
        fit_rate = 0.0
        fit_data = None
        
        # Set timeout signal
        handler = signal.signal(signal.SIGALRM, target_timeout_handler)
        signal.alarm(BaseConfig.TARGET_PROCESSING_TIMEOUT_SECONDS)
        
        try:
            logging.info(f"Timeout: {BaseConfig.TARGET_PROCESSING_TIMEOUT_SECONDS} seconds")
            
            # Assertion Mining
            logging.info(LEVEL2_SEPARATOR)
            logging.info("Starting assertion mining...")
            asrt_result, asrtm_time = self._assertion_mining_for_target(target_col, asrtm_df)
            if asrt_result is None or asrt_result['best_assertion'] is None:
                logging.error("Assertion mining failed")
                logging.info(LEVEL2_SEPARATOR)
                overall_time = time.time() - start_time
                return None, None, overall_time, asrtm_time, 0
            logging.info(f"Assertion mining completed, assertion: {str(asrt_result['best_assertion'])} (fitness: {asrt_result['best_fitness']:.9f})")
            logging.info(LEVEL2_SEPARATOR)
            
            # Assertion Validation
            logging.info(LEVEL2_SEPARATOR)
            logging.info("Starting assertion validation...")
            fit_rate, fit_data = self._validate_assertion(target_col, asrtm_df, asrt_result)
            logging.info(f"Assertion validation completed, fit rate: {fit_rate:.4f} ({fit_data.sum()}/{len(fit_data)})")
            asrt_result['fit_rate'] = fit_rate
            logging.info(LEVEL2_SEPARATOR)
            
            # Precondition Mining
            if self.mode in ['single', 'carid_join', 'carid_diff']:
                logging.info(LEVEL2_SEPARATOR)
                logging.info("Starting precondition mining...")
                
                precondition_result, predm_time = self._precondition_mining_for_target(predm_df, fit_rate, fit_data)
                if precondition_result is None or precondition_result['best_precondition'] is None:
                    if precondition_result is None:
                        logging.info("Precondition mining failed")
                    else:
                        logging.info(f"No precondition, reason: {precondition_result['predm_status']}")
                    logging.info(LEVEL2_SEPARATOR)
                    overall_time = time.time() - start_time
                    return asrt_result, None, overall_time, asrtm_time, predm_time
                else:
                    logging.info(f"Precondition mining completed, precondition: {precondition_result['description']} (rule fit_rate: {precondition_result['rule_fit_rate']:.4f})")
                    logging.info(LEVEL2_SEPARATOR)
                    overall_time = time.time() - start_time
                    return asrt_result, precondition_result, overall_time, asrtm_time, predm_time
            elif self.mode == 'pairwise':
                logging.info(LEVEL2_SEPARATOR)
                logging.info("Skipping precondition mining due to complexity exploison.")
                logging.info(LEVEL2_SEPARATOR)
                overall_time = time.time() - start_time
                return asrt_result, None, overall_time, asrtm_time, 0
                
        except TargetTimeoutException:
            overall_time = BaseConfig.TARGET_PROCESSING_TIMEOUT_SECONDS
            logging.warning("Processing timeout ({overall_time}s)")
            
            # If assertion mining succeeded, keep partial results
            if asrt_result is not None and asrt_result['best_assertion'] is not None:
                # If validation not completed, try quick validation
                if fit_data is None:
                    fit_rate, fit_data = self._validate_assertion(target_col, asrtm_df, asrt_result)
                    asrt_result['fit_rate'] = fit_rate
                    logging.info(f"Completed assertion validation (timeout), fit rate: {fit_rate:.4f}")
                
                logging.info(LEVEL2_SEPARATOR)
                return asrt_result, None, overall_time, asrtm_time, predm_time
            else:
                logging.info(LEVEL2_SEPARATOR)  
                return None, None, overall_time, asrtm_time, predm_time
        finally:         
            # Cancel timeout signal
            signal.alarm(0)
            signal.signal(signal.SIGALRM, handler)
    
    def _assertion_mining_for_target(self, target_col: str, asrtm_df: pd.DataFrame):
        """Perform assertion mining for a single target"""
        start_time = time.time()
        try:
            X, y = self.data_processor.prepare_asrtm_data(asrtm_df, target_col)
            logging.info(f"Target: {target_col} - Features: {list(X.columns)}")
            
            result = self.asrt_miner.train(X, y, target_col)
            return result, time.time() - start_time
        except Exception as e:
            logging.error(f"Assertion mining exception: {e}")
            return None, time.time() - start_time
    
    def _validate_assertion(self, target_col: str, asrtm_df: pd.DataFrame, asrt_result: dict):
        """Perform assertion validation for a single target
        
        Args:
            target_col: Target column name
            asrtm_df: DataFrame for validation
            asrt_result: Assertion mining result
        
        Returns:
            tuple: (fit_rate, fit_data)
        """
        try:
            X, y = self.data_processor.prepare_asrtm_data(asrtm_df, target_col)
            fit_rate, fit_data = self.asrt_validator.validate_assertion(X, y, asrt_result, self.cmp)
            return fit_rate, fit_data
        except Exception as e:
            logging.error(f"Assertion validation exception: {e}")
            return 0.0, None
    
    def _precondition_mining_for_target(self, predm_df, fit_rate, fit_data):
        """Perform precondition mining for a single target
        
        Args:
            predm_df: DataFrame for precondition mining
            fit_rate: Fit rate from assertion validation
            fit_data: Fit data from assertion validation (0/1 sequence)
        
        Returns:
            tuple: (precondition_result, precondition_mining_time)
            - precondition_result: Precondition mining result dictionary, None indicates failure
            - precondition_mining_time: Precondition mining time (seconds)
        """
        try:            
            start_time = time.time()
            
            # Prepare data for precondition mining phase (binning + one-hot encoding)
            predm_data = self.data_processor.prepare_predm_data(predm_df, fit_data)

            # Mine preconditions
            precondition_result = self.pred_miner.mine_preconditions(predm_data, fit_rate)
            precondition_mining_time = time.time() - start_time
            
            return precondition_result, precondition_mining_time
            
        except Exception as e:
            precondition_mining_time = time.time() - start_time
            logging.error(f"Precondition mining exception: {e}")
            return None, precondition_mining_time
    
    def _combine_results(self, asrt_result: dict, pred_result: dict, target_col: str, overall_time: float, asrtm_time: float, predm_time: float) -> dict:
        """Combine assertion and precondition results to generate final usable constraint
        
        Decide final constraint type based on assertion quality and precondition status:
        1. asrt_result is None: Assertion mining failed, return None
        2. asrt_result is not None and pred_result is None: Assertion mining succeeded, precondition mining failed or none, check asrt_result['fit_rate']
        3. asrt_result is not None and pred_result is not None: Both assertion and precondition mining succeeded, check pred_result['rule_fit_rate']
        
        Args:
            asrt_result: Assertion mining result, None indicates mining failure
            pred_result: Precondition mining result, None indicates mining failure or skipped
            target_col: Target column name
            overall_time: Target processing time (seconds)
            asrtm_time: Assertion mining time (seconds)
            predm_time: Precondition mining time (seconds)
            
        Returns:
            dict: Final result containing status, assertion, preconditions and other fields
        """
        
        if asrt_result is None:
            return None
        else:
            if pred_result is None:
                if asrt_result['fit_rate'] >= BaseConfig.CONSTRAINT_RELIABILITY_THRESHOLD:
                    return {
                        "mode": self.mode,
                        "cmp": self.cmp,
                        "target_col": target_col,
                        "status": "success_simple_constraint",
                        "assertion": asrt_result['best_assertion'],
                        "rule_fit_rate": asrt_result['fit_rate'],
                        "overall_time": overall_time,
                        "asrtm_time": asrtm_time,
                        "predm_time": predm_time,
                        "asrt_info": {
                            "fitness": asrt_result['best_fitness'],
                            "was_early_stopped": asrt_result['was_early_stopped'],
                            "generations_completed": asrt_result['generations_completed'],
                            "semantic_selection": asrt_result.get("semantic_selection", {}),
                        }
                    }
                else:
                    return None
            else:
                if pred_result['rule_fit_rate'] >= BaseConfig.CONSTRAINT_RELIABILITY_THRESHOLD:
                    return {
                        "mode": self.mode,
                        "cmp": self.cmp,
                        "target_col": target_col,
                        "status": "success_with_preconditions",
                        "assertion": asrt_result['best_assertion'],
                        "precondition": pred_result['best_precondition'],
                        "rule_fit_rate": pred_result['rule_fit_rate'],
                        "overall_time": overall_time,
                        "asrtm_time": asrtm_time,
                        "predm_time": predm_time,
                        "asrt_info": {
                            "fitness": asrt_result['best_fitness'],
                            "was_early_stopped": asrt_result['was_early_stopped'],
                            "generations_completed": asrt_result['generations_completed'],
                            "semantic_selection": asrt_result.get("semantic_selection", {}),
                        },
                        "pred_info": {
                            "rule_confidence": pred_result['rule_confidence'],
                            "rule_support": pred_result['rule_support'],
                            "precondition_length": pred_result['precondition_length'],
                            "description": pred_result['description'],
                        }
                    }
                else:
                    return None
