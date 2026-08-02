# WHXY Quick Start Guide

## 1. Prerequisites

Install the required dependencies:

```bash
# macOS (using Homebrew)
brew install --cask wezterm
brew install yazi helix

# Linux (Arch)
sudo pacman -S wezterm yazi helix

# Linux (Ubuntu/Debian) - WezTerm from official repo
# See: https://wezfurlong.org/wezterm/install/linux.html
sudo apt install yazi helix
```

## 2. Installation

```bash
cd wezTerm
python3 install.py
```

The installer will:
- ✅ Check dependencies
- ✅ Install `whxy` and `wh` commands
- ✅ Configure yazi for WHXY
- ✅ Add Helix keybindings

## 3. Usage

### Start WHXY

```bash
# Method 1: Use the whxy command
whxy

# Method 2: Use the shorter wh command
wh

# Method 3: If already in WezTerm, just start Helix
hx
```

### File Picker

Once in Helix:

1. Press `Space` + `m` + `f` to toggle the file picker
2. Navigate with arrow keys or `j`/`k`
3. Press `Enter` to open a file
4. Press `q` or `ESC` to close the picker

### Git Integration

Press `Space` + `m` + `g` to open LazyGit

### Copilot CLI

Press `Space` + `m` + `o` to open GitHub Copilot CLI

## 4. Configuration

### Custom Yazi Config

Edit `~/.config/whxy/yazi.toml` to customize yazi behavior.

### Custom Keybindings

Edit `~/.config/helix/config.toml` to change keybindings:

```toml
[keys.normal.m]
f = ':sh whxy picker "%{buffer_name}"'  # File picker
g = ':sh whxy git'                      # LazyGit
o = ':sh whxy vibe "%{buffer_name}" %{cursor_line}'  # Copilot
```

### Environment Variables

```bash
# Use custom config directory
export WHXY_HOME=~/.config/my-whxy

# Disable custom yazi config (use system default)
export WHXY_USE_YAZI_CONFIG=false
```

## 5. Troubleshooting

### WezTerm CLI not found

**macOS:**
```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="/Applications/WezTerm.app/Contents/MacOS:$PATH"
```

**Linux:**
```bash
# Usually in PATH by default
which wezterm  # Should show: /usr/bin/wezterm
```

### Files not opening

- Make sure you're running Helix inside WezTerm
- Check that `WEZTERM_PANE` environment variable is set:
  ```bash
  echo $WEZTERM_PANE  # Should show a number
  ```

### Picker pane won't close

- Press `Space` + `m` + `f` again to toggle it off
- Or press `q` in yazi to quit

## 6. Uninstallation

```bash
cd wezTerm
python3 install.py uninstall
```

This removes:
- `~/.local/bin/whxy` and `~/.local/bin/wh`
- `~/.config/whxy/`
- WHXY keybindings from `~/.config/helix/config.toml`

## 7. Tips & Tricks

### Multi-file Selection

In the file picker (yazi):
- Press `Space` to select multiple files
- Press `Enter` to open all selected files

### Quick Directory Change

1. Open picker (`Space` + `m` + `f`)
2. Navigate to a directory
3. Press `Enter` on a directory (not a file)
4. Helix changes to that directory

### Viewing Current Directory

In Helix, check the status bar at the bottom to see your current working directory.

### Using with Existing WezTerm Setup

WHXY works alongside your existing WezTerm configuration. It only uses the CLI for pane management.

## 8. Comparison with THXY

If you're familiar with THXY:

- **Same keybindings**: `Space` + `m` + `f/g/o`
- **Same workflow**: Toggle picker, select files, auto-open
- **Different backend**: WezTerm CLI instead of tmux
- **No session management**: WezTerm doesn't have tmux-style sessions

See `COMPARISON.md` for detailed differences.

## 9. Advanced Usage

### Custom Picker Width

Edit `bin/whxy` and change the `--percent 20` value:

```bash
# Change from 20% to 30%
wezterm cli split-pane --left --percent 30 ...
```

### Debug Mode

Uncomment debug logging in `bin/whxy`:

```bash
# Enable debug output
exec 2>>/tmp/whxy.log; set -x
```

Then tail the log:
```bash
tail -f /tmp/whxy.log
```

## 10. Getting Help

- Check `README.md` for full documentation
- Check `COMPARISON.md` for WHXY vs THXY differences
- Run `whxy --help` for command usage
- Report issues on the project repository

---

**Version**: 1.0  
**Last Updated**: 2026-07-31
