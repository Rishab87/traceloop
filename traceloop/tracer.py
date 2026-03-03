import time
import uuid
import traceback
from functools import wraps
from contextlib import contextmanager
from typing import Any, Dict, Optional

from .storage import save_run

class Tracer:
    def __init__(self):
        self.current_run: Optional[Dict[str, Any]] = None
        self.step_counter = 0

    def _save_run(self):
        if self.current_run:
            save_run(self.current_run)

    def run(self):
        """Decorator to wrap an entire agent execution run."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.current_run = {
                    "run_id": str(uuid.uuid4())[:8],
                    "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "status": "running",
                    "steps": []
                }
                self.step_counter = 0
                
                try:
                    result = func(*args, **kwargs)
                    self.current_run["status"] = "success"
                    return result
                except Exception as e:
                    self.current_run["status"] = "failed"
                    raise e
                finally:
                    self._save_run()
                    self.current_run = None
            return wrapper
        return decorator

    @contextmanager
    def step(self, name: str, **inputs):
        """Context manager to wrap an individual agent step or tool call."""
        if not self.current_run:
            # If not wrapped in @tracer.run(), just execute normally without tracing
            yield
            return

        self.step_counter += 1
        step_id = self.step_counter
        
        step_data = {
            "step_id": step_id,
            "name": name,
            "inputs": inputs,
            "started_at": time.time(),
            "status": "running"
        }
        
        self.current_run["steps"].append(step_data)
        
        # Save intermediate state in case of hard crash
        self._save_run()

        try:
            # Yield so the caller can execute their inner logic
            # We catch outputs by allowing them to optionally modify a dict or return? 
            # Context managers don't easily capture returns directly unless they yield a tracker.
            # So we yield the step_data dict to let them manually add "outputs" if they want.
            yield step_data
            
            step_data["status"] = "success"
        except Exception as e:
            step_data["status"] = "failed"
            step_data["error"] = f"{type(e).__name__}: {str(e)}"
            step_data["traceback"] = "".join(traceback.format_tb(e.__traceback__))
            raise e
        finally:
            end_time = time.time()
            step_data["duration_ms"] = int((end_time - step_data["started_at"]) * 1000)
            del step_data["started_at"]  # Clean up temporary field
            self._save_run()

# Global singleton
tracer = Tracer()
