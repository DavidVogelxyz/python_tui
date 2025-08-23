#!/usr/bin/env python3
"""
Python TUI Template - Inspired by linutil
A modern text-based user interface built with textual framework
"""

import asyncio
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static, DataTable, Tree, Label
from textual.widgets.tree import TreeNode
from textual.reactive import reactive
from textual import work
from textual.binding import Binding
from views import SystemInfoView, FileManagerView, ProcessMonitorView, NetworkToolsView, SettingsView


class NavigationPanel(Static):
    """Left navigation panel with menu items"""

    def compose(self) -> ComposeResult:
        yield Label("Navigation", classes="section-title")
        yield Button("System Info", id="btn-system", classes="nav-button")
        yield Button("File Manager", id="btn-files", classes="nav-button")
        yield Button("Process Monitor", id="btn-processes", classes="nav-button")
        yield Button("Network Tools", id="btn-network", classes="nav-button")
        yield Button("Settings", id="btn-settings", classes="nav-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle navigation button clicks"""
        button_id = event.button.id
        # Get the parent app to access the content area
        app = self.app
        if app:
            content_area = app.query_one("#content-area")
            if content_area:
                if button_id == "btn-system":
                    content_area.show_view("system")
                elif button_id == "btn-files":
                    content_area.show_view("files")
                elif button_id == "btn-processes":
                    content_area.show_view("processes")
                elif button_id == "btn-network":
                    content_area.show_view("network")
                elif button_id == "btn-settings":
                    content_area.show_view("settings")


class ContentArea(ScrollableContainer):
    """Main content area that changes based on navigation"""

    current_view = reactive("system")
    is_switching = False

    def compose(self) -> ComposeResult:
        yield SystemInfoView(id="system-view")

    def show_view(self, view_name: str) -> None:
        """Show the specified view"""
        # Prevent duplicate view switching
        if self.current_view == view_name or self.is_switching:
            return

        self.is_switching = True
        self.current_view = view_name

        # Remove all existing views
        for child in list(self.children):
            child.remove()

        # Add the selected view with a unique ID
        if view_name == "system":
            self.mount(SystemInfoView(id=f"system-view-{id(self)}"))
        elif view_name == "files":
            self.mount(FileManagerView(id=f"files-view-{id(self)}"))
        elif view_name == "processes":
            self.mount(ProcessMonitorView(id=f"processes-view-{id(self)}"))
        elif view_name == "network":
            self.mount(NetworkToolsView(id=f"network-view-{id(self)}"))
        elif view_name == "settings":
            self.mount(SettingsView(id=f"settings-view-{id(self)}"))

        # Reset switching flag after a short delay
        self.call_after_refresh(self._reset_switching_flag)

    def _reset_switching_flag(self):
        """Reset the switching flag after view change"""
        self.is_switching = False


class PythonTUIApp(App):
    """Main TUI application class"""

    CSS_PATH = "styles.css"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("h", "show_help", "Help"),
        Binding("1", "view_system", "System"),
        Binding("2", "view_files", "Files"),
        Binding("3", "view_processes", "Processes"),
        Binding("4", "view_network", "Network"),
        Binding("5", "view_settings", "Settings"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the main application layout"""
        yield Header(show_clock=True)

        with Container(id="main-container"):
            with Horizontal(id="app-layout"):
                yield NavigationPanel(id="nav-panel")
                yield ContentArea(id="content-area")

        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.title = "Python TUI - linutil-inspired Template"
        self.sub_title = "Modern Text-Based User Interface"

    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()

    def action_show_help(self) -> None:
        """Show help information"""
        # Implementation for help display
        pass

    def action_view_system(self) -> None:
        """Switch to system view"""
        content_area = self.query_one("#content-area")
        content_area.show_view("system")

    def action_view_files(self) -> None:
        """Switch to files view"""
        content_area = self.query_one("#content-area")
        content_area.show_view("files")

    def action_view_processes(self) -> None:
        """Switch to processes view"""
        content_area = self.query_one("#content-area")
        content_area.show_view("processes")

    def action_view_network(self) -> None:
        """Switch to network view"""
        content_area = self.query_one("#content-area")
        content_area.show_view("network")

    def action_view_settings(self) -> None:
        """Switch to settings view"""
        content_area = self.query_one("#content-area")
        content_area.show_view("settings")


def main():
    """Main entry point"""
    app = PythonTUIApp()
    app.run()


if __name__ == "__main__":
    main()
