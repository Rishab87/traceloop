import json
import os
from typing import List, Dict, Any

TRACELOOP_DIR = os.path.expanduser("~/.traceloop/runs")

def ensure_dir():
    os.makedirs(TRACELOOP_DIR, exist_ok=True)

def save_run(run_data: Dict[str, Any]):
    """Save a run dictionary to a JSON file."""
    if not run_data or "run_id" not in run_data:
        return
    ensure_dir()
    file_path = os.path.join(TRACELOOP_DIR, f"{run_data['run_id']}.json")
    with open(file_path, "w") as f:
        json.dump(run_data, f, indent=2)

def list_runs() -> List[Dict[str, Any]]:
    """Get a list of all runs, sorted by newest first."""
    runs = []
    if not os.path.exists(TRACELOOP_DIR):
        return runs
    for f in os.listdir(TRACELOOP_DIR):
        if f.endswith(".json"):
            with open(os.path.join(TRACELOOP_DIR, f), "r") as file:
                try:
                    data = json.load(file)
                    runs.append(data)
                except Exception:
                    pass
    return sorted(runs, key=lambda x: x.get("started_at", ""), reverse=True)

def get_run(run_id: str) -> Dict[str, Any]:
    """Get a specific run by ID."""
    file_path = os.path.join(TRACELOOP_DIR, f"{run_id}.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        return json.load(f)
