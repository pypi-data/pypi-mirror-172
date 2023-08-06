import os
import sys
from pathlib import Path


class DirectoryExecContext:
    def __init__(self, dir: Path):
        self.dir = dir.resolve().absolute()
        self.cwd = None

    def __enter__(self):
        sys.path = [str(self.dir)] + sys.path
        self.cwd = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.path = sys.path[1:]
        os.chdir(self.cwd)
