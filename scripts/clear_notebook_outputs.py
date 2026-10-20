"""Clear saved notebook outputs before publishing notebooks that may contain raw tweets."""
from pathlib import Path
import json
import shutil
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "notebooks")
if not root.exists():
    raise SystemExit(f"Notebook directory not found: {root}")

files = list(root.rglob("*.ipynb"))
if not files:
    print(f"No notebooks found under {root}")
    raise SystemExit(0)

backup_dir = root.parent / (root.name + "_backup_before_clear_outputs")
backup_dir.mkdir(exist_ok=True)
for path in files:
    backup = backup_dir / path.name
    shutil.copy2(path, backup)
    nb = json.loads(path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Cleared output: {path}")
print(f"Backup copies saved in: {backup_dir}")
