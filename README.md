# Python TUI Template

A modern, interactive text-based user interface (TUI) built with Python and the `textual` framework.

## Features

- **Modern TUI Framework**: Built with `textual`, a powerful Python library for creating interactive text interfaces
- **Multi-View Navigation**: Switch between different content views (System Info, File Manager, Process Monitor, Network Tools, Settings)
- **Responsive Design**: Adapts to different terminal sizes with responsive layouts
- **CSS-like Styling**: Professional appearance with customizable themes and styling
- **Keyboard Shortcuts**: Quick navigation using number keys (1-5) and other shortcuts
- **System Integration**: Real-time system monitoring and file management capabilities

## Screenshots

The TUI features:
- Header with clock display
- Left navigation panel with menu buttons
- Main content area that changes based on selection
- Footer with status information
- Professional color scheme and borders

## Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd python_tui
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Dependencies

- `textual` >= 0.40.0 - Modern TUI framework
- `rich` >= 13.0.0 - Rich text and formatting
- `psutil` >= 5.9.0 - System and process utilities

## Usage

### Navigation

- **Mouse**: Click on navigation buttons to switch views
- **Keyboard**: Use number keys 1-5 for quick navigation
- **Shortcuts**:
  - `q` - Quit the application
  - `h` - Show help
  - `1` - System Info view
  - `2` - File Manager view
  - `3` - Process Monitor view
  - `4` - Network Tools view
  - `5` - Settings view

### Views

#### System Info
- Operating system details
- Memory usage statistics
- CPU information and usage

#### File Manager
- Navigate directory structure
- View files and folders
- Basic file operations (Home, Parent, Refresh)

#### Process Monitor
- Real-time process list
- CPU and memory usage per process
- Process status information

#### Network Tools
- Network interface information
- Active network connections
- Network statistics

#### Settings
- Theme selection (Light/Dark/Auto)
- Display options configuration
- Application preferences

## Project Structure

```
python_tui/
├── main.py              # Main application entry point
├── views.py             # Individual view components
├── styles.css           # CSS styling for the TUI
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Customization

### Adding New Views

1. Create a new view class in `views.py`:
   ```python
   class MyCustomView(Static):
       def compose(self):
           yield Label("My Custom View", classes="section-title")
           # Add your widgets here
   ```

2. Add navigation button in `NavigationPanel`:
   ```python
   yield Button("My View", id="btn-myview", classes="nav-button")
   ```

3. Update the `ContentArea.show_view()` method to handle the new view.

### Styling

Modify `styles.css` to customize:
- Colors and themes
- Layout and spacing
- Button and widget appearance
- Responsive breakpoints

### Key Bindings

Add new keyboard shortcuts in the `BINDINGS` list in `main.py`:
```python
BINDINGS = [
    # ... existing bindings ...
    Binding("n", "new_action", "New Action"),
]
```

## Development

### Running in Development Mode

For development and debugging:
```bash
python -m textual dev main.py
```

### Testing

The application can be tested by running it in different terminal sizes to verify responsive behavior.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Inspired by the `ChrisTitusTech/linutil` project's TUI design
- Worked with Cursor and its AI agent
- Built with the excellent `textual` framework
- Uses `psutil` for system monitoring capabilities

## Support

For issues, questions, or contributions, please open an issue on the project repository.
