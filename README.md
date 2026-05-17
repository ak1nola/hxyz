# HXZY - Helix + Zellij + Yazi Integration

A powerful file picker integration that brings seamless file selection to Helix through Yazi and Zellij terminal multiplexing.

## What is HXZY?

HXZY is a shell script that integrates three powerful terminal tools:
- **Helix** - A modern text editor
- **Zellij** - A terminal multiplexer (like tmux)
- **Yazi** - A blazing fast file manager

It provides a convenient file picker directly accessible from within Helix via a simple keybinding.

## Features

- **Quick File Picker**: Toggle a file picker pane with `space + q + f` in Helix
- **Seamless Navigation**: Browse files in Yazi and open selections directly in Helix
- **Session Management**: Auto-creates named Zellij sessions for organization
- **Configuration Support**: Includes optimized Yazi configuration
- **Non-Destructive Install**: Safe installation with conflict detection

## Requirements

Before installing HXZY, ensure you have the following installed:

- **Zellij** - Terminal multiplexer
- **Yazi** - File manager
- **Helix** (or `hx`) - Text editor
- **Python 3** - For the install script

## Installation

### Using the Install Script

1. Navigate to the HXYZ directory:
   ```bash
   cd ~/Projects/hxyz
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
   - ✓ Copy the hxyz script to `~/.local/bin/hxyz`
   - ✓ Copy yazi configuration to `~/.config/hxyz/yazi.toml`
   - ✓ Inject the keybinding into your Helix config

### Manual Installation

If you prefer to install manually:

1. Copy the script:
   ```bash
   cp bin/hxyz ~/.local/bin/hxyz
   chmod +x ~/.local/bin/hxyz
   ```

2. Copy the yazi configuration:
   ```bash
   mkdir -p ~/.config/xyz
   cp yazi.toml ~/.config/xyz/yazi.toml
   ```

3. Add the keybinding to your Helix config (`~/.config/helix/config.toml`):
   ```toml
   [keys.normal.space.q]
   f = ':sh hxyz toggle "%{buffer_name}"'
   ```

## Usage

### Using the Keybinding

While editing in Helix:

1. Press `space` (space leader key)
2. Press `q` (group key)
3. Press `f` (file picker key)

This toggles a file picker pane on the left. You can then:
- Navigate files with arrow keys or `j`/`k`
- Open files with `Enter`
- Select multiple files
- Close the picker with `q` or `ESC`

### Using the Command

You can also run HXZY directly from the terminal:

```bash
# Start HXZY in current directory
hxzy

# Start with custom session name prefix
hxzy -s myproject

# Show usage information
hxzy --help
```

## How It Works

### The File Picker Flow

1. **Toggle Picker**: Press `space q f` in Helix to toggle the picker pane
2. **Browse Files**: Use Yazi to navigate the file system
3. **Select & Open**: Choose files to open in Helix
4. **Auto-focus**: Helix pane automatically receives focus when you select files

### Session Management

HXYZ creates Zellij sessions with auto-generated names:
- Default format: `hxyz-{process-id}`
- Custom prefix: `hxyz -s myproject` creates `myproject-{process-id}`

This allows multiple independent HXZY sessions without conflicts.

## Configuration

### Yazi Configuration

The HXZY installation includes an optimized `yazi.toml` configuration file at:
```
~/.config/xyz/yazi.toml
```

This configuration is tailored for use with HXZY and Helix integration. You can customize it further if needed.

### Environment Variables

You can customize HXZY behavior with environment variables:

```bash
# Set custom Yazi configuration directory
export HXYZ_HOME=~/.config/custom/yazi

# Disable custom Yazi config (use system default)
export HXYZ_USE_YAZI_CONFIG=false

# Custom session prefix
hxyz -s custom-session-name
```

### Helix Keybindings

If you want to customize the keybindings, edit `~/.config/helix/config.toml`:

```toml
[keys.normal.space.q]
f = ':sh hxyz toggle "%{buffer_name}"'  # Current binding

# You can also add custom variations:
# q = ':sh hxyz toggle'                # Open without current file context
# v = ':sh hxyz -s vsplit toggle'     # Future: split variation
```

## Troubleshooting

### "Missing dependencies" error

**Problem**: The install script reports missing Zellij, Yazi, or Helix

**Solution**: Install the missing tools
```bash
# Example for Arch Linux
sudo pacman -S zellij yazi helix

# Or use your package manager
```

To skip dependency checking (if tools are installed in non-standard locations):
```bash
python3 install.py --no-dep-check
```

### "hxzy already exists" error

**Problem**: HXZY installation detects an existing hxzy at `~/.local/bin/hxzy`

**Solution**: Either remove the existing file or verify it's the version you want:
```bash
rm ~/.local/bin/hxzy
python3 install.py
```

### "space q f already exists" error

**Problem**: The keybinding is already present in Helix config

**Solution**: This is expected if you've already installed HXYZ. The install script prevents duplicate keybindings. If you want to reinstall:
```bash
# Edit ~/.config/helix/config.toml and remove the hxyz keybinding
# Then run install again
python3 install.py
```

### Files not opening in Helix

**Problem**: Selected files don't appear in Helix after using the picker

**Solution**: 
- Ensure Helix is the active pane (it should auto-focus after selection)
- Check that your Helix config is properly loaded
- Verify the keybinding is correctly installed with `hxyz --help`

## Uninstalling

HXZY installation is unintrusive, so uninstalling is simple:

```bash
# Remove the hxyz script
rm ~/.local/bin/hxzy

# Remove yazi configuration
rm -rf ~/.config/xyz

# Remove the keybinding from ~/.config/helix/config.toml
# (Edit the file and remove the [keys.normal.space.q] section)
```

## Performance Tips

1. **First Run**: The first time you use `hxyz`, Zellij creates the session. This takes 1-2 seconds.

2. **Session Reuse**: Subsequent calls reuse the existing Zellij session for faster startup.

3. **Yazi Preview**: The included yazi.toml enables image previews. Disable if you want faster performance:
   ```toml
   [preview]
   tab_size = 0  # Disable tab size preview
   ```

## Architecture

### File Structure

```
~/.local/bin/hxzy              # Executable script
~/.config/helix/config.toml    # Helix config with keybinding (modified during install)
~/.config/xyz/
├── yazi.toml                  # Yazi configuration
└── plugins/
    └── auto-layout.yazi       # Auto-layout plugin for Yazi
```

### Session Layout

When you toggle the picker, HXZY creates:
```
Zellij Session
├── Main Pane (Helix)
└── Left Pane (Yazi file picker)
```

Files selected in Yazi are automatically opened in the Helix pane.

## Development

### Modifying the Script

The hxyz script is written in bash and uses:
- Zellij CLI for pane management
- Python 3 for JSON parsing
- Yazi for file browsing

Key functions:
- `toggle_picker()` - Opens/closes the picker pane
- `run_picker()` - Runs Yazi with proper configuration
- `edit_from_picker()` - Opens selected files in Helix

### Contributing

To improve HXZY:
1. Edit `bin/hxzy`
2. Test with `hxzy toggle`
3. Report issues or suggest improvements

## License

HXZY is provided as-is. Use at your own risk.

## Credits

HXZY integrates:
- **Zellij** - Terminal multiplexer (https://zellij.dev)
- **Yazi** - File manager (https://yazi.rs)
- **Helix** - Text editor (https://helix-editor.com)

---

**Version**: 1.0  
**Last Updated**: 2026-05-15  
**Installed at**: `~/Projects/hxyz`
