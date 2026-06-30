# -*- coding: utf-8 -*-
"""
odoo-cli entrypoint
===================
Entrypoint utama untuk TUI, CLI, dan MCP mode odoo-cli.
"""
import sys
import argparse
from rich.console import Console
from rich.table import Table

from core.connector import OdooConnector
from core.introspection import OdooIntrospection
from core.executor import OdooExecutor

console = Console()

def main():
    """Fungsi entrypoint utama."""
    parser = argparse.ArgumentParser(description="Odoo CLI & TUI")
    parser.add_argument("--profile", type=str, help="Profile to use from profiles.json", default=None)
    parser.add_argument("command", nargs="?", default="tui", help="Command to run: 'tui', 'mcp', or other CLI commands")
    
    args = parser.parse_args()
    
    try:
        console.print(f"[bold blue]Connecting to Odoo using profile:[/bold blue] [green]{args.profile or 'default'}[/green]")
        connector = OdooConnector(profile_name=args.profile)
        introspection = OdooIntrospection(connector)
        executor = OdooExecutor(connector)
        
        console.print(f"[bold green]Successfully connected![/bold green] (UID: {connector.uid})")
        
        if args.command == "tui":
            console.print("[bold yellow]TUI mode is not fully implemented yet. Please use CLI commands.[/bold yellow]")
        elif args.command == "mcp":
            console.print("[bold yellow]MCP mode is not fully implemented yet.[/bold yellow]")
        else:
            console.print(f"[bold red]Unknown command: {args.command}[/bold red]")
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
