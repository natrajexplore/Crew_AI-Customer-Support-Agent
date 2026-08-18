import sys
from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"

sys.path.insert(0, str(SRC_DIR))

subprocess.run(
    [sys.executable, "-m", "pytest", str(TESTS_DIR), "-v"],
    check=False,
)

