# WHXY vs THXY Comparison

## Overview

Both WHXY and THXY provide seamless file picker integration for Helix editor using yazi. The main difference is the terminal multiplexer used.

## Component Comparison

| Component | THXY | WHXY |
|-----------|------|------|
| **Terminal** | tmux | WezTerm |
| **Editor** | Helix | Helix |
| **File Manager** | yazi | yazi |
| **CLI Command** | `thxy` / `th` | `whxy` / `wh` |
| **Config Dir** | `~/.config/thxy` | `~/.config/whxy` |

## Key Differences

### Terminal Multiplexing

**THXY (tmux-based):**
- Requires tmux to be installed separately
- Uses tmux sessions, windows, and panes
- Widely supported across all platforms
- Can detach/reattach sessions
- Standard terminal multiplexer workflow

**WHXY (WezTerm-based):**
- WezTerm has built-in pane management
- No additional multiplexer needed
- GPU-accelerated rendering
- Better font rendering and ligatures
- Native image preview support
- Requires WezTerm specifically

### Pane Management

**THXY:**
```bash
tmux split-window -h -b -l 20%
tmux select-pane -T "picker"
tmux send-keys -t "$pane_id" Escape
```

**WHXY:**
```bash
wezterm cli split-pane --left --percent 20
wezterm cli set-tab-title --pane-id "$picker_id" "picker"
wezterm cli send-text --pane-id "$pane_id" --no-paste
```

### Installation

Both use Python-based installers with the same features:
- Dependency checking
- Conflict detection
- Dry-run mode
- Verbose output
- Clean uninstall

## Feature Parity

Both versions support:
- ✅ File picker toggle (`space + m + f`)
- ✅ LazyGit integration (`space + m + g`)
- ✅ Copilot CLI integration (`space + m + o`)
- ✅ Multi-file selection
- ✅ Auto-focus on file open
- ✅ Custom yazi configuration
- ✅ Helix keybinding injection

## Performance

**THXY:**
- Depends on terminal emulator performance
- tmux adds minimal overhead
- Works with any terminal

**WHXY:**
- GPU-accelerated rendering via WezTerm
- Potentially faster rendering
- Limited to WezTerm

## Use Cases

### Choose THXY if you:
- Already use tmux for other workflows
- Want maximum terminal compatibility
- Need session persistence/detachment
- Work on remote servers via SSH
- Prefer a widely-adopted tool

### Choose WHXY if you:
- Already use WezTerm as your terminal
- Want GPU-accelerated rendering
- Prefer fewer dependencies
- Value better font/ligature rendering
- Want native image previews
- Don't need session persistence

## Migration

Switching between THXY and WHXY is simple:

**From THXY to WHXY:**
```bash
# Uninstall THXY
cd thxy
python3 install.py uninstall

# Install WHXY
cd wezTerm
python3 install.py
```

**From WHXY to THXY:**
```bash
# Uninstall WHXY
cd wezTerm
python3 install.py uninstall

# Install THXY
cd ..
python3 install.py
```

Both use different keybinding keys (`m` submenu), so they won't conflict if installed simultaneously.

## Architecture

### THXY Flow
```
User presses space+m+f in Helix
  ↓
:sh thxy picker "%{buffer_name}"
  ↓
thxy creates/toggles tmux pane
  ↓
Yazi launches with $EDITOR set to thxy
  ↓
User selects files
  ↓
thxy sends :open command to Helix pane
```

### WHXY Flow
```
User presses space+m+f in Helix
  ↓
:sh whxy picker "%{buffer_name}"
  ↓
whxy creates/toggles WezTerm pane
  ↓
Yazi launches with $EDITOR set to whxy
  ↓
User selects files
  ↓
whxy sends :open command to Helix pane
```

## Conclusion

Both versions provide the same functionality with excellent user experience. The choice depends primarily on your terminal emulator preference:

- **THXY** = tmux universality + session management
- **WHXY** = WezTerm performance + simpler setup

You can even install both and use whichever fits your current environment!
