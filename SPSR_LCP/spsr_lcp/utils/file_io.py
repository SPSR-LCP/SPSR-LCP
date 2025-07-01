"""File I/O utilities."""

def read_source_code(file_path):
    """Read source code from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_json_file(data, file_path):
    """Write JSON file."""
    import json
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_json_file(file_path):
    """Load JSON file."""
    import json
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def ensure_directory(path):
    """Ensure directory exists."""
    import os
    os.makedirs(path, exist_ok=True)

def find_source_files(root_path):
    """Find source files."""
    import os
    files = []
    for root, dirs, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith(('.c', '.cpp', '.h', '.hpp')):
                files.append(os.path.join(root, filename))
    return files
