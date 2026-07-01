from pathlib import Path
import tomli
from typing import Any, Generator

from .. import INPUT_DIR, CONTEXT_DEFINITIONS_FILE_NAME

def load_data_field_types(scenario: str) -> dict[str, str | int | float]:
    dataset_file_path = INPUT_DIR / scenario / CONTEXT_DEFINITIONS_FILE_NAME            
    if not dataset_file_path.exists() or not dataset_file_path.is_file():
        raise FileNotFoundError(f"Dataset file {dataset_file_path} not found")
        
    type_map = {}
    with open(dataset_file_path, 'rb') as f:
        try:
            fields = tomli.load(f)['context_definitions']['fields']
            for field_name, field_info in fields.items():
                field_type = field_info.get('type')
                if field_type == 'int':
                    type_map[field_name] = int
                elif field_type == 'float':
                    type_map[field_name] = float
                elif field_type == 'str':
                    type_map[field_name] = str
                else:
                    raise ValueError(f"Unsupported field type: {field_type}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Load field type map error: {str(e)}")  
    return type_map

def get_data_size(data_file_path: Path) -> int:
    with open(data_file_path, 'r') as data_file:
        return sum(1 for _ in data_file) - 1

def generate_data_chunks(file_path: Path, chunk_size: int, field_type_map: dict[str, Any]) -> Generator[list[dict[str, Any]], None, None]:

    with open(file_path, 'r') as file:
        header = file.readline().strip().split(",")
        chunk = []
        start_index = 0
        avaliable_chunk_sizes = range(1, chunk_size + 1, 1)
        target_chunk_size = avaliable_chunk_sizes[start_index]
        
        for line in file:
            values = line.strip().split(",")
            data = {
                k: field_type_map[k](v)
                for k, v in zip(header, values)
            }
            chunk.append(data)
            
            if len(chunk) >= target_chunk_size:
                yield chunk
                chunk = []
                start_index = (start_index + 1) % len(avaliable_chunk_sizes)
                target_chunk_size = avaliable_chunk_sizes[start_index]
        
        if chunk:
            yield chunk