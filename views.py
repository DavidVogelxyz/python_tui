"""
Views module for the Python TUI Template
Contains different content views that can be displayed in the main content area
"""

from textual.widgets import Static, Label, DataTable, Tree, Button, Input
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual import work
import psutil
import os
from pathlib import Path


class SystemInfoView(Static):
    """System information view showing OS details, memory, CPU, etc."""

    def compose(self):
        yield Label("System Information", classes="section-title")

        # System details
        yield Label("Operating System", classes="subsection-title")
        yield Label(f"OS: {os.name}", classes="info-text")
        yield Label(f"Platform: {os.uname().sysname}", classes="info-text")
        yield Label(f"Release: {os.uname().release}", classes="info-text")
        yield Label(f"Machine: {os.uname().machine}", classes="info-text")

        # Memory information
        yield Label("Memory Usage", classes="subsection-title")
        memory = psutil.virtual_memory()
        yield Label(f"Total: {memory.total // (1024**3):.1f} GB", classes="info-text")
        yield Label(f"Available: {memory.available // (1024**3):.1f} GB", classes="info-text")
        yield Label(f"Used: {memory.percent:.1f}%", classes="info-text")

        # CPU information
        yield Label("CPU Information", classes="subsection-title")
        yield Label(f"CPU Count: {psutil.cpu_count()}", classes="info-text")
        yield Label(f"CPU Usage: {psutil.cpu_percent(interval=1):.1f}%", classes="info-text")

        # Additional system info
        yield Label("Disk Information", classes="subsection-title")
        try:
            disk = psutil.disk_usage('/')
            yield Label(f"Root Disk Total: {disk.total // (1024**3):.1f} GB", classes="info-text")
            yield Label(f"Root Disk Used: {disk.used // (1024**3):.1f} GB", classes="info-text")
            yield Label(f"Root Disk Free: {disk.free // (1024**3):.1f} GB", classes="info-text")
        except Exception:
            yield Label("Disk information unavailable", classes="info-text")

        # User information
        yield Label("User Information", classes="subsection-title")
        yield Label(f"Username: {os.getlogin()}", classes="info-text")
        yield Label(f"Home Directory: {os.path.expanduser('~')}", classes="info-text")
        yield Label(f"Current Working Directory: {os.getcwd()}", classes="info-text")


class FileManagerView(Static):
    """File manager view showing directory structure and files"""

    current_path = reactive(str(Path.home()))

    def compose(self):
        yield Label("File Manager", classes="section-title")

        # Path display
        with Horizontal():
            yield Label("Current Path:", classes="label")
            yield Label(self.current_path, classes="path-text")

        # Navigation buttons
        with Horizontal():
            yield Button("Home", id="btn-home", classes="action-button")
            yield Button("Parent", id="btn-parent", classes="action-button")
            yield Button("Refresh", id="btn-refresh", classes="action-button")

        # File tree
        yield self.create_file_tree()

    def create_file_tree(self):
        """Create a tree view of the current directory"""
        tree = Tree("Files", id="file-tree")
        try:
            path = Path(self.current_path)
            if path.exists() and path.is_dir():
                for item in sorted(path.iterdir()):
                    if item.is_dir():
                        node = tree.root.add(f"📁 {item.name}", data=str(item))
                    else:
                        node = tree.root.add(f"📄 {item.name}", data=str(item))
        except PermissionError:
            tree.root.add("Permission denied", data="")
        return tree

    def on_button_pressed(self, event):
        """Handle file manager button clicks"""
        button_id = event.button.id
        if button_id == "btn-home":
            self.current_path = str(Path.home())
        elif button_id == "btn-parent":
            parent = Path(self.current_path).parent
            if str(parent) != self.current_path:
                self.current_path = str(parent)
        elif button_id == "btn-refresh":
            pass  # Refresh the file tree

        self.update_file_tree()

    def update_file_tree(self):
        """Update the file tree display"""
        # Implementation for updating the file tree
        pass


class ProcessMonitorView(Static):
    """Process monitor view showing running processes"""

    def compose(self):
        yield Label("Process Monitor", classes="section-title")

        # Process table
        table = DataTable(id="process-table")
        table.add_columns("PID", "Name", "CPU %", "Memory %", "Status")

        # Populate with process data
        self.populate_process_table(table)

        yield table

    def populate_process_table(self, table):
        """Populate the process table with current process data"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    table.add_row(
                        str(info['pid']),
                        info['name'][:20],  # Truncate long names
                        f"{info['cpu_percent']:.1f}",
                        f"{info['memory_percent']:.1f}",
                        info['status']
                    )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            table.add_row("Error", str(e), "", "", "")


class NetworkToolsView(Static):
    """Network tools view showing network interfaces and connections"""

    def compose(self):
        yield Label("Network Tools", classes="section-title")

        # Network interfaces
        yield Label("Network Interfaces", classes="subsection-title")
        interfaces = psutil.net_if_addrs()
        for interface, addrs in interfaces.items():
            yield Label(f"Interface: {interface}", classes="info-text")
            for addr in addrs:
                yield Label(f"  {addr.family.name}: {addr.address}", classes="info-text")

        # Network connections
        yield Label("Active Connections", classes="subsection-title")
        try:
            connections = psutil.net_connections()
            for conn in connections[:10]:  # Show first 10 connections
                if conn.status == 'ESTABLISHED':
                    yield Label(
                        f"{conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port}",
                        classes="info-text"
                    )
        except Exception as e:
            yield Label(f"Error getting connections: {e}", classes="info-text")


class SettingsView(Static):
    """Settings view for application configuration"""

    def compose(self):
        yield Label("Settings", classes="section-title")

        # Theme selection
        yield Label("Theme", classes="subsection-title")
        with Horizontal():
            yield Button("Light", id="btn-light", classes="theme-button")
            yield Button("Dark", id="btn-dark", classes="theme-button")
            yield Button("Auto", id="btn-auto", classes="theme-button")

        # Display options
        yield Label("Display Options", classes="subsection-title")
        yield Label("Show clock in header: Yes", classes="info-text")
        yield Label("Auto-refresh interval: 5s", classes="info-text")
        yield Label("Enable animations: Yes", classes="info-text")

        # Save button
        yield Button("Save Settings", id="btn-save", classes="action-button")

    def on_button_pressed(self, event):
        """Handle settings button clicks"""
        button_id = event.button.id
        if button_id == "btn-light":
            # Apply light theme
            pass
        elif button_id == "btn-dark":
            # Apply dark theme
            pass
        elif button_id == "btn-auto":
            # Apply auto theme
            pass
        elif button_id == "btn-save":
            # Save settings
            pass
