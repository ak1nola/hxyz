# THXY - tmux + Helix + yazi Integration

A powerful simple picker integration that brings seamless file selection to Helix through yazi and tmux terminal multiplexing.

It is based on [zide](https://github.com/josephschmitt/zide) - but, hopefully, a little more lightweight and simpler.

## What is THXY?

THXY is a shell script that integrates three powerful terminal tools:
- **tmux** - A terminal multiplexer
- **Helix** - A modern text editor
- **yazi** - A blazing fast file manager

It provides a convenient file picker directly accessible from within Helix via a simple keybinding.

## Features

- **Quick File Picker**: Toggle a file picker pane with `space + m + f` in Helix (`thxy picker`)
- **Seamless Navigation**: Browse files in yazi and open selections directly in Helix
- **Session Management**: Auto-creates named tmux sessions for organization
- **Configuration Support**: Includes optimized yazi configuration
- **Non-Destructive Install**: Safe installation with conflict detection

## Nota Bene

The file picker command (`thxy picker`) toggles a pane titled `picker` in the current tmux window. If the pane exists it is closed, otherwise a new left-side yazi pane is created for the current working directory.

## Requirements

Before installing THXY, ensure you have the following installed:

- **tmux** - Terminal multiplexer
- **yazi** - File manager
- **Helix** (or `hx`) - Text editor
- **Python 3** - For the install script

## Installation

### Using the Install Script

Note: the install script also creates a 'th' symlink so that after installation you can open tmux + Helix with either `th` or `thxy`

1. Navigate to the THXY directory:
   ```bash
   cd ./thxy
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
   - ✓ Copy the thxy script to `~/.local/bin/thxy`
   - ✓ Copy yazi configuration to `~/.config/thxy/yazi.toml`
   - ✓ Inject the keybinding into your Helix config

### Manual Installation

If you prefer to install manually:

1. Copy the script:
   ```bash
   cp bin/thxy ~/.local/bin/thxy
   chmod +x ~/.local/bin/thxy
   ```

2. Copy the yazi configuration:
   ```bash
   mkdir -p ~/.config/thxy
   cp config/yazi.toml ~/.config/thxy/yazi.toml
   ```

3. Add the keybinding to your Helix config (`~/.config/helix/config.toml`):
   ```toml
   [keys.normal.space.m]
   f = ':sh thxy picker "%{buffer_name}"'
   g = ':sh thxy git'
   ```

## Usage

### Using the Keybinding

While editing in Helix (running within tmux):

1. Press `space` (space leader key)
2. Press `m` (group key)
3. Press `f` (file picker key)

This toggles a file picker pane on the left. You can then:
- Navigate files with arrow keys or `j`/`k`
- Open files with `Enter`
- Select multiple files
- Close the picker with `q` or `ESC`

### Using the Command

You can also run THXY directly from the terminal:

```bash
# Start THXY in current directory
thxy

# Start with custom session name
thxy -s myproject

# Show usage information
thxy --help
```

## How It Works

### The File Picker Flow

1. **Toggle Picker**: Press `space m f` in Helix (runs `thxy picker "%{buffer_name}"`)
2. **Browse Files**: Use yazi to navigate the file system
3. **Select & Open**: Choose files to open in Helix
4. **Auto-focus**: Helix pane automatically receives focus when you select files

### Session Management

THXY creates tmux sessions with auto-generated names or custom names:
- Default format: `thxy-{process-id}`
- Custom name: `thxy -s myproject` creates a session named exactly `myproject`

This allows multiple independent THXY sessions without conflicts.

## Configuration

### yazi Configuration

The THXY installation includes an optimized `yazi.toml` configuration file at:
```
~/.config/thxy/yazi.toml
```

This configuration is tailored for use with THXY and Helix integration. You can customize it further if needed.

### Environment Variables

You can customize THXY behavior with environment variables:

```bash
# Set custom yazi configuration directory
export THXY_HOME=~/.config/custom/yazi

# Disable custom yazi config (use system default)
export THXY_USE_YAZI_CONFIG=false

# Custom session prefix
thxy -s custom-session-name
```

### Helix Keybindings

If you want to customize the keybindings, edit `~/.config/helix/config.toml`:

```toml
[keys.normal.space.m]
f = ':sh thxy picker "%{buffer_name}"'  # Current binding
g = ':sh thxy git'                       # Lazygit popup

# You can also add custom variations:
# q = ':sh thxy picker'               # Open without current file context
# v = ':sh thxy -s vsplit picker'     # Future: split variation
```

## Troubleshooting

### "Missing dependencies" error

**Problem**: The install script reports missing tmux, yazi, or Helix

**Solution**: Install the missing tools
```bash
# Example for Arch Linux
sudo pacman -S tmux yazi helix

# Or use your package manager
```

To skip dependency checking (if tools are installed in non-standard locations):
```bash
python3 install.py --no-dep-check
```

### "thxy already exists" error

**Problem**: THXY installation detects an existing thxy at `~/.local/bin/thxy`

**Solution**: Either remove the existing file or verify it's the version you want:
```bash
rm ~/.local/bin/thxy
python3 install.py
```

### "space m f already exists" error

**Problem**: The keybinding is already present in Helix config

**Solution**: This is expected if you've already installed THXY. The install script prevents duplicate keybindings. If you want to reinstall:
```bash
# Edit ~/.config/helix/config.toml and remove the thxy keybinding
# Then run install again
python3 install.py
```

### Files not opening in Helix

**Problem**: Selected files don't appear in Helix after using the picker

**Solution**: 
- Ensure Helix is the active pane (it should auto-focus after selection)
- Check that your Helix config is properly loaded
- Verify the keybinding is correctly installed with `thxy --help`

## Uninstalling

** Use the uninstall mode in the install script **

```bash
python3 install.py uninstall
```

This removes the following (i.e. you can uninstall manually this way):
- `~/.local/bin/thxy`
- `~/.local/bin/th`
- `~/.config/thxy`
- The THXY keys added under `[keys.normal.space.m]` in `~/.config/helix/config.toml`

## Performance Tips

1. **First Run**: The first time you use `thxy`, tmux creates the session. This takes 1-2 seconds.

2. **Session Reuse**: Subsequent calls reuse the existing tmux session for faster startup.

3. **yazi Preview**: The included yazi.toml enables image previews. Disable if you want faster performance:
   ```toml
   [preview]
   tab_size = 0  # Disable tab size preview
   ```

## Architecture

### File Structure

```
~/.local/bin/thxy              # Executable script
~/.config/helix/config.toml    # Helix config with keybinding (modified during install)
~/.config/thxy/
├── yazi.toml                  # yazi configuration
└── plugins/
    └── auto-layout.yazi       # Auto-layout plugin for yazi
```

### Session Layout

When you run `thxy picker`, THXY creates:
```
tmux Session
├── Main Pane (Helix)
└── Left Pane (yazi file picker)
```

Files selected in yazi are automatically opened in the Helix pane.

## Development

### Modifying the Script

The THXY scripts are written in bash and use:
- tmux CLI for pane management
- `jq` for JSON parsing
- yazi for file browsing

Key script responsibilities:
- `bin/thxy` - Main command dispatcher (`picker`, `git`, `vibe`, and internal `loadbuffer`)
- `bin/thxy-picker` - Opens/closes the picker pane in the current tmux window
- `bin/thxy-buffer` - Runs yazi and handles picker callbacks that open files in Helix

### Contributing

To improve THXY:
1. Edit `bin/thxy`
2. Test with `thxy picker`
3. Report issues or suggest improvements

## License

THXY is provided as-is. Use at your own risk.

## Credits

THXY integrates:
- **tmux** - Terminal multiplexer (https://github.com/tmux/tmux)
- **yazi** - File manager (https://yazi.rs)
- **Helix** - Text editor (https://helix-editor.com)

---

**Version**: 1.0  
**Last Updated**: 2026-05-15  
**Installed at**: `~/Projects/thxy`
