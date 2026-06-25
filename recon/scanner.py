"""
Многопоточный TCP-сканер сетевых портов и замера сетевой задержки.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
import socket
import time
from typing import Dict, List, Optional
from recon.config import COMMON_PORTS


@dataclass
class PortScanResult:
    port: int
    service: str
    is_open: bool
    latency_ms: float
    banner: Optional[str] = None

    def to_dict(self):
        return asdict(self)


class PortScanner:
    def __init__(self, timeout: float = 0.8, max_threads: int = 20):
        self.timeout = timeout
        self.max_threads = max_threads

    def scan_port(self, host: str, port: int) -> PortScanResult:
        service_name = COMMON_PORTS.get(port, "Unknown")
        start = time.perf_counter()
        is_open = False
        banner = None

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                res = s.connect_ex((host, port))
                latency = round((time.perf_counter() - start) * 1000, 2)
                if res == 0:
                    is_open = True
                    # Попытка быстрого считывания баннера
                    try:
                        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n" if port in [80, 8080, 443] else b"\r\n")
                        raw = s.recv(256).decode("utf-8", errors="ignore").strip()
                        if raw:
                            banner = raw.split("\n")[0][:60]
                    except Exception:
                        banner = None
        except Exception:
            latency = round((time.perf_counter() - start) * 1000, 2)
            is_open = False

        return PortScanResult(
            port=port,
            service=service_name,
            is_open=is_open,
            latency_ms=latency,
            banner=banner
        )

    def scan_ports_pool(self, host: str, ports: List[int]) -> List[PortScanResult]:
        results = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_port = {executor.submit(self.scan_port, host, p): p for p in ports}
            for future in as_completed(future_to_port):
                results.append(future.result())

        results.sort(key=lambda x: x.port)
        return results

