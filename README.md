# Traceloop

A lightweight Python developer tool for local AI agent execution recording and timeline replaying.

**Traceloop** wraps any AI agent workflow to automatically capture every step, context handoff, tool call, and failure, allowing you to browse and replay failed runs locally.

## Features
- **Pure Python:** Minimal dependencies (`flask`, `click`, `rich`).
- **Framework Agnostic:** Works with arbitrary Python code, LangChain, raw OpenAI calls, or custom agents.
- **Local JSON Storage:** Runs are saved as plain JSON to `~/.traceloop/runs/`. No cloud accounts or API keys required.
- **CLI & Web UI:** Browse run timelines in your terminal or via a local web dashboard.
- **Replay Capability:** Step-level checkpoints allow you to inject saved inputs and re-run localized failures.

## Installation

Traceloop is published on PyPI. You can install it globally via pip:

```bash
pip install traceloop-local
```

Alternatively, you can clone the [GitHub Repository](https://github.com/Rishab87/traceloop) and install from source:

```bash
git clone https://github.com/Rishab87/traceloop.git
cd traceloop
pip install -e .
```

## Quick Start

### 1. Instrument your Agent

Use the `@tracer.run()` and `tracer.step()` decorators to wrap your logic.

```python
from traceloop import tracer
import time

@tracer.run()
def my_agent(query):
    with tracer.step("web_search", query=query) as step:
        # Simulate work
        time.sleep(0.3)
        results = ["Result 1", "Result 2"]
        step["outputs"] = {"results": results}
        
    with tracer.step("summarize", context=results) as step:
        # Simulate a crash
        raise Exception("API Rate Limit Exceeded")

if __name__ == "__main__":
    try:
        my_agent("What is the capital of France?")
    except Exception:
        pass
```

### 2. View Runs (CLI)

Listrecent runs:
```bash
traceloop list
```

Show a specific run timeline (with execution durations and error tracebacks):
```bash
traceloop show <run_id>
```

### 3. Web Dashboard

Launch the local timeline viewer UI:
```bash
traceloop ui
```
Then navigate to `http://localhost:5000` to interactively expand steps and view full input/output JSON payloads.

### 4. Replay from Checkpoint

In a real environment, you can re-inject inputs to debug a specific failing step:
```bash
traceloop replay <run_id> --from-step 2
```
