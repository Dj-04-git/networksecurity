from dataclasses import dataclass

@dataclass
class DataIngestionartifact:
    trained_file_path : str
    test_file_path : str