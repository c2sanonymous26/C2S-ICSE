from dataclasses import dataclass, field, asdict
import json
from pathlib import Path
import time
from contextlib import contextmanager


@dataclass
class IasStatistics:
    """Phase 1: Intent and semantics generation statistics"""
    time_cost: float = 0.0  # Time cost in seconds
    semantic_duplicate_count: int = 0  # Number of semantic duplicate detections triggered
    llm_call_count: int = 0  # Number of LLM calls in this phase
    
    # Internal timer
    _start_time: float = field(default=0.0, repr=False, compare=False)
    
    @contextmanager
    def time_ias(self):
        """Context manager: automatically record intent and semantics generation time"""
        self._start_time = time.time()
        try:
            yield self
        finally:
            self.time_cost = time.time() - self._start_time


@dataclass
class SasStatistics:
    """Phase 2: Structure and signatures statistics"""
    time_cost: float = 0.0  # Time cost in seconds
    syntax_error_count: int = 0  # Number of syntax errors
    semantic_error_count: int = 0  # Number of semantic errors
    llm_call_count: int = 0  # Number of LLM calls in this phase
    
    # Internal timer
    _start_time: float = field(default=0.0, repr=False, compare=False)
    
    @contextmanager
    def time_phase(self):
        """Context manager: accumulate time across multiple uses (for LLM retries)"""
        self._start_time = time.time()
        try:
            yield self
        finally:
            self.time_cost += time.time() - self._start_time  # += to accumulate!


@dataclass
class ImplStatistics:
    """Phase 3: Implementation statistics"""
    time_cost: float = 0.0  # Time cost in seconds
    syntax_error_count: int = 0  # Number of syntax errors
    consistency_error_count: int = 0  # Number of consistency errors
    unit_error_count: int = 0  # Number of unit errors
    llm_call_count: int = 0  # Number of LLM calls in this phase
    
    # Internal timer
    _start_time: float = field(default=0.0, repr=False, compare=False)
    
    @contextmanager
    def time_phase(self):
        """Context manager: accumulate time across multiple uses (for LLM retries)"""
        self._start_time = time.time()
        try:
            yield self
        finally:
            self.time_cost += time.time() - self._start_time  # += to accumulate!


@dataclass
class RewriteStatistics:
    """Statistics for one rewrite attempt (structure + implementation)"""
    attempt_number: int  # 1-based attempt number
    result: str  # "cannot_implement" or "success"
    time_cost: float = 0.0  # Total time for this rewrite attempt (sas + impl)
    
    sas_stats: SasStatistics = field(default_factory=SasStatistics)
    impl_stats: ImplStatistics = field(default_factory=ImplStatistics)
    
    # Internal timer
    _start_time: float = field(default=0.0, repr=False, compare=False)
    
    @contextmanager
    def time_rewrite(self):
        """Context manager: automatically record rewrite time"""
        self._start_time = time.time()
        try:
            yield self
        finally:
            self.time_cost = time.time() - self._start_time


@dataclass
class ReimagineStatistics:
    """Statistics for one reimagine attempt (intent and semantics → template)"""
    attempt_number: int  # 1-based attempt number
    result: str  # "failed", "duplicate", or "success"
    duplicate_with: str | None = None  # Name of duplicate template (if result="duplicate")
    time_cost: float = 0.0  # Total time for this reimagine attempt (ias + all rewrites)
    
    # Statistics split into intent-and-semantics and rewrites
    ias: IasStatistics = field(default_factory=IasStatistics)
    rewrites: list[RewriteStatistics] = field(default_factory=list)  # May have multiple rewrite attempts
    
    # Internal timer
    _start_time: float = field(default=0.0, repr=False, compare=False)
    
    @contextmanager
    def time_reimagine(self):
        """Context manager: automatically record reimagine time"""
        self._start_time = time.time()
        try:
            yield self
        finally:
            self.time_cost = time.time() - self._start_time


@dataclass
class TemplateStatistics:
    """Complete statistics for a single template"""
    success: bool = False  # Whether the template was successfully generated
    total_time: float = 0.0  # Total time cost in seconds
    reimagine_rollback_count: int = 0  # Number of reimagine rollbacks (semantics → template)
    
    # All reimagine attempts (including the final successful one if success=True)
    reimagine_attempts: list[ReimagineStatistics] = field(default_factory=list)
    
    # Internal timer (will not be serialized)
    _start_time: float = field(default=0.0, repr=False, compare=False)
    
    @contextmanager
    def time_template(self):
        """Context manager: automatically record total template generation time"""
        self._start_time = time.time()
        try:
            yield self
        finally:
            self.total_time = time.time() - self._start_time
    
    def to_dict(self):
        """Convert to dictionary, excluding internal fields"""
        data = asdict(self)
        # Remove internal fields (recursively)
        self._remove_internal_fields(data)
        return data
    
    def _remove_internal_fields(self, data):
        """Recursively remove all _start_time fields"""
        if isinstance(data, dict):
            data.pop('_start_time', None)
            for value in data.values():
                self._remove_internal_fields(value)
        elif isinstance(data, list):
            for item in data:
                self._remove_internal_fields(item)
    
    def save_to_file(self, file_path: Path):
        """Save to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


@dataclass
class ConverterStatistics:
    """Statistics for conversion process"""
    success: bool = False  # Whether the conversion was successful
    total_time: float = 0.0  # Total conversion time in seconds
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
    
    def save_to_file(self, file_path: Path):
        """Save to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
