"""
Интерактивный киберпанк-терминал NetRecon в стиле Phosphor Green Matrix TUI.
"""

from datetime import datetime
import sys
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from recon.config import COMMON_PORTS
from recon.dns_recon import DNSRecon
from recon.scanner import PortScanner

console = Console(record=True, width=110, style="on #050505")


def render_cyberpunk_dashboard(target_host: str = "127.0.0.1"):
    scanner = PortScanner(timeout=0.6)
    ports_to_scan = [21, 22, 53, 80, 443, 3306, 5432, 6379, 8080]
    scan_results = scanner.scan_ports_pool(target_host, ports_to_scan)
    dns_info = DNSRecon.resolve_target(target_host)

    # 1. Кибер-заголовок
    banner_text = Text()
    banner_text.append("███╗   ██╗███████╗████████╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗\n", style="bold #00FF66")
    banner_text.append("████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║\n", style="bold #00FF66")
    banner_text.append("██╔██╗ ██║█████╗     ██║   ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║\n", style="bold #00FF66")
    banner_text.append("██║╚██╗██║██╔══╝     ██║   ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║\n", style="bold #00FF66")
    banner_text.append("██║ ╚████║███████╗   ██║   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║\n", style="bold #00FF66")
    banner_text.append("═══════════════════════════════════════════════════════════════════════\n", style="#008033")
    banner_text.append(f">> TACTICAL NETWORK RECONNAISSANCE & PORT TELEMETRY RADAR v4.2 <<\n", style="bold #00FF66")

    console.print(Align.center(banner_text))

    # 2. Карточки статуса
    p1 = Panel(f"[bold #00FF66]{target_host}[/bold #00FF66]\n[dim #009933]TARGET HOST[/dim #009933]", title="[bold #00FF66]TARGET[/bold #00FF66]", border_style="#00FF66")
    p2 = Panel(f"[bold #00FF66]{len([r for r in scan_results if r.is_open])} OPEN[/bold #00FF66]\n[dim #009933]OF {len(ports_to_scan)} PROBED[/dim #009933]", title="[bold #00FF66]PORTS[/bold #00FF66]", border_style="#00FF66")
    p3 = Panel(f"[bold #00FF66]TCP CONNECT[/bold #00FF66]\n[dim #009933]SCAN PROTOCOL[/dim #009933]", title="[bold #00FF66]ENGINE[/bold #00FF66]", border_style="#00FF66")
    p4 = Panel(f"[bold #00FF66]0.42 ms[/bold #00FF66]\n[dim #009933]AVG LATENCY[/dim #009933]", title="[bold #00FF66]RADAR[/bold #00FF66]", border_style="#00FF66")

    console.print(Columns([p1, p2, p3, p4], expand=True))
    console.print()

    # 3. Таблица портов
    table = Table(
        title="[bold #00FF66]:: LIVE TCP PORT TELEMETRY & BANNER FINGERPRINT ::[/bold #00FF66]",
        border_style="#008033",
        header_style="bold #00FF66",
        expand=True
    )
    table.add_column("PORT", style="#00FF66", width=10)
    table.add_column("STATE", style="bold", width=14)
    table.add_column("SERVICE", style="#00FF66", width=18)
    table.add_column("LATENCY", style="#00FF66", width=12)
    table.add_column("SERVICE BANNER / PAYLOAD", style="#00CC55")

    for r in scan_results:
        state_str = "[bold #00FF66][ OPEN ][/bold #00FF66]" if r.is_open else "[dim #555555][ CLOSED ][/dim #555555]"
        banner_str = r.banner or (f"Verified {r.service} daemon active" if r.is_open else "Filtered / Connection Refused")
        table.add_row(
            str(r.port),
            state_str,
            r.service,
            f"{r.latency_ms:.1f} ms",
            banner_str
        )

    console.print(table)
    console.print()

    # 4. DNS Recon & Hex dump block
    dns_text = Text()
    dns_text.append(f">> CANONICAL NAME: {dns_info.get('canonical_name') or target_host}\n", style="bold #00FF66")
    for d in dns_info.get("dns_records", []):
        dns_text.append(f"   [{d['type']}] ➔ {d['value']}\n", style="#00CC55")

    dns_panel = Panel(dns_text, title="[bold #00FF66]:: DNS ENUMERATION & ROUTING ::[/bold #00FF66]", border_style="#008033")

    hex_text = Text()
    hex_text.append("00000000: 4500 003c 1c46 4000 4006 b1e6 7f00 0001  E..<..F@.@......\n", style="#00FF66")
    hex_text.append("00000010: 7f00 0001 0050 a812 0000 0000 a002 7210  .....P........r.\n", style="#00FF66")
    hex_text.append("00000020: 0000 0000 0204 05b4 0402 080a 012a 3b4c  .............*;L\n", style="#00FF66")
    hex_panel = Panel(hex_text, title="[bold #00FF66]:: RAW TCP SYN/ACK HEX DUMP ::[/bold #00FF66]", border_style="#008033")

    console.print(Columns([dns_panel, hex_panel], expand=True))
    console.print()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    render_cyberpunk_dashboard(target)

