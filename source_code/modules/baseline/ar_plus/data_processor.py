# -*- coding: utf-8 -*-
"""
Data processing module

Extends original data processing functionality, adds data preprocessing needed for association rule mining
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Tuple
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
import warnings

from .config import DataProcessorConfig

class DataProcessor(ABC):
    """Data processor abstract base class"""
    
    # ===== Main public methods =====
    
    def load_and_preprocess_data(self, data_file_path) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Complete data loading and preprocessing workflow
        
        Args:
            data_file_path: Data file path
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: (asrtm_df, predm_df)
            - asrtm_df: For assertion mining
            - predm_df: For precondition mining
        """
        df = pd.read_csv(data_file_path)
        
        # Only drop ID fields, keep all other fields
        columns_to_drop = [col for col in DataProcessorConfig.ID_FIELDS if col in df.columns]
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
        
        # Check for missing values
        na_counts = df.isnull().sum()
        total_na = na_counts.sum()
        assert total_na == 0, f"Found {total_na} missing values in data: {na_counts[na_counts > 0].to_dict()}"
        
        df = df.reset_index(drop=True)
        
        # Apply mode-specific data processing
        processed_df = self._construct_df_by_mode(df)
        
        # Generate two specialized DataFrames
        asrtm_df, predm_df = self._create_specialized_dataframes(processed_df)
        
        return asrtm_df, predm_df
    
    def prepare_asrtm_data(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features and target variable for assertion mining phase (common implementation)"""
        # Simple feature-target separation: input df is already asrtm_df, contains only needed fields
        X = df.drop(columns=[target_col])
        y = df[target_col]
        return X, y
    
    # ===== Precondition mining related methods =====
    
    def prepare_predm_data(self, predm_df: pd.DataFrame, fit_data: pd.Series) -> pd.DataFrame:
        """Prepare data for precondition mining phase (binning + one-hot encoding)
        
        Args:
            predm_df: Data frame dedicated for precondition mining
            fit_data: Fit result from assertion mining
        """
        logging.info("Starting to prepare data for precondition mining phase")
        
        # 1. Add fit column to precondition mining data
        full_data = predm_df.copy()
        full_data['fit'] = fit_data
        
        # 2. Bin assertion mining fields
        discretized_data = self._discretize_asrtm_features(full_data)

        with pd.option_context('display.max_columns', None, 'display.max_colwidth', None, 'display.width', None):
            logging.info(discretized_data.head(0))

        # 3. Convert directly to one-hot format
        predm_data = self._convert_to_onehot(discretized_data)
        
        with pd.option_context('display.max_columns', None, 'display.max_colwidth', None, 'display.width', None):
            logging.info(predm_data.head(0))


        logging.info(f"Precondition mining phase data preparation completed, shape: {predm_data.shape}")
        return predm_data
    
    def _discretize_asrtm_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Bin assertion mining fields"""
        discretized_df = df.copy()
        
        # Get assertion mining field list (exclude fit column)
        asrtm_features = self._get_asrtm_features()
        target_cols = [col for col in asrtm_features if col in df.columns and col != 'fit']
        
        logging.info(f"Binning {len(target_cols)} assertion mining fields: {target_cols}")
                
        for col in target_cols:
            try:
                # Suppress warnings about bins with too small width
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', category=UserWarning, 
                                        message='Bins whose width are too small.*are removed')
                    # Use sklearn's KBinsDiscretizer for binning
                    discretizer = KBinsDiscretizer(
                        n_bins=self._get_number_of_bins(),
                        encode='ordinal', 
                        # strategy='quantile'  # Equal frequency binning
                        strategy='uniform'  # Equal width binning
                    )
                    
                    # Bin and generate new categorical columns
                    discretized_values = discretizer.fit_transform(df[[col]]).flatten()
                    
                    bin_edges = discretizer.bin_edges_[0]
                    logging.info(f'{col} bin_edges: {bin_edges}')
                
                # Create meaningful labels (using boundary values)
                for bin_idx in range(self._get_number_of_bins()):
                    # Get current bin's boundary values
                    left_edge = bin_edges[bin_idx]
                    right_edge = bin_edges[bin_idx + 1]
                    
                    # Format boundary values (keep 9 decimal places)
                    left_str = f"{left_edge:.9f}".rstrip('.')
                    right_str = f"{right_edge:.9f}".rstrip('.')
                    
                    # Generate column name: col_bin_leftBoundary_rightBoundary
                    bin_col_name = f"{col}_bin_{left_str}_{right_str}"
                    discretized_df[bin_col_name] = (discretized_values == bin_idx).astype(int)
                
                # Delete original continuous variable
                discretized_df = discretized_df.drop(columns=[col])
                
            except Exception as e:
                logging.warning(f"Binning failed for column '{col}': {e}, keeping original value")
        
        return discretized_df
    
    def _convert_to_onehot(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert DataFrame directly to one-hot format, handling categorical and numerical variables"""
        onehot_df = pd.DataFrame()
        
        # Get assertion mining field list to identify binned columns
        asrtm_features = self._get_asrtm_features()
        for col in df.columns:
            if col == 'fit':
                # fit column special handling: convert to fit_0 and fit_1
                onehot_df['fit_0'] = (df[col] == 0).astype(bool)
                onehot_df['fit_1'] = (df[col] == 1).astype(bool)
            
            elif self._is_asrtm_bin_column(col, asrtm_features):
                # Assertion mining field binning result (0/1 values): convert directly to bool
                onehot_df[col] = (df[col] == 1).astype(bool)
            
            elif col == 'carid' or col == 'grpid':
                continue
            
            elif col == 'carid_1':
                # carid_join mode: only process grpid comparison features (carid always equal, no discrimination)
                self._convert_carid_join_metadata_fields_to_onehot(df, onehot_df)
                
            elif col in ['carid_2', 'grpid_1', 'grpid_2']:
                # carid_join mode: these fields were already processed when handling carid_1, skip
                continue
            
            else:
                # Categorical columns: use pandas get_dummies for one-hot encoding
                dummies = pd.get_dummies(df[col], prefix=col, dtype=bool)
                onehot_df = pd.concat([onehot_df, dummies], axis=1)
        
        logging.info(f"Direct one-hot encoding completed, number of features: {len(onehot_df.columns)}")
        return onehot_df
    
    def _convert_carid_join_metadata_fields_to_onehot(self, df: pd.DataFrame, onehot_df: pd.DataFrame):
        """Process metadata field comparisons in carid_join mode
        
        Note: In carid_join mode, carid is always equal (paired within same carid), so no carid_eq feature is generated
        Only generate grpid comparison features, which have discrimination
        """        
        # Only process grpid comparison (carid is always equal in carid_join mode, no discrimination)
        if 'grpid_1' in df.columns and 'grpid_2' in df.columns:
            onehot_df['grpid_eq'] = (df['grpid_1'] == df['grpid_2']).astype(bool)
            onehot_df['grpid_lt'] = (df['grpid_1'] < df['grpid_2']).astype(bool)
            onehot_df['grpid_gt'] = (df['grpid_1'] > df['grpid_2']).astype(bool)
    
    def _is_asrtm_bin_column(self, col_name: str, asrtm_features: List[str]) -> bool:
        """Determine if column name is a binning result of assertion mining field"""
        for feature in asrtm_features:
            if col_name.startswith(f"{feature}_bin_"):
                # Check if suffix is in boundary value format (number_number)
                suffix = col_name[len(f"{feature}_bin_"):]
                # Boundary value format: number_number (may contain decimal point)
                parts = suffix.split('_')
                assert len(parts) == 2, f"Binned column format error: {col_name}"
                assert float(parts[0]) < float(parts[1]), f"Binned column format error: {col_name}"
                return True
        return False
    
    # ===== Internal utility methods =====
    
    def _create_specialized_dataframes(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Create specialized DataFrames
        
        Args:
            df: Processed complete data
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: (asrtm_df, predm_df)
        """
        # Assertion mining DataFrame: only contains numerical fields, for constraint discovery
        asrtm_features = self._get_asrtm_features()
        asrtm_df = df[asrtm_features].copy()
        logging.info(f"Assertion mining DataFrame fields: {asrtm_features}")
        logging.info(f"Assertion mining DataFrame shape: {asrtm_df.shape}")
        
        # Precondition mining DataFrame: includes context fields, for precondition mining
        predm_features = self._get_predm_features()
        predm_df = df[predm_features].copy()
        logging.info(f"Precondition mining DataFrame fields: {predm_features}")
        logging.info(f"Precondition mining DataFrame shape: {predm_df.shape}")
        
        return asrtm_df, predm_df
    
    # ===== Abstract method definitions =====
    
    @abstractmethod
    def _construct_df_by_mode(self, df: pd.DataFrame) -> pd.DataFrame:
        """Mode-specific data construction"""
        pass
    
    @abstractmethod
    def get_asrtm_targets(self) -> List[str]:
        """Get available target columns for assertion mining phase"""
        pass
    
    @abstractmethod
    def _get_asrtm_features(self) -> List[str]:
        """Get field list for assertion mining phase"""
        pass
    
    @abstractmethod
    def _get_predm_features(self) -> List[str]:
        """Get field list for precondition mining phase"""
        pass
    
    @abstractmethod
    def get_mode_name(self) -> str:
        """Get mode name"""
        pass
    
    @abstractmethod
    def _get_number_of_bins(self) -> int:
        pass


class SingleRecordProcessor(DataProcessor):
    """Single record processor"""
    
    def _construct_df_by_mode(self, df: pd.DataFrame) -> pd.DataFrame:
        """Single record mode: return original data directly"""
        return df.copy()
    
    def get_asrtm_targets(self) -> List[str]:
        """Get available target columns for assertion mining phase in Single mode"""
        return [col for col in DataProcessorConfig.ASRTM_TARGETS]
    
    def _get_asrtm_features(self) -> List[str]:
        """Get field list for assertion mining phase in Single mode"""
        return [col for col in DataProcessorConfig.ASRTM_FEATURES]
    
    def _get_predm_features(self) -> List[str]:
        """Get field list for precondition mining phase in Single mode"""
        return [col for col in DataProcessorConfig.PREDM_FEATURES if col]
    
    def get_mode_name(self) -> str:
        return "single"
    
    def _get_number_of_bins(self) -> int:
        return DataProcessorConfig.SINGLE_N_BINS


class PairwiseRecordProcessor(DataProcessor):
    """Two-record processor (Cartesian product)"""
    
    def _construct_df_by_mode(self, df: pd.DataFrame) -> pd.DataFrame:
        """Two-record mode: create Cartesian product"""
        
        def _create_cartesian_product() -> pd.DataFrame:
            """Create Cartesian product of dataset"""
            logging.info(f"Starting to create Cartesian product dataset, original data shape: {df.shape}")
            # Add _1 suffix to first record features and keep original index
            df1 = df.copy().reset_index()
            df1 = df1.rename(columns={'index': 'global_orig_idx_1'})
            df1.columns = [f"{col}_1" if col != 'global_orig_idx_1' else col for col in df1.columns]
            
            # Add _2 suffix to second record features and keep original index
            df2 = df.copy().reset_index()
            df2 = df2.rename(columns={'index': 'global_orig_idx_2'})
            df2.columns = [f"{col}_2" if col != 'global_orig_idx_2' else col for col in df2.columns]
            
            # Create Cartesian product
            df1['key'] = 1
            df2['key'] = 1
            
            # Perform Cartesian product operation
            pairwise_df = pd.merge(df1, df2, on='key', how='outer').drop(columns=['key'])
            
            # Ensure output order consistency: sort by global original index
            pairwise_df = pairwise_df.sort_values(['global_orig_idx_1', 'global_orig_idx_2']).reset_index(drop=True)
            
            # Remove temporary index columns
            pairwise_df = pairwise_df.drop(columns=['global_orig_idx_1', 'global_orig_idx_2'])
            
            logging.info(f"Cartesian product completed, new data shape: {pairwise_df.shape}")
            return pairwise_df
        
        return _create_cartesian_product()
    
    def _get_asrtm_features(self) -> List[str]:
        """Get field list for assertion mining phase in Pairwise mode (handle _1 and _2 suffixes)"""
        asrtm_features = []
        for feature in DataProcessorConfig.ASRTM_FEATURES:
            for suffix in ["_1", "_2"]:
                col_name = f"{feature}{suffix}"
                asrtm_features.append(col_name)
        return asrtm_features

    def _get_predm_features(self) -> List[str]:
        """Get field list for precondition mining phase in Pairwise mode (handle _1 and _2 suffixes)"""
        predm_features = []
        for feature in DataProcessorConfig.PREDM_FEATURES:
            for suffix in ["_1", "_2"]:
                col_name = f"{feature}{suffix}"
                predm_features.append(col_name)
        return predm_features
    
    def get_asrtm_targets(self) -> List[str]:
        """Get available target columns for assertion mining phase in Pairwise mode"""
        available_targets = []
        
        # Assertion mining phase: check numerical fields with _1 and _2 suffixes
        for field in DataProcessorConfig.ASRTM_TARGETS:
            for suffix in ["_1", "_2"]:
                col_name = f"{field}{suffix}"
                available_targets.append(col_name)
        return available_targets
    
    def get_mode_name(self) -> str:
        return "pairwise"
    
    def _get_number_of_bins(self) -> int:
        raise NotImplementedError("Pairwise mode does not support binning")
        #return DataProcessorConfig.PAIRWISE_N_BINS


class CaridJoinRecordProcessor(DataProcessor):
    """Carid-based data processor (join data with same carid)"""
    
    def _construct_df_by_mode(self, df: pd.DataFrame) -> pd.DataFrame:
        """carid_join mode: only pair records with same carid"""
        
        def _create_carid_join() -> pd.DataFrame:
            """Create data pairing based on carid"""
            logging.info(f"Starting to create carid-based data pairing, original data shape: {df.shape}")
            
            if 'carid' not in df.columns:
                raise ValueError("carid_join mode requires 'carid' column in data")
            
            paired_dfs = []
            # Group by carid (no need to force sort, will sort by original index at end)
            carid_groups = df.groupby('carid', sort=False)
            total_pairs = 0
            
            for carid, group_df in carid_groups:
                group_size = len(group_df)
                
                if group_size < 2:
                    # carid with only one record cannot be paired, skip
                    logging.debug(f"carid {carid} has only {group_size} record, skipping")
                    continue
                
                # Create pairwise pairing for this carid group, keep global original index to ensure order
                df1 = group_df.copy().reset_index()
                df1 = df1.rename(columns={'index': 'global_orig_idx_1'})
                df1.columns = [f"{col}_1" if col != 'global_orig_idx_1' else col for col in df1.columns]
                
                df2 = group_df.copy().reset_index()
                df2 = df2.rename(columns={'index': 'global_orig_idx_2'})
                df2.columns = [f"{col}_2" if col != 'global_orig_idx_2' else col for col in df2.columns]
                
                # Use Cartesian product for pairwise pairing
                df1['key'] = 1
                df2['key'] = 1
                
                group_pairs = pd.merge(df1, df2, on='key', how='outer').drop(columns=['key'])
                
                # Ensure intra-group order consistency
                group_pairs = group_pairs.sort_values(['global_orig_idx_1', 'global_orig_idx_2']).reset_index(drop=True)
                
                # Keep global index columns, remove uniformly at end
                
                # Optional: exclude self-pairing (same record paired with itself)
                # Can add filtering logic here as needed
                
                paired_dfs.append(group_pairs)
                group_pairs_count = len(group_pairs)
                total_pairs += group_pairs_count
                
                logging.debug(f"carid {carid}: {group_size} records → {group_pairs_count} pairs")
            
            if not paired_dfs:
                logging.warning("No carid groups can be paired")
                return pd.DataFrame()
            
            # Merge pairing results from all carid groups
            result_df = pd.concat(paired_dfs, ignore_index=True)
            
            # Final sorting ensures global order consistency (sort by global original index, consistent with pairwise)
            if 'global_orig_idx_1' in result_df.columns and 'global_orig_idx_2' in result_df.columns:
                result_df = result_df.sort_values(['global_orig_idx_1', 'global_orig_idx_2']).reset_index(drop=True)
                # Remove temporary global index columns
                result_df = result_df.drop(columns=['global_orig_idx_1', 'global_orig_idx_2'])
            
            logging.info(f"carid join completed, new data shape: {result_df.shape}")
            logging.info(f"Processed {len(carid_groups)} carid groups, generated {total_pairs} pairs")
            
            return result_df
        
        return _create_carid_join()
    
    def _get_asrtm_features(self) -> List[str]:
        """Get field list for assertion mining phase in CaridJoin mode (handle _1 and _2 suffixes)"""
        asrtm_features = []
        for feature in DataProcessorConfig.ASRTM_FEATURES:
            for suffix in ["_1", "_2"]:
                col_name = f"{feature}{suffix}"
                asrtm_features.append(col_name)
        return asrtm_features

    def _get_predm_features(self) -> List[str]:
        """Get field list for precondition mining phase in CaridJoin mode (handle _1 and _2 suffixes)"""
        predm_features = []
        for feature in DataProcessorConfig.PREDM_FEATURES:
            for suffix in ["_1", "_2"]:
                col_name = f"{feature}{suffix}"
                predm_features.append(col_name)
        return predm_features
    
    def get_asrtm_targets(self) -> List[str]:
        """Get available target columns for assertion mining phase in CaridJoin mode"""
        available_targets = []
        # Assertion mining phase: check numerical fields with _1 and _2 suffixes
        for field in DataProcessorConfig.ASRTM_TARGETS:
            for suffix in ["_1", "_2"]:
                col_name = f"{field}{suffix}"
                available_targets.append(col_name)
        return available_targets
    
    def get_mode_name(self) -> str:
        return "carid_join"
    
    def _get_number_of_bins(self) -> int:
        return DataProcessorConfig.CARID_JOIN_N_BINS


class CaridDiffRecordProcessor(DataProcessor):
    """Carid-based data processor (join data with different carid)"""
    
    def _construct_df_by_mode(self, df: pd.DataFrame) -> pd.DataFrame:
        """carid_diff mode: only pair records with different carid"""
        
        def _create_carid_diff() -> pd.DataFrame:
            """Create data pairing based on different carid"""
            logging.info(f"Starting to create different carid data pairing, original data shape: {df.shape}")
            
            if 'carid' not in df.columns:
                raise ValueError("carid_diff mode requires 'carid' column in data")
            
            # For first record features, add _1 suffix and keep original index
            df1 = df.copy().reset_index()
            df1 = df1.rename(columns={'index': 'global_orig_idx_1'})
            df1.columns = [f"{col}_1" if col != 'global_orig_idx_1' else col for col in df1.columns]
            
            # For second record features, add _2 suffix and keep original index
            df2 = df.copy().reset_index()
            df2 = df2.rename(columns={'index': 'global_orig_idx_2'})
            df2.columns = [f"{col}_2" if col != 'global_orig_idx_2' else col for col in df2.columns]
            
            # Create Cartesian product
            df1['key'] = 1
            df2['key'] = 1
            
            # Perform Cartesian product operation
            diff_df = pd.merge(df1, df2, on='key', how='outer').drop(columns=['key'])
            
            # Filter to keep only pairs with different carid
            diff_df = diff_df[diff_df['carid_1'] != diff_df['carid_2']]
            
            # Ensure output order consistency: sort by global original index
            diff_df = diff_df.sort_values(['global_orig_idx_1', 'global_orig_idx_2']).reset_index(drop=True)
            
            # Remove temporary index columns
            diff_df = diff_df.drop(columns=['global_orig_idx_1', 'global_orig_idx_2'])
            
            logging.info(f"Different carid pairing completed, new data shape: {diff_df.shape}")
            
            return diff_df
        
        return _create_carid_diff()
    
    def _get_asrtm_features(self) -> List[str]:
        """Get field list for assertion mining phase in CaridDiff mode (handle _1 and _2 suffixes)"""
        asrtm_features = []
        for feature in DataProcessorConfig.ASRTM_FEATURES:
            for suffix in ["_1", "_2"]:
                col_name = f"{feature}{suffix}"
                asrtm_features.append(col_name)
        return asrtm_features

    def _get_predm_features(self) -> List[str]:
        """Get field list for precondition mining phase in CaridDiff mode (handle _1 and _2 suffixes)"""
        predm_features = []
        for feature in DataProcessorConfig.PREDM_FEATURES:
            for suffix in ["_1", "_2"]:
                col_name = f"{feature}{suffix}"
                predm_features.append(col_name)
        return predm_features
    
    def get_asrtm_targets(self) -> List[str]:
        """Get available target columns for assertion mining phase in CaridDiff mode"""
        available_targets = []
        # Assertion mining phase: check numerical fields with _1 and _2 suffixes
        for field in DataProcessorConfig.ASRTM_TARGETS:
            for suffix in ["_1", "_2"]:
                col_name = f"{field}{suffix}"
                available_targets.append(col_name)
        return available_targets
    
    def get_mode_name(self) -> str:
        return "carid_diff"
    
    def _get_number_of_bins(self) -> int:
        return DataProcessorConfig.CARID_DIFF_N_BINS


# ===== Factory function =====

def create_data_processor(mode: str) -> DataProcessor:
    """Data processor factory function"""
    if mode == "single":
        return SingleRecordProcessor()
    elif mode == "pairwise":
        return PairwiseRecordProcessor()
    elif mode == "carid_join":
        return CaridJoinRecordProcessor()
    elif mode == "carid_diff":
        return CaridDiffRecordProcessor()
    else:
        raise ValueError(f"Unsupported mode: {mode}, supported modes: 'single', 'pairwise', 'carid_join', 'carid_diff'") 
