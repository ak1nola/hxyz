# WHXY - WezTerm + Helix + Yazi Integration

A powerful simple picker integration that brings seamless file selection to Helix through yazi and WezTerm's native multiplexing.

It is based on [THXY](https://github.com/ak1nola/hxyz) but uses WezTerm instead of tmux for terminal multiplexing.

## What is WHXY?

WHXY is a shell script that integrates three powerful terminal tools:
- **WezTerm** - A GPU-accelerated terminal emulator with built-in multiplexing
- **Helix** - A modern text editor
- **yazi** - A blazing fast file manager

It provides a convenient file picker directly accessible from within Helix via a simple keybinding.

## Features

- **Quick File Picker**: Toggle a file picker pane with `space + m + f` in Helix (`whxy picker`)
- **Seamless Navigation**: Browse files in yazi and open selections directly in Helix
- **Native Multiplexing**: Uses WezTerm's built-in pane management (no tmux required)
- **Configuration Support**: Includes optimized yazi configuration
- **Non-Destructive Install**: Safe installation with conflict detection

## Nota Bene

The file picker command (`whxy picker`) toggles a pane in the current WezTerm tab. If a picker pane exists it is closed, otherwise a new left-side yazi pane is created for the current working directory.

## Requirements

Before installing WHXY, ensure you have the following installed:

- **WezTerm** - GPU-accelerated terminal emulator (https://wezfurlong.org/wezterm/)
- **yazi** - File manager
- **Helix** (or `hx`) - Text editor
- **Python 3** - For the install script

## Installation

### Using the Install Script

Note: the install script also creates a 'wh' symlink so that after installation you can open WezTerm + Helix with either `wh` or `whxy`

1. Navigate to the WHXY directory:
   ```bash
   cd ./wezTerm
   ```

2. Run the install script:
   ```bash
   python3 install.py
   ```

   **Options:**
   - `--dry-run` - Preview what will be installed without making changes
   - `--verbose` or `-v` - Show detailed progress during installation
   - `--no-dep-check` - Skip dependency verification

3. The script will:
   - ✓ Verify all dependencies are installed
   - ✓ Check for conflicts with existing files
   - ✓ Copy the whxy script to `~/.local/bin/whxy`
   - ✓ Copy yazi configuration to `~/.config/whxy/yazi.toml`
   - ✓ Inject the keybinding into your Helix config

### Manual Installation

If you prefer to install manually:

1. Copy the script:
   ```bash
   cp bin/whxy ~/.local/bin/whxy
   chmod +x ~/.local/bin/whxy
   ```

2. Copy the yazi configuration:
   ```bash
   mkdir -p ~/.config/whxy
   cp config/yazi.toml ~/.config/whxy/yazi.toml
   ```

3. Add the keybinding to your Helix config (`~/.config/helix/config.toml`):
   ```toml
   [keys.normal.space.m]
   f = ':sh whxy picker "%{buffer_name}"'
   g = ':sh whxy git'
   o = ':sh whxy vibe "%{buffer_name}" %{cursor_line}'
   ```

## Usage

### Using the Keybinding

While editing in Helix (running within WezTerm):

1. Press `space` (space leader key)
2. Press `m` (group key)
3. Press `f` (file picker key)

This toggles a file picker pane on the left. You can then:
- Navigate files with arrow keys or `j`/`k`
- Open files with `Enter`
- Select multiple files
- Close the picker with `q` or `ESC`

### Using the Command

You can also run WHXY directly from the terminal:

```bash
# Start WHXY in current directory
whxy

# Show usage information
whxy --help
```

## How It Works

### The File Picker Flow

1. **Toggle Picker**: Press `space m f` in Helix (runs `whxy picker "%{buffer_name}"`)
2. **Browse Files**: Use yazi to navigate the file system
3. **Select & Open**: Choose files to open in Helix
4. **Auto-focus**: Helix pane automatically receives focus when you select files

### WezTerm Integration

WHXY uses WezTerm's CLI to manage panes:
- `wezterm cli split-pane` - Creates new panes
- `wezterm cli list --format=json` - Discovers pane information
- `wezterm cli kill-pane` - Closes panes
- `wezterm cli activate-pane-direction` - Focuses panes

This provides a seamless experience without requiring an additional terminal multiplexer.

## Configuration

### yazi Configuration

The WHXY installation includes an optimized `yazi.toml` configuration file at:
```
~/.config/whxy/yazi.toml
```

This configuration is tailored for use with WHXY and Helix integration. You can customize it further if needed.

### Environment Variables

You can customize WHXY behavior with environment variables:

```bash
# Set custom yazi configuration directory
export WHXY_HOME=~/.config/custom/yazi

# Disable custom yazi config (use system default)
export WHXY_USE_YAZI_CONFIG=false
```

### Helix Keybindings

If you want to customize the keybindings, edit `~/.config/helix/config.toml`:

```toml
[keys.normal.space.m]
f = ':sh whxy picker "%{buffer_name}"'  # Current binding
g = ':sh whxy git'                       # Lazygit popup
o = ':sh whxy vibe "%{buffer_name}" %{cursor_line}' # Copilot CLI

# You can also add custom variations:
# q = ':sh whxy picker'               # Open without current file context
```

## Troubleshooting

### "Missing dependencies" error

**Problem**: The install script reports missing WezTerm, yazi, or Helix

**Solution**: Install the missing tools
```bash
# Example for macOS
brew install --cask wezterm
brew install yazi helix

# For Linux, see WezTerm installation docs
```

To skip dependency checking (if tools are installed in non-standard locations):
```bash
python3 install.py --no-dep-check
```

### "whxy already exists" error

**Problem**: WHXY installation detects an existing whxy at `~/.local/bin/whxy`

**Solution**: Either remove the existing file or verify it's the version you want:
```bash
rm ~/.local/bin/whxy
python3 install.py
```

### "space m f already exists" error

**Problem**: The keybinding is already present in Helix config

**Solution**: This is expected if you've already installed WHXY. The install script prevents duplicate keybindings. If you want to reinstall:
```bash
# Edit ~/.config/helix/config.toml and remove the whxy keybinding
# Then run install again
python3 install.py
```

### Files not opening in Helix

**Problem**: Selected files don't appear in Helix after using the picker

**Solution**: 
- Ensure Helix is the active pane (it should auto-focus after selection)
- Check that your Helix config is properly loaded
- Verify the keybinding is correctly installed with `whxy --help`

### WezTerm CLI not found

**Problem**: Error messages about `wezterm` command not being found

**Solution**:
- Ensure WezTerm is installed and in your PATH
- On macOS, you may need to add `/Applications/WezTerm.app/Contents/MacOS` to your PATH
- Test with: `wezterm --version`

## Uninstalling

** Use the uninstall mode in the install script **

```bash
python3 install.py uninstall
```

This removes the following (i.e. you can uninstall manually this way):
- `~/.local/bin/whxy`
- `~/.local/bin/wh`
- `~/.config/whxy`
- The WHXY keys added under `[keys.normal.space.m]` in `~/.config/helix/config.toml`

## Performance Tips

1. **GPU Acceleration**: WezTerm uses GPU acceleration for fast rendering

2. **yazi Preview**: The included yazi.toml enables image previews. Disable if you want faster performance:
   ```toml
   [preview]
   tab_size = 0  # Disable tab size preview
   ```

## Architecture

### File Structure

```
~/.local/bin/whxy              # Executable script
~/.config/helix/config.toml    # Helix config with keybinding (modified during install)
~/.config/whxy/
└── yazi.toml                  # yazi configuration
```

### Pane Layout

When you run `whxy picker`, WHXY creates:
```
WezTerm Tab
├── Main Pane (Helix)
└── Left Pane (yazi file picker)
```

Files selected in yazi are automatically opened in the Helix pane.

## Development

### Modifying the Script

The WHXY scripts are written in bash and use:
- WezTerm CLI for pane management
- `jq` for JSON parsing
- yazi for file browsing

Key script responsibilities:
- `bin/whxy` - Main command dispatcher (`picker`, `git`, `vibe`, and internal `buffer`)
- Picker management via WezTerm CLI
- File opening via Helix shell commands

### Contributing

To improve WHXY:
1. Edit `bin/whxy`
2. Test with `whxy picker`
3. Report issues or suggest improvements

## Comparison with THXY

WHXY is similar to THXY but uses WezTerm instead of tmux:

**Advantages:**
- No additional multiplexer required (WezTerm has built-in panes)
- GPU-accelerated rendering
- Better font rendering and ligature support
- Native image preview support
- Simpler setup (one less dependency)

**Disadvantages:**
- Requires WezTerm specifically (less flexible than tmux)
- Different CLI for pane management

## License

WHXY is provided as-is. Use at your own risk.

## Credits

WHXY integrates:
- **WezTerm** - GPU-accelerated terminal (https://wezfurlong.org/wezterm/)
- **yazi** - File manager (https://yazi.rs)
- **Helix** - Text editor (https://helix-editor.com)

Based on **THXY** (https://github.com/ak1nola/hxyz)

---

**Version**: 1.0  
**Last Updated**: 2026-07-31
