import os

def print_tree(start_path, ignore_dirs=None, ignore_files=None, prefix=""):
    if ignore_dirs is None:
        ignore_dirs = {"venv", "__pycache__", ".git"}
    if ignore_files is None:
        ignore_files = {".DS_Store"}

    items = sorted(os.listdir(start_path))
    items = [item for item in items if item not in ignore_dirs and item not in ignore_files]

    for i, item in enumerate(items):
        path = os.path.join(start_path, item)
        connector = "└── " if i == len(items) - 1 else "├── "
        print(prefix + connector + item)

        if os.path.isdir(path):
            extension = "    " if i == len(items) - 1 else "│   "
            print_tree(path, ignore_dirs, ignore_files, prefix + extension)

if __name__ == "__main__":
    project_path = "."  
    print_tree(project_path)