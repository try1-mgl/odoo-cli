# -*- coding: utf-8 -*-
"""
odoo-cli entrypoint
===================
Entrypoint utama untuk TUI, CLI, dan MCP mode odoo-cli.
"""

import argparse
import json
import sys

from rich.console import Console

from core.connector import OdooConnector
from core.executor import OdooExecutor

console = Console()


def run_cli_payload(executor: OdooExecutor, payload: dict):
    """Parses and executes a JSON payload using the executor."""
    action = payload.get("action")
    model = payload.get("model")

    if not action or not model:
        raise ValueError("Payload must contain 'action' and 'model' keys.")

    if action == "search":
        result = executor.search(
            model,
            payload.get("domain", []),
            offset=payload.get("offset", 0),
            limit=payload.get("limit", 0),
        )
    elif action == "read":
        result = executor.read(model, payload.get("ids", []), payload.get("fields"))
    elif action == "create":
        result = executor.create(model, payload.get("values", {}))
    elif action == "write":
        result = executor.write(model, payload.get("ids", []), payload.get("values", {}))
    elif action == "delete":
        result = executor.unlink(model, payload.get("ids", []))
    elif action == "execute":
        result = executor.execute(
            model, payload.get("method"), *payload.get("args", []), **payload.get("kwargs", {})
        )
    else:
        raise ValueError(f"Unknown action: {action}")

    # Output the result as pure JSON for script interoperability
    print(json.dumps({"status": "success", "data": result}))


def main():
    """Fungsi entrypoint utama."""
    parser = argparse.ArgumentParser(description="Odoo CLI & TUI")
    parser.add_argument(
        "--profile", type=str, help="Profile to use from profiles.json", default=None
    )
    parser.add_argument("--mcp", action="store_true", help="Run in MCP Server mode")
    parser.add_argument(
        "command", nargs="?", default="tui", help="Command to run: 'tui', or a JSON payload string"
    )

    args = parser.parse_args()

    try:
        # No rich stdout in MCP to prevent stdio transport corruption
        if args.mcp:
            # TODO: Initialize MCP server
            sys.stderr.write("Starting MCP mode...\n")
            sys.exit(0)

        is_json_payload = args.command.strip().startswith("{")

        # Only print connection status if we are in TUI mode
        if not is_json_payload:
            prof = args.profile or "default"
            console.print(f"[bold blue]Connecting to Odoo:[/bold blue] [green]{prof}[/green]")

        connector = OdooConnector(profile_name=args.profile)
        # introspection = OdooIntrospection(connector) # TODO: Initialize when needed
        executor = OdooExecutor(connector)

        if not is_json_payload:
            console.print(
                f"[bold green]Successfully connected![/bold green] (UID: {connector.uid})"
            )

        if is_json_payload:
            payload = json.loads(args.command)
            run_cli_payload(executor, payload)
        elif args.command == "tui":
            console.print("[bold yellow]TUI mode is not fully implemented yet.[/bold yellow]")
        else:
            console.print(f"[bold red]Unknown command: {args.command}[/bold red]")

    except Exception as e:
        if args.command.strip().startswith("{"):
            print(json.dumps({"status": "error", "message": str(e)}))
        else:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
