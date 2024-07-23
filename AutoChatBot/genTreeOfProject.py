import os
import fnmatch

class DirectoryTreeGenerator:
    def __init__(self, root_dir, ignore_patterns=None):
        if ignore_patterns is None:
            ignore_patterns = ['venv', 'wheel_dist', 'raw_context', '__pycache__', 'deb_dist', 'build', 'dist']
        self.root_dir = root_dir
        self.ignore_patterns = set(ignore_patterns)

    def is_ignored(self, path):
        relative_path = os.path.relpath(path, self.root_dir)
        return any(fnmatch.fnmatch(relative_path, pattern) for pattern in self.ignore_patterns)

    def generate_tree(self):
        tree = []
        for root, dirs, files in os.walk(self.root_dir, topdown=True):
            # Create full paths for directories for comparison
            full_dirs = [os.path.join(root, d) for d in dirs]
            dirs[:] = [d for d in dirs if not self.is_ignored(os.path.join(root, d))]
            
            level = root.replace(self.root_dir, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if not self.is_ignored(os.path.join(root, f)):
                    tree.append(f"{subindent}{f}")
        return '\n'.join(tree)

    def print_tree(self):
        print(self.generate_tree())
