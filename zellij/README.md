# HXYZ - Helix + Zellij + Yazi Integration

A powerful simple picker integration that brings seamless file selection to Helix through Yazi and Zellij terminal multiplexing.

It is based on [zide](https://github.com/josephschmitt/zide) - but, hopefully, a little more lightweight and simpler.

## What is HXYZ?

HXYZ is a shell script that integrates three powerful terminal tools:
- **Helix** - A modern text editor
- **Zellij** - A terminal multiplexer (like tmux)
- **Yazi** - A blazing fast file manager

It provides a convenient file picker directly accessible from within Helix via a simple keybinding.

## Features

- **Multi-Repo Sessions**: Work on multiple repositories in one Zellij session, each in its own tab
- **Per-Tab Layouts**: Each tab has independent picker, editor, terminal, and floating panes
- **Quick File Picker**: Toggle a file picker pane with `space + m + f` in Helix (per-tab)
- **Smart Helix Startup**: Running `hxyz` in an empty tab automatically creates and opens Helix
- **Per-Tab Floating Panes**: LazyGit and Copilot/vibe are scoped to each tab
- **Seamless Navigation**: Browse files in Yazi and open selections directly in Helix
- **Session Management**: Auto-creates named Zellij sessions for organization
- **Configuration Support**: Includes optimized Yazi configuration
- **Non-Destructive Install**: Safe installation with conflict detection

## Multi-Repo Workflow

HXYZ supports working on multiple repositories in a single Zellij session:

- **One Session, Many Repos**: Each tab represents a different repository or project
- **Independent Layouts**: Each tab can have its own picker, terminal, stacked panes, and floating panes
- **Tab-Scoped Features**: LazyGit and Vibe/Copilot are per-tab, using the correct repo directory
- **Easy Tab Creation**: Use `hxyz newtab ~/path/to/repo` or native Zellij commands (`Ctrl-t n`)

### Example Multi-Repo Workflow

```bash
# Start a session
hxyz -s work

# Tab 1 (auto-created): Backend repository
# - Open files with space m f (toggles picker)
# - Run LazyGit with space m g (tab-specific)
# - Use Copilot with space m v (tab-specific)

# Create Tab 2 for frontend
hxyz newtab ~/projects/frontend

# Create Tab 3 for infrastructure  
hxyz newtab ~/projects/infra

# Each tab maintains independent state:
# - Picker on/off
# - Terminal panes
# - Stacked build/test panes
# - LazyGit (uses tab's repo)
# - Vibe/Copilot
```

## Important Notes

## Important Notes

**Picker Toggle**: `space m f` specifically toggles the Yazi picker panel (named "hxyz-side-panel"). It won't close other panes you've created, allowing you to safely stack terminal/build panes alongside the picker.

## Requirements

Before installing HXYZ, ensure you have the following installed:

- **Zellij** - Terminal multiplexer
- **Yazi** - File manager
- **Helix** (or `hx`) - Text editor
- **Python 3** - For the install script

## Installation

### Using the Install Script

Note: the install script also creates a 'hz' symlink so that after installation you can open zellij + helix with either `hz` or `hxyz`

1. Navigate to the HXYZ directory:
   ```bash
   cd ./hxyz
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
   mkdir -p ~/.config/hxyz
   cp config/yazi.toml ~/.config/hxyz/yazi.toml
   ```

3. Add the keybinding to your Helix config (`~/.config/helix/config.toml`):
   ```toml
   [keys.normal.space.m]
   f = ':sh hxyz toggle "%{buffer_name}"'
   ```

## Usage

### Using the Keybinding

While editing in Helix (running within zellij):

1. Press `space` (space leader key)
2. Press `m` (group key)
3. Press `f` (file picker key)

This toggles a file picker pane on the left. You can then:
- Navigate files with arrow keys or `j`/`k`
- Open files with `Enter`
- Select multiple files
- Close the picker with `q` or `ESC`

### Using the Command

You can also run HXYZ directly from the terminal:

```bash
# Start HXYZ in current directory
hxyz

# Start with custom session name
hxyz -s myproject

# Create a new tab for a different repository
hxyz newtab ~/projects/frontend

# In an empty Zellij tab, start Helix
hxyz

# Show usage information
hxyz --help
```

## Working with Tabs and Panes

HXYZ supports a flexible multi-repo workflow with per-tab layouts:

### Per-Tab Layout

Each Zellij tab can have its own independent layout:
- **Left**: Yazi file picker (toggleable with `space m f`)
- **Right**: Helix editor (primary pane)
- **Right (stacked)**: Additional terminal/build panes created manually
- **Bottom**: Terminal pane (toggleable with `space m t`)
- **Floating**: Per-tab LazyGit (`space m g`) and Vibe/Copilot (`space m v`)

### Creating Tabs for Different Repos

**Option 1: Using hxyz command**
```bash
hxyz newtab ~/projects/backend
hxyz newtab ~/projects/frontend
hxyz newtab ~/projects/infrastructure
```

**Option 2: Using native Zellij**
1. Press `Ctrl-t` then `n` to create a new tab
2. Navigate to your repo directory
3. Run `hxyz` to start Helix in the new tab

### Working with Stacked Panes

Create additional panes for running build tools, tests, or terminals:

**Native Zellij Commands:**
- `Ctrl-p` then `d` - Create pane below (stacked)
- `Ctrl-p` then `r` - Create pane to the right
- `Ctrl-p` then `x` - Close current pane
- `Ctrl-p` then `h`/`j`/`k`/`l` - Navigate between panes
- `Ctrl-p` then `+`/`-` - Resize panes

**Example Workflow:**
1. Edit code in Helix
2. Press `Ctrl-p` then `d` to create a terminal below
3. Run `sbt` or `npm run dev` in the terminal
4. Press `Ctrl-p` then `k` to return to Helix
5. Both panes coexist with the picker toggle

### Per-Tab Floating Panes

Floating panes are scoped to each tab:

- **LazyGit** (`space m g` in Helix):
  - Each tab has its own LazyGit instance
  - Uses the correct repository directory for that tab
  - Closes automatically when you exit LazyGit
  
- **Vibe/Copilot** (`space m v` in Helix):
  - Each tab has its own Copilot CLI instance
  - Pass file context: In Helix, position cursor and press `space m v`
  - Independent per tab for context isolation

### Tab Isolation

All operations are tab-scoped:
- Toggling the picker in Tab 1 doesn't affect Tab 2
- Each tab's LazyGit works with that tab's repository
- Terminal toggles are per-tab
- Stacked panes are per-tab
- Floating panes are per-tab

## How It Works

### The File Picker Flow

1. **Toggle Picker**: Press `space m f` in Helix to toggle the picker pane
2. **Browse Files**: Use Yazi to navigate the file system
3. **Select & Open**: Choose files to open in Helix
4. **Auto-focus**: Helix pane automatically receives focus when you select files

### Session Management

HXYZ creates Zellij sessions with auto-generated names or custom names:
- Default format: `hxyz-{process-id}`
- Custom name: `hxyz -s myproject` creates a session named exactly `myproject`

This allows multiple independent HXYZ sessions without conflicts.

## Configuration

### Yazi Configuration

The HXYZ installation includes an optimized `yazi.toml` configuration file at:
```
~/.config/xyz/yazi.toml
```

This configuration is tailored for use with HXYZ and Helix integration. You can customize it further if needed.

### Environment Variables

You can customize HXYZ behavior with environment variables:

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
[keys.normal.space.m]
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

### "hxyz already exists" error

**Problem**: HXYZ installation detects an existing hxyz at `~/.local/bin/hxyz`

**Solution**: Either remove the existing file or verify it's the version you want:
```bash
rm ~/.local/bin/hxyz
python3 install.py
```

### "space m f already exists" error

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

HXYZ installation is unintrusive, so uninstalling is simple:

```bash
# Remove the hxyz script
rm ~/.local/bin/hxyz

# Remove yazi configuration
rm -rf ~/.config/xyz

# Remove the keybinding from ~/.config/helix/config.toml
# (Edit the file and remove the [keys.normal.space.m] section)
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
~/.local/bin/hxyz              # Executable script
~/.config/helix/config.toml    # Helix config with keybinding (modified during install)
~/.config/xyz/
├── yazi.toml                  # Yazi configuration
└── plugins/
    └── auto-layout.yazi       # Auto-layout plugin for Yazi
```

### Session Layout

When you toggle the picker, HXYZ creates:
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

To improve HXYZ:
1. Edit `bin/hxyz`
2. Test with `hxyz toggle`
3. Report issues or suggest improvements

## License

HXYZ is provided as-is. Use at your own risk.

## Credits

HXYZ integrates:
- **Zellij** - Terminal multiplexer (https://zellij.dev)
- **Yazi** - File manager (https://yazi.rs)
- **Helix** - Text editor (https://helix-editor.com)

---

**Version**: 1.0  
**Last Updated**: 2026-05-15  
**Installed at**: `~/Projects/hxyz`
