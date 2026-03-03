import os
import json
import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from .storage import TRACELOOP_DIR, list_runs

console = Console()

@click.group()
def cli():
    """Traceloop: Local AI Agent Execution Recorder & Replayer."""
    pass

@cli.command()
def list():
    """List recent agent runs."""
    runs = list_runs()
    if not runs:
        console.print("[yellow]No runs found in ~/.traceloop/runs/[/yellow]")
        return
    
    table = Table(title="Recent Traceloop Runs")
    table.add_column("Run ID", style="cyan")
    table.add_column("Started At", style="magenta")
    table.add_column("Steps", justify="right")
    table.add_column("Status", style="bold")

    for run in runs[:10]:
        status_color = "green" if run.get("status") == "success" else ("red" if run.get("status") == "failed" else "yellow")
        stats = run.get("status", "unknown")
        steps = str(len(run.get("steps", [])))
        table.add_row(
            run.get("run_id", "N/A"),
            run.get("started_at", "N/A"),
            steps,
            f"[{status_color}]{stats}[/{status_color}]"
        )
    
    console.print(table)

@cli.command()
@click.argument("run_id")
def show(run_id):
    """Show details for a specific run timeline."""
    file_path = os.path.join(TRACELOOP_DIR, f"{run_id}.json")
    if not os.path.exists(file_path):
        console.print(f"[red]Error: Run {run_id} not found.[/red]")
        return
        
    with open(file_path, "r") as f:
        data = json.load(f)
        
    console.print(f"\n[bold cyan]Run ID:[/bold cyan] {data['run_id']}")
    console.print(f"[bold cyan]Started:[/bold cyan]  {data['started_at']}")
    status_color = "green" if data["status"] == "success" else "red"
    console.print(f"[bold cyan]Status:[/bold cyan]   [{status_color}]{data['status']}[/{status_color}]\n")
    
    for step in data.get("steps", []):
        icon = "[green]✓[/green]" if step.get("status") == "success" else ("[red]✗[/red]" if step.get("status") == "failed" else "[yellow]-[/yellow]")
        console.print(f"{icon} [bold]Step {step['step_id']}: {step['name']}[/bold] ({step.get('duration_ms', 0)}ms)")
        if step.get("status") == "failed":
            console.print(f"   [red]Error:[/red] {step.get('error')}")

@cli.command()
def ui():
    """Launch the local web dashboard."""
    from .ui import run_server
    console.print("[bold green]Starting local Traceloop UI on port 4999...[/bold green]")
    run_server()

@cli.command()
@click.argument("run_id")
@click.option("--from-step", type=int, help="Step ID to replay from.", required=True)
def replay(run_id, from_step):
    """Replay a specific run from a checkpoint."""
    from .storage import get_run
    run = get_run(run_id)
    if not run:
        console.print(f"[red]Error: Run {run_id} not found.[/red]")
        return
    
    step = next((s for s in run.get("steps", []) if s["step_id"] == from_step), None)
    if not step:
        console.print(f"[red]Error: Step {from_step} not found in run {run_id}.[/red]")
        return
        
    console.print(f"[bold yellow]Replaying {run_id} from Step {from_step} ({step['name']})...[/bold yellow]")
    console.print("Injecting previous inputs:")
    rprint(step.get("inputs", {}))
    
    # Normally, we'd hook this into the user's framework. For now, this is a mock.
    console.print("\n[bold green]Replay capability stubbed. In a full implementation, this drops you into a debugger or mock execution loop.[/bold green]")

if __name__ == "__main__":
    cli()
