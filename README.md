# HXYZ

A powerful simple picker integration that brings seamless file selection to Helix through Yazi and Zellij terminal multiplexing.

It is loosely based on [zide](https://github.com/josephschmitt/zide) - but, hopefully, a little more lightweight and simpler.

## What is HXYZ?

HXYZ is a shell script that integrates three powerful terminal tools - creating a richer keyboard-driven development workflow:
- **[Helix](https://helix-editor.com)** - A modern text editor
- **[Zellij](https://zellij.dev)** - A terminal multiplexer (like tmux)
- **[Yazi](https://yazi.rs)** - A blazing fast file manager

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
- **Easy Tab Creation**: Use `hxyz newtab ~/path/to/repo` or native Zellij commands (`Ctrl-t n`). Within Helix Editor, custom keybindings (all starting with 'm') are added for creating files, lazygit, blame or terminal panes.
- **Easy cross pane navigation**: all tabs and panes are full zellij components and normal zellij keybindings are used for navigation. Note that I typically run zellij in locked mode 

## Supported Multiplexer

HXYZ currently supports Zellij.

## Requirements

For the Zellij implementation, install:

- Zellij
- Yazi
- Helix (`hx` or `helix`)
- Python 3
- `jq`
- LazyGit (for `hxyz git`)
- GitHub Copilot CLI (for `hxyz vibe`). You can use any ai cli tool instead of copilot.

## Installation

Run the installer from the repository root:

```bash
python3 install.py
```

The installer:

- installs `hxyz` and the `hz` shortcut/symlink in `~/.local/bin/`
- installs the HXYZ Yazi configuration in `~/.config/hxyz/`
- adds the HXYZ keybindings to `~/.config/helix/config.toml`
- asks before replacing a changed `hxyz` executable or updating each differing managed keybinding
- leaves existing Yazi configuration files untouched
- checks for existing files before modifying them

Use `--dry-run` to preview changes, `--verbose` for detailed output, or
`--no-dep-check` to skip dependency checks:

```bash
python3 install.py --dry-run
```

## Helix Editor Keybindings

The installer adds these bindings under `[keys.normal.m]`:

| Binding | Action |
| --- | --- |
| `m f` | Toggle the Yazi file picker in a Zellij side pane |
| `m g` | Open LazyGit in a Zellij floating pane |
| `m o` | Open Copilot CLI in a Zellij floating pane |
| `m T` | Create a new Zellij tab in the current directory |

## Quick Start

Start or attach to a Zellij session and open Helix:

```bash
hxyz
```

Useful commands:

```bash
hxyz --help
hxyz -s zellij_session_name
hxyz newtab ~/path/to/repository
hxyz terminal
hxyz git
hxyz vibe
```

Each Zellij tab can represent a different 'IDE' instance. The picker, terminal,
LazyGit, and Copilot panes are scoped to the current tab.

## Documentation

See [`ZELLIJ.md`](ZELLIJ.md) for the complete Zellij guide,
including configuration, multi-repository workflows, troubleshooting, and
uninstallation.

## Repository Layout

```text
.
├── hxyz                 # Zellij implementation
├── install.py           # Installer
├── keybinding_config.txt # Helix editor keybindings
├── yazi.toml            # Yazi configuration
├── README.md
└── ZELLIJ.md            # Detailed Zellij documentation
```

### Example Multi-Repo Workflow

```bash
# Start a session i.e. a zellij tab with hx running in it
hxyz -s work

# Tab 1 (auto-created): Backend repository
# - Show git blame for current line with m b (toggles picker)
# - Open files with m f (toggles picker)
# - Run LazyGit with m g (tab-specific)
# - Open terminal with m t (toggles picker)
# - Use Copilot with m v (tab-specific)

# Create Tab 2 for frontend (only works from terminal)
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

**Picker Toggle**: `space m f` specifically toggles the Yazi picker panel (named "hxyz-side-panel"). It won't close other panes you've created, allowing you to safely stack terminal/build panes alongside the picker.


## License

HXYZ is provided as-is. Use at your own risk.
