# HXYZ - Helix Editor Integration Suite

A collection of terminal integrations that bring seamless file picker functionality to the Helix text editor using yazi file manager.

## Available Variants

This repository contains three variants of the same concept, each using a different terminal multiplexer:

### 🔷 HXYZ (Zellij-based) - Original
**Location:** [`zellij/`](zellij/)

Uses Zellij for terminal multiplexing.

```bash
cd zellij/
python3 install.py
```

**Best for:**
- Modern terminal multiplexer experience
- Those wanting built-in layouts
- Tab-based workflow preference
- Rust-based tooling enthusiasts

**This is the only well tested version**


### 🖥️ THXY (tmux-based)
**Location:** [`tmux/`](tmux/)

Uses tmux for terminal multiplexing.

```bash
cd tmux/
python3 install.py
```

**Best for:**
- Users who already use tmux
- Those needing session persistence
- Remote work via SSH
- Maximum terminal compatibility

### ⚡ WHXY (WezTerm-based)
**Location:** [`wezTerm/`](wezTerm/)

Uses WezTerm's built-in pane management.

```bash
cd wezTerm/
python3 install.py
```

**Best for:**
- WezTerm users
- GPU-accelerated rendering
- Simpler setup (one less dependency)
- Better font/ligature rendering

## Unified Command: `zwt`

The repository includes a unified command `zwt` (Zellij/WezTerm/Tmux) that automatically detects your current multiplexer and routes commands to the appropriate script (hxyz, thxy, or whxy).

**Location:** [`common/bin/zwt`](common/bin/zwt)

The `zwt` command:
- Auto-detects which multiplexer you're running (Zellij, WezTerm, or tmux)
- Routes commands to the correct script automatically
- Uses the `MULTIPLEXER` environment variable if set
- Provides a consistent interface across all variants

**Usage:**
```bash
# Use zwt instead of hxyz/thxy/whxy - it works in any multiplexer
zwt picker      # Toggle file picker
zwt git         # Open LazyGit
zwt vibe        # Open Copilot CLI
```

The unified keybindings in [`common/config/keybinding_config.txt`](common/config/keybinding_config.txt) use `zwt` to work seamlessly across all three multiplexers.

## Quick Comparison

| Feature | HXYZ (Zellij) | THXY (tmux) | WHXY (WezTerm) |
|---------|---------------|-------------|----------------|
| **Multiplexer** | Zellij | tmux (external) | WezTerm (built-in) |
| **Dependencies** | Zellij + terminal | tmux + terminal | WezTerm only |
| **Session Management** | ✅ Yes | ✅ Yes | ❌ No |
| **Performance** | Fast (Rust) | Terminal-dependent | GPU-accelerated |
| **Remote SSH** | ✅ Good | ✅ Excellent | ⚠️ Limited |
| **Setup Complexity** | Medium | Medium | Simple |
| **Config Language** | KDL | Config file | Lua |

## Features (Both Variants)

- 🎯 **File Picker**: Toggle yazi picker with `space + m + f`
- 🔀 **Git Integration**: Open LazyGit with `space + m + g`
- 🤖 **AI Assistant**: Open Copilot CLI with `space + m + o`
- 🔄 **Multi-file Selection**: Select and open multiple files at once
- ⚡ **Auto-focus**: Helix automatically focuses after file selection
- 🛡️ **Safe Install**: Non-destructive installation with conflict detection

## What Each Variant Provides

Both variants integrate three powerful tools:
- **Helix** (`hx`) - Modern text editor
- **yazi** - Fast file manager
- **Terminal Multiplexer** - tmux or WezTerm

### Keybindings (Identical for Both)

While editing in Helix:

| Key Combo | Action |
|-----------|--------|
| `space` + `m` + `f` | Toggle file picker |
| `space` + `m` + `g` | Open LazyGit |
| `space` + `m` + `o` | Open Copilot CLI |

## Installation

### Prerequisites

Both variants require:
- **Helix** or `hx` text editor
- **yazi** file manager
- **Python 3** for the installer

Additionally:
- **THXY** requires: tmux
- **WHXY** requires: WezTerm

### Install THXY (tmux variant)

```bash
cd tmux
python3 install.py
```

This installs:
- `~/.local/bin/thxy` and `~/.local/bin/th` commands
- `~/.config/thxy/` configuration
- Helix keybindings

### Install WHXY (WezTerm variant)

```bash
cd wezTerm
python3 install.py
```

This installs:
- `~/.local/bin/whxy` and `~/.local/bin/wh` commands
- `~/.config/whxy/` configuration
- Helix keybindings

### Can I Install Multiple Variants?

Yes! All three variants can coexist peacefully:
- They use different command names (`hxyz` vs `thxy` vs `whxy`)
- They use different config directories (`~/.config/hxyz` vs `~/.config/thxy` vs `~/.config/whxy`)
- They all support the unified `zwt` command for cross-multiplexer compatibility
- The keybindings can use `zwt` to work with any installed variant

## Usage

After installation, you can use either the specific command or the unified `zwt`:

```bash
# Specific commands
hxyz        # Zellij variant
thxy        # or just: th (tmux variant)

# WHXY (WezTerm variant)
whxy        # or just: wh
```

Then use the keybindings inside Helix:
- `space + m + f` - File picker
- `space + m + g` - LazyGit
- `space + m + o` - Copilot CLI

## Documentation

Each variant has complete documentation in its directory:

### HXYZ Documentation
- [`zellij/README.md`](zellij/README.md) - Complete guide
- [`zellij/install.py`](zellij/install.py) - Installation script

### THXY Documentation
- [`tmux/README.md`](tmux/README.md) - Complete guide
- [`tmux/install.py`](tmux/install.py) - Installation script

### WHXY Documentation
- [`wezTerm/README.md`](wezTerm/README.md) - Complete guide
- [`wezTerm/QUICKSTART.md`](wezTerm/QUICKSTART.md) - Quick start
- [`wezTerm/COMPARISON.md`](wezTerm/COMPARISON.md) - Detailed comparison
- [`wezTerm/install.py`](wezTerm/install.py) - Installation script

### Common Files
- [`common/bin/zwt`](common/bin/zwt) - Unified multiplexer proxy command
- [`common/config/keybinding_config.txt`](common/config/keybinding_config.txt) - Unified Helix keybindings

## Architecture

### HXYZ (Zellij variant)
```
User → Helix (in Zellij pane) → hxyz picker
  ↓
Zellij creates yazi pane
  ↓
User selects files in yazi
  ↓
hxyz sends :open to Helix pane
```

### THXY (tmux variant)
```
User → Helix (in tmux pane) → thxy picker
  ↓
tmux creates yazi pane
  ↓
User selects files in yazi
  ↓
thxy sends :open to Helix pane
```

### WHXY (WezTerm variant)
```
User → Helix (in WezTerm pane) → whxy picker
  ↓
WezTerm creates yazi pane
  ↓
User selects files in yazi
  ↓
whxy sends :open to Helix pane
```

## Which Should I Choose?

### Choose HXYZ if:
- ✅ You already use Zellij
- ✅ You want modern terminal multiplexing
- ✅ You prefer Rust-based tools
- ✅ You like built-in layout management
- ✅ You want tab-based workflow

### Choose THXY if:
- ✅ You already use tmux daily
- ✅ You work on remote servers via SSH
- ✅ You need session persistence (detach/reattach)
- ✅ You want maximum terminal compatibility
- ✅ You prefer battle-tested tools

### Choose WHXY if:
- ✅ You already use WezTerm
- ✅ You want GPU-accelerated rendering
- ✅ You prefer fewer dependencies
- ✅ You value font rendering quality
- ✅ You work primarily on local machine

### Still Unsure?

If you're starting fresh and don't have a preference:
- **Zellij users**: Use HXYZ (native integration)
- **WezTerm users**: Use WHXY (simpler setup)
- **tmux users**: Use THXY (familiar workflow)
- **Neither**: Try WHXY first (easier to set up)

**Pro tip:** Use the unified `zwt` command with the `common/config/keybinding_config.txt` keybindings to work seamlessly across any installed variant.

## Uninstallation

All variants support clean uninstallation:

```bash
# HXYZ
cd zellij
python3 install.py uninstall
# THXY
cd tmux
python3 install.py uninstall

# WHXY
cd wezTerm
python3 install.py uninstall
```

## Troubleshooting

### Common to All Variants

**"Helix not found"**
```bash
# Install Helix
brew install helix        # macOS
sudo pacman -S helix      # Arch Linux
```

**"yazi not found"**
```bash
# Install yazi
brew install yazi         # macOS
sudo pacman -S yazi       # Arch Linux
```

### HXYZ Specific

**"zellij not found"**
```bash
brew install zellij       # macOS
sudo pacman -S zellij     # Arch Linux
# Or: cargo install zellij
```

### THXY Specific

**"tmux not found"**
```bash
brew install tmux         # macOS
sudo apt install tmux     # Ubuntu/Debian
sudo pacman -S tmux       # Arch Linux
```

### WHXY Specific

**"wezterm not found"**
```bash
brew install --cask wezterm    # macOS
# Linux: see https://wezfurlong.org/wezterm/install/linux.html
```

## Development

All three variants are standalone bash scripts with Python installers:

```
hxyz/
├── common/        # Shared utilities
│   ├── bin/zwt    # Unified proxy command
│   └── config/    # Unified keybindings
├── zellij/        # HXYZ variant
│   ├── bin/hxyz   # Main script
│   └── install.py # Installer
├── tmux/          # THXY variant
│   ├── bin/thxy   # Main script
│   └── install.py # Installer
└── wezTerm/       # WHXY variant
    ├── bin/whxy   # Main script
    └── install.py # Installer
```

## Credits

All three variants integrate:
- **Helix** - Modern text editor (https://helix-editor.com)
- **yazi** - Fast file manager (https://yazi.rs)

HXYZ uses:
- **Zellij** - Terminal multiplexer (https://zellij.dev)

THXY uses:
- **tmux** - Terminal multiplexer (https://github.com/tmux/tmux)

WHXY uses:
- **WezTerm** - GPU-accelerated terminal (https://wezfurlong.org/wezterm/)

Originally inspired by [zide](https://github.com/josephschmitt/zide).

## License

Provided as-is. Use at your own risk.

---

**Repository**: [ak1nola/hxyz](https://github.com/ak1nola/hxyz)  
**Version**: 1.0  
**Last Updated**: 2026-07-31
