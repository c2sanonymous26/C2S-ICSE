class BaseConfig:
    """Base configuration class - Contains configurations shared by all modules"""
    
    # Formula validation precision
    VALIDATION_PRECISION = 1e-9
    
    # Constraint reliability threshold (unified threshold)
    CONSTRAINT_RELIABILITY_THRESHOLD = 0.995
    
    # Timeout for processing a single target (seconds)
    TARGET_PROCESSING_TIMEOUT_SECONDS = 1 * 60 * 60

class DataProcessorConfig:
    """Data processor configuration"""
    
    # Field classification definition
    ID_FIELDS = ["id"]  # ID fields, removed after loading
    METADATA_FIELDS = ["carid", "grpid"]  # Metadata fields
    TIMESTAMP_FIELDS = ["timestamp"]  # Timestamp fields, kept but not used as features
    NUMERICAL_FIELDS = ["speed", "latitude", "longitude", "direction"]  # Numerical fields
    
    # Assertion mining phase: only use numerical fields for constraint discovery
    ASRTM_FEATURES = TIMESTAMP_FIELDS + NUMERICAL_FIELDS  # All features used in assertion mining phase
    ASRTM_TARGETS = TIMESTAMP_FIELDS + NUMERICAL_FIELDS  # Available target columns in assertion mining phase
    ASRTM_EXCLUDED = ID_FIELDS + METADATA_FIELDS  # Fields excluded in assertion mining phase
    
    # Precondition mining phase: need to include METADATA_FIELDS for precondition mining
    PREDM_FEATURES = METADATA_FIELDS + TIMESTAMP_FIELDS + NUMERICAL_FIELDS
    
    # Binning configuration
    SINGLE_N_BINS = 20
    CARID_JOIN_N_BINS = 10
    CARID_DIFF_N_BINS = 5
    
class AssertionMinerConfig:
    """Symbolic regressor configuration"""
    
    # Training control
    STOPPING_CRITERIA = 0.005
    
    # Assertion mining parameters
    TOURNAMENT_SIZE = 20
    CONST_RANGE = (-65535, 65535)
    FUNCTION_SET = (
        'add', 'sub', 'mul', 'div', 
        'sqrt', 'log', 'abs', 'neg', 
        'max', 'min', 
        'sin', 'cos', 'tan'
    )
    PARSIMONY_COEFFICIENT = 1e-4
    MAX_SAMPLES = 1.0
    LOW_MEMORY = True
    
    VERBOSE = 1
    
    # Fitness configuration
    FITNESS_PRECISION = BaseConfig.VALIDATION_PRECISION
    
    # Early stopping configuration
    EARLY_STOPPING_MIN_DELTA = 1e-6
    EARLY_STOPPING_BATCH_GENERATIONS = 1
    
    # Mode-specific configuration
    MODE_CONFIGS = {
        'single': {
            'MAX_GENERATIONS': 100,
            'POPULATION_SIZE': 2000,
            'N_JOBS': -1,
            'EARLY_STOPPING_PATIENCE': 20
        },
        'carid_join': {
            'MAX_GENERATIONS': 100,  
            'POPULATION_SIZE': 1000,  
            'N_JOBS': -1,           
            'EARLY_STOPPING_PATIENCE': 20
        },
        'carid_diff': {
            'MAX_GENERATIONS': 100,
            'POPULATION_SIZE': 500,
            'N_JOBS': -1,
            'EARLY_STOPPING_PATIENCE': 20
        },
        'pairwise': {
            'MAX_GENERATIONS': 100,
            'POPULATION_SIZE': 200,
            'N_JOBS': -1,
            'EARLY_STOPPING_PATIENCE': 20
        }
    }
        
    @classmethod
    def get_mode_config(cls, mode: str):
        if mode not in cls.MODE_CONFIGS:
            raise ValueError(f"Unsupported mode: {mode}, supported modes: {list(cls.MODE_CONFIGS.keys())}")
        return cls.MODE_CONFIGS[mode]
    
    @classmethod
    def get_fitness_weights(cls, cmp: str):
        """Get fitness weights based on comparison operator
        
        Args:
            cmp: Comparison operator ('eq', 'le', 'lt', 'ge', 'gt')
            
        Returns:
            tuple: (mape_weight, cmpr_weight)
        """
        if cmp == 'eq':
            return (0.2, 0.8)
        else:
            return (0.05, 0.95)
    
    @classmethod
    def get_config(cls, mode: str):
        """Get complete symbolic regression configuration"""
        mode_config = cls.get_mode_config(mode)
        
        return {
            'POPULATION_SIZE': mode_config['POPULATION_SIZE'],
            'GENERATIONS': cls.EARLY_STOPPING_BATCH_GENERATIONS,
            'TOURNAMENT_SIZE': cls.TOURNAMENT_SIZE,
            'STOPPING_CRITERIA': cls.STOPPING_CRITERIA,
            'CONST_RANGE': cls.CONST_RANGE,
            'FUNCTION_SET': cls.FUNCTION_SET,
            'PARSIMONY_COEFFICIENT': cls.PARSIMONY_COEFFICIENT,
            'MAX_SAMPLES': cls.MAX_SAMPLES,
            'LOW_MEMORY': cls.LOW_MEMORY,
            'N_JOBS': mode_config['N_JOBS'],
            'VERBOSE': cls.VERBOSE,
            'WARM_START': True,
            'MAX_GENERATIONS': mode_config['MAX_GENERATIONS'],
            'EARLY_STOPPING_PATIENCE': mode_config['EARLY_STOPPING_PATIENCE'],
            'EARLY_STOPPING_MIN_DELTA': cls.EARLY_STOPPING_MIN_DELTA,
            'EARLY_STOPPING_BATCH_GENERATIONS': cls.EARLY_STOPPING_BATCH_GENERATIONS,
        }

class PreconditionMinerConfig:
    """Association rule miner configuration"""
    
    MIN_CONFIDENCE = 0.8
    
    MODE_CONFIGS = {
        'single': {
            "MIN_SUPPORT": 0.1,
            "MAX_PRECONDITION_LENGTH": 5
        },
        "carid_join": {
            "MIN_SUPPORT": 0.1,
            "MAX_PRECONDITION_LENGTH": 4
        },
        "carid_diff": {
            "MIN_SUPPORT": 0.1,
            "MAX_PRECONDITION_LENGTH": 3
        }
    }
    
    @classmethod
    def get_mode_config(cls, mode: str):
        if mode not in cls.MODE_CONFIGS:
            raise ValueError(f"Unsupported mode: {mode}, supported modes: {list(cls.MODE_CONFIGS.keys())}")
        return cls.MODE_CONFIGS[mode]
    
    @classmethod
    def get_config(cls, mode: str):
        """Get complete precondition mining configuration"""
        mode_config = cls.get_mode_config(mode)
        
        return {
            'MIN_CONFIDENCE': cls.MIN_CONFIDENCE,
            'MIN_SUPPORT': mode_config['MIN_SUPPORT'],
            'MAX_PRECONDITION_LENGTH': mode_config['MAX_PRECONDITION_LENGTH']
        }
    

    
