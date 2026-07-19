"""
P4rsInSight - Package Manager Service
Wraps apt / flatpak / dpkg operations via QThread workers.
Never executes commands without explicit user confirmation.
All operations emit signals for UI progress updates.
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from typing import Optional

from PySide6.QtCore import QObject, QThread, Signal

from core.logger import get_logger

log = get_logger("package_manager")

IS_LINUX = sys.platform.startswith("linux")


# ---------------------------------------------------------------------------
# Worker base
# ---------------------------------------------------------------------------

class CommandWorker(QThread):
    """
    Generic QThread worker that runs a shell command and streams output.

    Signals
    -------
    output_line(str)       — emitted for each line of stdout/stderr
    progress(int, int)     — emitted with (current, total) where meaningful
    finished(bool, str)    — emitted with (success, final_message)
    command_preview(str)   — emitted immediately with the command string
    """

    output_line = Signal(str)
    progress = Signal(int, int)
    finished = Signal(bool, str)
    command_preview = Signal(str)

    def __init__(self, cmd: list[str], parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.cmd = cmd
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True
        self.terminate()

    def run(self) -> None:  # noqa: D102
        cmd_str = shlex.join(self.cmd)
        self.command_preview.emit(cmd_str)
        log.info("Running: %s", cmd_str)

        if not IS_LINUX:
            # Simulate output on non-Linux for UI development
            self.output_line.emit(f"[SIMULATION] Would run: {cmd_str}")
            self.output_line.emit("[SIMULATION] (No real command executed on this platform)")
            self.finished.emit(True, "Simulation complete")
            return

        try:
            proc = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            for line in proc.stdout:  # type: ignore[union-attr]
                if self._cancelled:
                    proc.terminate()
                    self.finished.emit(False, "Cancelled by user")
                    return
                self.output_line.emit(line.rstrip())
            proc.wait()
            success = proc.returncode == 0
            msg = "Completed successfully" if success else f"Exit code {proc.returncode}"
            self.finished.emit(success, msg)
        except FileNotFoundError:
            msg = f"Command not found: {self.cmd[0]}"
            log.error(msg)
            self.finished.emit(False, msg)
        except Exception as exc:
            log.exception("Unexpected error running command")
            self.finished.emit(False, str(exc))


# ---------------------------------------------------------------------------
# Specific package operations
# ---------------------------------------------------------------------------

class PackageManager(QObject):
    """
    High-level package management API.

    Methods return CommandWorker instances.  The caller must:
      1. Show the user the command + explanation (Terminal Learning Mode).
      2. Ask for confirmation.
      3. Start the worker.
      4. Connect to worker signals for UI updates.
    """

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

    # -- apt helpers ---------------------------------------------------------

    def update_package_list(self) -> CommandWorker:
        """apt update"""
        return CommandWorker(["sudo", "apt", "update", "-y"])

    def upgrade_packages(self) -> CommandWorker:
        """apt upgrade"""
        return CommandWorker(["sudo", "apt", "upgrade", "-y"])

    def install_package(self, package: str) -> CommandWorker:
        """apt install <package>"""
        return CommandWorker(["sudo", "apt", "install", "-y", package])

    def remove_package(self, package: str) -> CommandWorker:
        """apt remove <package>"""
        return CommandWorker(["sudo", "apt", "remove", "-y", package])

    def autoremove(self) -> CommandWorker:
        """apt autoremove"""
        return CommandWorker(["sudo", "apt", "autoremove", "-y"])

    def clean_cache(self) -> CommandWorker:
        """apt clean + autoclean"""
        return CommandWorker(["sudo", "apt", "clean"])

    def install_multimedia_codecs(self) -> CommandWorker:
        """Install common multimedia codecs."""
        return CommandWorker(
            ["sudo", "apt", "install", "-y",
             "ubuntu-restricted-extras", "libavcodec-extra",
             "gstreamer1.0-plugins-bad", "gstreamer1.0-plugins-ugly"]
        )

    # -- Flatpak helpers -----------------------------------------------------

    def install_flatpak(self) -> CommandWorker:
        """Install flatpak and add Flathub."""
        return CommandWorker(
            ["sudo", "apt", "install", "-y", "flatpak",
             "gnome-software-plugin-flatpak"]
        )

    def add_flathub(self) -> CommandWorker:
        """flatpak remote-add --if-not-exists flathub"""
        return CommandWorker(
            ["flatpak", "remote-add", "--if-not-exists", "flathub",
             "https://dl.flathub.org/repo/flathub.flatpakrepo"]
        )

    def install_flatpak_app(self, app_id: str) -> CommandWorker:
        """flatpak install <app_id>"""
        return CommandWorker(["flatpak", "install", "-y", "flathub", app_id])

    # -- Driver helpers -------------------------------------------------------

    def install_nvidia_driver(self) -> CommandWorker:
        """Install recommended NVIDIA driver."""
        return CommandWorker(
            ["sudo", "ubuntu-drivers", "install"]
        )

    def check_drivers(self) -> CommandWorker:
        """ubuntu-drivers devices"""
        return CommandWorker(["ubuntu-drivers", "devices"])

    @staticmethod
    def build_command_explanation(cmd: list[str]) -> dict:
        """
        Return a structured explanation dict for a given command.
        Used by TerminalPanel to display human-friendly breakdowns.
        """
        cmd_str = shlex.join(cmd)
        explanations = {
            "sudo": "Runs the command with administrator (superuser) privileges.",
            "apt": "APT is Pardus/Debian's package manager — it installs, removes, and updates software.",
            "update": "Downloads the latest list of available packages from the internet.",
            "upgrade": "Installs newer versions of all installed packages.",
            "install": "Installs the specified package(s) from the repository.",
            "remove": "Removes the specified package (keeps configuration files).",
            "autoremove": "Removes packages that were installed as dependencies but are no longer needed.",
            "clean": "Deletes downloaded package files (.deb) from the local cache.",
            "flatpak": "Flatpak is a universal packaging format that works on any Linux distro.",
            "remote-add": "Adds a new software source (repository) to flatpak.",
            "-y": "Automatically answers 'yes' to confirmation prompts.",
        }
        args = []
        for part in cmd:
            args.append({
                "token": part,
                "explanation": explanations.get(part, ""),
            })
        return {
            "command": cmd_str,
            "args": args,
        }


# Singleton
package_manager = PackageManager()
