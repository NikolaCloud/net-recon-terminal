"""
Тесты сканера портов и модуля DNS.
"""

from recon.config import COMMON_PORTS
from recon.dns_recon import DNSRecon
from recon.scanner import PortScanner


def test_port_service_mapping():
    assert COMMON_PORTS[80] == "HTTP"
    assert COMMON_PORTS[443] == "HTTPS"
    assert COMMON_PORTS[22] == "SSH"


def test_scanner_returns_result_structure():
    scanner = PortScanner(timeout=0.1)
    res = scanner.scan_port("127.0.0.1", 80)
    assert res.port == 80
    assert res.service == "HTTP"
    assert isinstance(res.is_open, bool)
    assert res.latency_ms >= 0


def test_dns_recon_fallback():
    info = DNSRecon.resolve_target("internal-test.corp")
    assert "ip_addresses" in info
    assert len(info["dns_records"]) > 0

