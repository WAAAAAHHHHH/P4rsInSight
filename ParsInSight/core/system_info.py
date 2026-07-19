"""
P4rsInSight - System Information
Detects CPU, RAM, GPU, disk, OS, Wi-Fi, Bluetooth, installed packages, etc.
On non-Linux platforms (Windows/macOS) returns graceful mock data so the
UI can be developed and tested cross-platform.
"""

from __future__ import annotations

import platform
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional

import psutil

from core.logger import get_logger

log = get_logger("system_info")

IS_LINUX = sys.platform.startswith("linux")


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CpuInfo:
    brand: str = "Unknown CPU"
    cores_physical: int = 1
    cores_logical: int = 1
    frequency_mhz: float = 0.0
    usage_percent: float = 0.0


@dataclass
class RamInfo:
    total_gb: float = 0.0
    available_gb: float = 0.0
    used_gb: float = 0.0
    percent: float = 0.0


@dataclass
class GpuInfo:
    brand: str = "Unknown GPU"
    vendor: str = "unknown"   # "nvidia" | "amd" | "intel" | "unknown"
    driver_installed: bool = False
    recommended_driver: Optional[str] = None


@dataclass
class DiskInfo:
    device: str = "/"
    total_gb: float = 0.0
    used_gb: float = 0.0
    free_gb: float = 0.0
    percent: float = 0.0


@dataclass
class OsInfo:
    name: str = "Unknown"
    version: str = ""
    kernel: str = ""
    arch: str = ""


@dataclass
class NetworkInfo:
    wifi_present: bool = False
    wifi_connected: bool = False
    bluetooth_present: bool = False


@dataclass
class SystemReport:
    """Aggregated system health report."""
    cpu: CpuInfo = field(default_factory=CpuInfo)
    ram: RamInfo = field(default_factory=RamInfo)
    gpu: GpuInfo = field(default_factory=GpuInfo)
    disks: list[DiskInfo] = field(default_factory=list)
    os: OsInfo = field(default_factory=OsInfo)
    network: NetworkInfo = field(default_factory=NetworkInfo)
    # Package-level checks
    flatpak_installed: bool = False
    multimedia_codecs_installed: bool = False
    updates_available: int = 0
    installed_packages: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(cmd: list[str], timeout: int = 10) -> str:
    """Run a subprocess and return stdout, or '' on failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        log.debug("Command %s failed: %s", cmd, exc)
        return ""


# ---------------------------------------------------------------------------
# Detection functions
# ---------------------------------------------------------------------------

def detect_cpu() -> CpuInfo:
    try:
        freq = psutil.cpu_freq()
        freq_mhz = freq.current if freq else 0.0
        brand = "Unknown CPU"
        if IS_LINUX:
            brand = _run(["grep", "-m1", "model name", "/proc/cpuinfo"])
            if ":" in brand:
                brand = brand.split(":", 1)[1].strip()
        else:
            import platform as _platform
            brand = _platform.processor() or "Unknown CPU"
        return CpuInfo(
            brand=brand or "Unknown CPU",
            cores_physical=psutil.cpu_count(logical=False) or 1,
            cores_logical=psutil.cpu_count(logical=True) or 1,
            frequency_mhz=freq_mhz,
            usage_percent=psutil.cpu_percent(interval=0.5),
        )
    except Exception as exc:
        log.error("CPU detection failed: %s", exc)
        return CpuInfo()


def detect_ram() -> RamInfo:
    try:
        vm = psutil.virtual_memory()
        return RamInfo(
            total_gb=round(vm.total / 1e9, 2),
            available_gb=round(vm.available / 1e9, 2),
            used_gb=round(vm.used / 1e9, 2),
            percent=vm.percent,
        )
    except Exception as exc:
        log.error("RAM detection failed: %s", exc)
        return RamInfo()


def detect_gpu() -> GpuInfo:
    """Detect primary GPU vendor and driver status."""
    if not IS_LINUX:
        return GpuInfo(brand="Mock GPU (Windows)", vendor="unknown")

    # Try lspci for GPU info
    lspci_out = _run(["lspci"])
    gpu_line = ""
    for line in lspci_out.splitlines():
        lower = line.lower()
        if "vga" in lower or "3d" in lower or "display" in lower:
            gpu_line = line
            break

    vendor = "unknown"
    brand = gpu_line or "Unknown GPU"
    recommended_driver = None
    driver_installed = False

    if "nvidia" in gpu_line.lower():
        vendor = "nvidia"
        # Check if nvidia module is loaded
        lsmod = _run(["lsmod"])
        driver_installed = "nvidia" in lsmod.lower()
        if not driver_installed:
            recommended_driver = "nvidia-driver"
    elif "amd" in gpu_line.lower() or "radeon" in gpu_line.lower():
        vendor = "amd"
        driver_installed = True  # amdgpu is built into kernel
    elif "intel" in gpu_line.lower():
        vendor = "intel"
        driver_installed = True  # i915 is built into kernel

    return GpuInfo(
        brand=brand,
        vendor=vendor,
        driver_installed=driver_installed,
        recommended_driver=recommended_driver,
    )


def detect_disks() -> list[DiskInfo]:
    disks = []
    try:
        for part in psutil.disk_partitions(all=False):
            if not part.mountpoint:
                continue
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append(DiskInfo(
                    device=part.mountpoint,
                    total_gb=round(usage.total / 1e9, 2),
                    used_gb=round(usage.used / 1e9, 2),
                    free_gb=round(usage.free / 1e9, 2),
                    percent=usage.percent,
                ))
            except (PermissionError, OSError):
                pass
    except Exception as exc:
        log.error("Disk detection failed: %s", exc)
    return disks or [DiskInfo()]


def detect_os() -> OsInfo:
    return OsInfo(
        name=platform.system(),
        version=platform.version(),
        kernel=platform.release(),
        arch=platform.machine(),
    )


def detect_network() -> NetworkInfo:
    wifi = False
    bluetooth = False
    wifi_connected = False

    if IS_LINUX:
        # Wi-Fi detection via /sys
        import os
        wireless_path = "/proc/net/wireless"
        if os.path.exists(wireless_path):
            content = _run(["cat", wireless_path])
            wifi = len(content.splitlines()) > 2
        # Check Bluetooth
        bt_out = _run(["rfkill", "list"])
        bluetooth = "bluetooth" in bt_out.lower()
        # Connectivity
        nm = _run(["nmcli", "-t", "-f", "TYPE,STATE", "device"])
        for line in nm.splitlines():
            if "wifi" in line.lower() and "connected" in line.lower():
                wifi_connected = True
    else:
        wifi = True
        wifi_connected = True
        bluetooth = True

    return NetworkInfo(
        wifi_present=wifi,
        wifi_connected=wifi_connected,
        bluetooth_present=bluetooth,
    )


def check_flatpak() -> bool:
    if not IS_LINUX:
        return False
    out = _run(["which", "flatpak"])
    return bool(out)


def check_multimedia_codecs() -> bool:
    if not IS_LINUX:
        return False
    # A rough heuristic — check for a common codec package
    out = _run(["dpkg", "-s", "ubuntu-restricted-extras"])
    return "Status: install ok installed" in out


def count_available_updates() -> int:
    if not IS_LINUX:
        return 0
    out = _run(["apt", "list", "--upgradable", "-q", "2>/dev/null"])
    lines = [l for l in out.splitlines() if "/" in l]
    return len(lines)


def get_installed_packages() -> list[str]:
    if not IS_LINUX:
        return []
    out = _run(["dpkg", "--get-selections"])
    packages = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == "install":
            packages.append(parts[0])
    return packages


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def collect_system_report() -> SystemReport:
    """
    Gather all system information and return a SystemReport.
    Safe to call from a QThread worker.
    """
    log.info("Collecting system report...")
    report = SystemReport(
        cpu=detect_cpu(),
        ram=detect_ram(),
        gpu=detect_gpu(),
        disks=detect_disks(),
        os=detect_os(),
        network=detect_network(),
        flatpak_installed=check_flatpak(),
        multimedia_codecs_installed=check_multimedia_codecs(),
        updates_available=count_available_updates(),
        installed_packages=get_installed_packages(),
    )
    log.info("System report collected successfully.")
    return report
