# -*- coding: utf-8 -*-
"""
Assertion mining module

Implements enhanced symbolic regression based on gplearn library for mining assertion parts of data constraints
"""

import logging
import pandas as pd
import numpy as np
from gplearn.genetic import SymbolicRegressor
from gplearn.fitness import make_fitness
import warnings

from .config import AssertionMinerConfig
from .semantic_checker import SemanticChecker

warnings.simplefilter(action='ignore', category=FutureWarning)


class AssertionMiner:
    """Assertion miner
    
    Uses symbolic regression for training to discover assertion parts of data constraints
    """
    
    def __init__(self, mode: str, cmp: str):
        self.mode = mode
        self.cmp = cmp
        self.semantic_selection_records: dict[int, dict] = {}
    
    def train(self, X: pd.DataFrame, y: pd.Series, target_col: str) -> dict:
        """Train symbolic regression model
        
        Args:
            X: Feature data
            y: Target data
            target_col: Target column name
            
        Returns:
            dict: Result dictionary containing the following fields
            - best_assertion: Best assertion formula (gplearn._program object)
            - best_fitness: Best fitness value
            - training_generations: Actual training generations
            - programs_info: List of all candidate program information
            - was_early_stopped: Whether early stopped
        """
        
        config = AssertionMinerConfig.get_config(self.mode)
        self.semantic_selection_records = {}
        
        
        # Add training-specific parameters
        config['metric'] = self._create_fitness(self.cmp, X)
        config['feature_names'] = list(X.columns)
        
        # Separate early stopping parameters
        early_stopping_config = {
            'max_generations': config.pop('MAX_GENERATIONS'),
            'early_stopping_patience': config.pop('EARLY_STOPPING_PATIENCE'),
            'early_stopping_min_delta': config.pop('EARLY_STOPPING_MIN_DELTA'),
            'early_stopping_batch_generations': config.pop('EARLY_STOPPING_BATCH_GENERATIONS'),
        }
        
        # Create symbolic regressor
        # Convert config keys to lowercase (SymbolicRegressor requires lowercase parameters)
        sr_config = {key.lower(): value for key, value in config.items()}
        gp = SymbolicRegressor(**sr_config)
        
        # Execute training (with early stopping)
        training_result = self._train_with_early_stopping(
            gp, X, y, target_col, early_stopping_config
        )
        
        # Format results
        result = self._format_training_result(gp, training_result, target_col)
        
        return result
    
    def _create_fitness(self, cmp: str, X: pd.DataFrame):
        """Create fitness function"""
        def fitness(y, y_pred, w):
            """Calculate fitness"""
            
            def cmpr(y, y_pred):
                count = 0
                precision = AssertionMinerConfig.FITNESS_PRECISION
                multiplier = round(1.0 / precision)  # Use round to avoid floating point errors
                
                for truth, pred in zip(y, y_pred):
                    # Use simple round for precision handling
                    rounded_truth = round(truth * multiplier) / multiplier
                    rounded_pred = round(pred * multiplier) / multiplier
                    
                    if cmp == "eq":
                        if rounded_truth == rounded_pred:
                            count += 1
                    elif cmp == "le":
                        if rounded_truth <= rounded_pred:
                            count += 1
                    elif cmp == "lt":
                        if rounded_truth < rounded_pred:
                            count += 1
                    elif cmp == "ge":
                        if rounded_truth >= rounded_pred:
                            count += 1
                    elif cmp == "gt":
                        if rounded_truth > rounded_pred:
                            count += 1
                    else:
                        raise ValueError(f"Unsupported comparison operator: {cmp}")
                
                return count / len(y)

            def mape(y, y_pred):
                """Calculate mean absolute percentage error"""
                y_safe = np.where(np.abs(y) < AssertionMinerConfig.FITNESS_PRECISION, AssertionMinerConfig.FITNESS_PRECISION, y)
                return np.mean(np.abs(y_safe - y_pred) / np.abs(y_safe))

            # Get fitness weights based on comparison operator
            mape_weight, cmpr_weight = AssertionMinerConfig.get_fitness_weights(cmp)
            return mape_weight * mape(y, y_pred) + cmpr_weight * (1 - cmpr(y, y_pred))
        
        return make_fitness(function=fitness, greater_is_better=False, wrap=True)
    
    def _train_with_early_stopping(self, gp, X, y, target_col, early_stopping_config):
        """Training with early stopping"""
        was_early_stopped = False
        semantic_checker = SemanticChecker(list(X.columns))
        
        past_best_fitness = float('inf')
        no_improvement_count = 0
        generations = 0
        
        logging.info(f"Early stopping strategy: stop after {early_stopping_config['early_stopping_patience']} consecutive batches without improvement, minimum improvement: {early_stopping_config['early_stopping_min_delta']}")
        
        while generations < early_stopping_config['max_generations']:
            logging.info(f"Starting batch {generations // early_stopping_config['early_stopping_batch_generations']} training, will train to generation {generations}")
            gp.set_params(generations=generations + 1)
            gp.fit(X, y.values.ravel())
            selection_summary = self._apply_semantic_selection(gp, semantic_checker, target_col, generations)
            cur_best_fitness = selection_summary.get("best_adjusted_fitness", float("inf"))
            logging.info(f"Batch {generations // early_stopping_config['early_stopping_batch_generations']} training completed, current best fitness: {cur_best_fitness:.9f}")
            generations += early_stopping_config['early_stopping_batch_generations']
        
            if cur_best_fitness <= gp.stopping_criteria:
                break
        
            if cur_best_fitness < past_best_fitness - early_stopping_config['early_stopping_min_delta']:
                past_best_fitness = cur_best_fitness
                no_improvement_count = 0
            else:
                no_improvement_count += 1
                logging.info(f"Current fitness not improved, consecutive no improvement count: {no_improvement_count}")

            if no_improvement_count >= early_stopping_config['early_stopping_patience']:
                was_early_stopped = True
                logging.info(f"Early stopping triggered: {no_improvement_count} consecutive batches without improvement")
                break
        
        training_result = {
            'was_early_stopped': was_early_stopped,
            'generations_completed': generations
        }
        
        return training_result

    def _apply_semantic_selection(self, gp, semantic_checker: SemanticChecker, target_col: str, generation: int) -> dict:
        latest_population = gp._programs[-1] if hasattr(gp, "_programs") and gp._programs else []
        programs = [program for program in latest_population if program is not None and program.fitness_ is not None]
        if not programs:
            return {"generation": generation, "best_adjusted_fitness": float("inf")}

        records: list[dict] = []
        valid_fitnesses: list[float] = []
        invalid_fitnesses: list[float] = []

        for program in programs:
            original_fitness = float(program.fitness_)
            semantic_result = semantic_checker.check_program(program, target_col)
            record = {
                "generation": generation,
                "program": str(program),
                "original_fitness": original_fitness,
                "semantic_valid": semantic_result.valid,
                "semantic_type": semantic_result.semantic_type,
                "semantic_reason": semantic_result.reason,
                "semantic_adjusted_fitness": original_fitness,
            }
            records.append(record)
            self.semantic_selection_records[id(program)] = record
            if semantic_result.valid:
                valid_fitnesses.append(original_fitness)
            else:
                invalid_fitnesses.append(original_fitness)

        offset = 0.0
        if valid_fitnesses and invalid_fitnesses:
            valid_max = max(valid_fitnesses)
            invalid_min = min(invalid_fitnesses)
            if invalid_min <= valid_max:
                offset = valid_max - invalid_min + max(1e-12, abs(valid_max) * 1e-12)

            for program, record in zip(programs, records):
                if not record["semantic_valid"]:
                    adjusted_fitness = record["original_fitness"] + offset
                    program.fitness_ = adjusted_fitness
                    record["semantic_adjusted_fitness"] = adjusted_fitness

        gp._program = min(programs, key=lambda program: program.fitness_)
        best_record = self.semantic_selection_records.get(id(gp._program), {})
        summary = {
            "generation": generation,
            "semantic_valid_count": len(valid_fitnesses),
            "semantic_invalid_count": len(invalid_fitnesses),
            "fitness_offset": offset,
            "best_program": str(gp._program),
            "best_semantic_valid": best_record.get("semantic_valid"),
            "best_original_fitness": best_record.get("original_fitness"),
            "best_adjusted_fitness": best_record.get("semantic_adjusted_fitness", float(gp._program.fitness_)),
        }
        logging.info(
            "Semantic-aware selection: valid=%s invalid=%s offset=%.9g best_valid=%s",
            summary["semantic_valid_count"],
            summary["semantic_invalid_count"],
            summary["fitness_offset"],
            summary["best_semantic_valid"],
        )
        return summary
    
    def _format_training_result(self, gp, training_result, target_col):
        """Format training results"""
        was_early_stopped = training_result['was_early_stopped']
        generations = training_result['generations_completed']
        best_assertion = gp._program if hasattr(gp, '_program') else None
        best_record = self.semantic_selection_records.get(id(best_assertion), {}) if best_assertion else {}
        best_fitness = best_record.get("original_fitness")
        if best_fitness is None and hasattr(gp, '_program') and gp._program:
            best_fitness = gp._program.fitness_
                        
        result = {
            'best_assertion': best_assertion,
            'best_fitness': best_fitness,
            'was_early_stopped': was_early_stopped,
            'generations_completed': generations,
            'semantic_selection': self._format_selected_semantic_info(best_record),
        }
                
        status = "stopped early" if was_early_stopped else "completed normally"
        logging.info(f"Target '{target_col}' constraint discovery {status}")
        logging.info(f"Generations completed: {generations}")
                
        return result

    @staticmethod
    def _format_selected_semantic_info(best_record: dict) -> dict:
        return {
            "semantic_valid": best_record.get("semantic_valid"),
            "semantic_type": best_record.get("semantic_type"),
            "semantic_reason": best_record.get("semantic_reason"),
        }
