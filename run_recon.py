"""
Точка входа для запуска NetRecon Cyberpunk Terminal.
Использование:
  python run_recon.py 127.0.0.1
  python run_recon.py scanme.nmap.org
"""

import sys
from recon.ui.terminal_app import render_cyberpunk_dashboard

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    render_cyberpunk_dashboard(host)

