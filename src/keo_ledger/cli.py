from __future__ import annotations

import csv
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from keo_ledger.parse import scan_dir, tickets_to_csv_rows
from keo_ledger.settle import settle_ticket, winrate

app = typer.Typer(help="Football tip ledger from filenames")
console = Console()


@app.command()
def parse(
    folder: Path = typer.Argument(..., exists=True, file_okay=False),
    out: Path = typer.Option(Path("tickets.csv"), "--out", "-o"),
) -> None:
    """Scan folder for ticket filenames → CSV."""
    tickets = scan_dir(folder)
    rows = tickets_to_csv_rows(tickets)
    if not rows:
        console.print("[yellow]No tickets matched naming convention.[/yellow]")
        raise typer.Exit(1)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    console.print(f"[green]Wrote {len(rows)} tickets → {out}[/green]")


@app.command()
def settle(
    csv_path: Path = typer.Option(Path("tickets.csv"), "--csv"),
    scores: Path = typer.Option(..., "--scores", help="JSON map match→'2-1'"),
) -> None:
    """Apply scores JSON and write results back into CSV."""
    score_map = json.loads(scores.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    for row in rows:
        key = row.get("match") or ""
        sc = score_map.get(key) or score_map.get(key.replace("-", " vs "))
        if not sc:
            continue
        row["score"] = sc
        row["result"] = settle_ticket(row["market"], sc)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    console.print(f"[green]Settled → {csv_path}[/green]")


@app.command()
def report(csv_path: Path = typer.Argument(Path("tickets.csv"))) -> None:
    """Winrate by tipster."""
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    by: dict[str, list[str]] = {}
    for r in rows:
        by.setdefault(r["tipster"], []).append(r.get("result") or "PENDING")
    table = Table(title="Tipster winrate")
    table.add_column("Tipster")
    table.add_column("n")
    table.add_column("WR")
    for tip, res in sorted(by.items()):
        wr = winrate(res)
        table.add_row(
            tip,
            str(wr["n"]),
            f"{wr['winrate']*100:.1f}%" if wr["winrate"] is not None else "—",
        )
    console.print(table)


if __name__ == "__main__":
    app()
