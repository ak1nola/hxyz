# HXYZ

A combination of non-intrusive cli tools that help me focus on my coding. It integrates Mitos (with Helix fallback) with Yazi, LazyGit and Zellij.

It is loosely based on [zide](https://github.com/josephschmitt/zide) - but, hopefully, a little more lightweight and simpler.

Note: Mitos is a Helix fork with more way features directly integrated e.g. better git and file explorer.

## What is HXYZ?

HXYZ is a shell script that integrates three powerful terminal tools - creating a richer keyboard-driven development workflow:
- **[Mitos])(https://github.com/mitos-editor/mitos) (`ms`)** - The preferred editor; falls back to **[Helix](https://helix-editor.com) (`hx`)** when unavailable
- **[Zellij](https://zellij.dev)** - A terminal multiplexer (similar to tmux)
- **[Yazi](https://yazi.rs)** - A blazing fast file manager

## Features

- **Multi-Repo Sessions**: Work on multiple repositories in one Zellij session, each in its own zellij tab
- **Per-Tab Layouts**: Each tab has independent picker, editor, terminal, and floating panes for lazygit and yazi
- **Quick File Picker**: Open/show Yazi with `m f` in a right-aligned float (30% width, full height). `q` closes a focused yazi pane
- **Floating Terminal**: Open/show a bottom-aligned terminal with `m t` (full width, 30% height). There's no close shortcut. This pane stays open in the background until it's manually closed
- **Editor Startup**: Running `hxyz` or `hz` launches `ms`, or `hx` if `ms` is unavailable
- **Seamless Navigation**: Browse files in Yazi and open selections directly in the originating editor
- **Session Management**: Auto-creates named Zellij sessions for organization
- **Configuration Support**: Includes optimized Yazi configuration
- **Non-Destructive Install**: Safe installation with conflict detection
- **Zellij**: use normal zellij shortcuts for navigating panes and tabs. For instance, `alt+f`/`opt+f` toggles floating zellij panes. This also means you can open a zellij session directly and use hxyz commands within it. 

## Requirements

For the Zellij implementation, install:

- Zellij 0.45.1
- Yazi
- Mitos (`ms`), or Helix (`hx`) as fallback
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
- adds HXYZ keybindings to `~/.config/mitos/config.toml` when `ms` is available, otherwise `~/.config/helix/config.toml` for `hx` (not both)
- asks before replacing a changed `hxyz` executable or updating each differing managed keybinding
- leaves existing Yazi configuration files untouched
- checks for existing files before modifying them

Use `--dry-run` to preview changes, `--verbose` for detailed output, or
`--no-dep-check` to skip non-editor dependency checks (editor selection still requires `ms` or `hx`):

```bash
python3 install.py --dry-run
```

The selected editor's config must already exist. A missing Mitos config is reported
as an error even if `hx` is also installed; it does not silently select Helix.
The installer does not build plugins, download packages, or install dependencies.

### Manual installation

```bash
mkdir -p ~/.local/bin ~/.config/hxyz
cp hxyz ~/.local/bin/hxyz
chmod +x ~/.local/bin/hxyz
# Copy only if you do not already have an HXYZ Yazi config:
cp -n yazi.toml ~/.config/hxyz/yazi.toml
```

Merge the bindings from `keybinding_config.txt` into the selected editor's config
under `[keys.normal.m]`; do not add a duplicate table or overwrite unrelated keys.
Make sure `~/.local/bin` is on `PATH`.

## Editor Keybindings

The installer adds these bindings under `[keys.normal.m]`:

| Binding | Action |
| --- | --- |
| `m f` | Open/show the right floating Yazi picker |
| `m t` | Open/show the bottom floating terminal |
| `m g` | Open LazyGit in a Zellij floating pane |
| `m o` | Open Copilot CLI in a Zellij floating pane |
| `m T` | Create a new Zellij tab in the current directory |

## Quick Start

Start or attach to a Zellij session. New sessions open Mitos, falling back to Helix:

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
├── keybinding_config.txt # Shared Mitos/Helix keybindings
├── yazi.toml            # Yazi configuration
├── README.md
└── ZELLIJ.md            # Detailed Zellij documentation
```

## Floating layout and lifecycle

| Pane | Position | Width | Height |
| --- | --- | --- | --- |
| Editor | Main tiled pane | Available area | Available area |
| Yazi (`files`) | x=70%, y=0% | 30% | 100% |
| Terminal (`terminal`) | x=0%, y=70% | 100% | 30% |
| LazyGit | Centered | 90% | 90% |
| Copilot | Centered | 80% | 80% |

Picker and terminal commands look for a matching non-plugin floating pane in the
current tab. If present, they show the floating layer and focus that pane; if
absent, they create one. Other floating panes remain open with their processes
and geometry intact. Running the same command again leaves that pane open.
No helper plugin is needed.

Native layer controls still work:

```bash
zellij action hide-floating-panes
zellij action show-floating-panes
zellij action close-pane   # Close the focused pane
```

With default Zellij bindings, `Ctrl-p` then `w` toggles the floating layer,
and `Ctrl-p` then `x` closes the focused pane. Custom/locked keymaps may differ;
use your configured navigation and pane controls.

Geometry is relative to Zellij's available pane area, with borders, reserved UI
rows, and cell rounding.
Old tiled panes in existing sessions are not automatically migrated: close them
before opening the new floats.

## File picker flow

1. In the editor, press `m f`. The current buffer path chooses the picker's starting directory.
2. Browse/select files in Yazi and open them with `Enter`.
3. Yazi invokes HXYZ's internal `edit` callback, which focuses the originating editor and sends an `:open` command. Directory selections use `:cd`.

Multiple selected files and paths containing spaces are supported. Opening an
existing picker does not reset its browsing directory or retarget its original
editor callback. Quit Yazi and reopen it to start a new context.

Yazi's `q` exits its process and closes its floating picker pane.
The picker is launched with Zellij's `--close-on-exit` option.
HXYZ does not add custom automatic hiding on selection.

### Example Multi-Repo Workflow

```bash
# Start a session with ms (or hx if ms is unavailable)
hxyz -s work

# Tab 1 (auto-created): Backend repository
# - Open files with m f
# - Run LazyGit with m g (tab-specific)
# - Open terminal with m t
# - Use Copilot with m o (tab-specific)

# Create Tab 2 for frontend (only works from terminal)
hxyz newtab ~/projects/frontend
# Run hxyz in the new tab to start its editor

# Create Tab 3 for infrastructure  
hxyz newtab ~/projects/infra

# Each tab maintains independent state:
# - Picker and terminal processes
# - Terminal panes
# - Stacked build/test panes
# - LazyGit (uses tab's repo)
# - Vibe/Copilot
```

## Important Notes

**Pane lifecycle**: `m f` and `m t` show/focus the existing float in the current
tab; they never close it. After you close it with Zellij, the next invocation
creates a new one. Quitting Yazi with `q` also closes its picker pane.
An existing picker keeps its directory and original editor
target even when invoked with a different path.

Opening an HXYZ float pane shows the tab's floating layer and focuses that pane.
Other floating panes remain open; HXYZ does not suppress or close them.
Use native Zellij commands to hide/show the current floating layer or close the
focused pane. Dimensions are relative to Zellij's available pane area,
subject to borders and rounding.
Old tiled panes in existing sessions are not migrated; close them before adopting
the floating layout. Existing sessions are attached without replacing their editor.


## Troubleshooting

- **No editor found:** put `ms` or `hx` on `PATH`. `ms` always wins when both exist.
- **Config not found:** create the selected editor's config before installation.
- **Files not opening:** verify the originating editor pane still exists, Yazi uses
  the HXYZ opener, and `jq`/Zellij are available. Close/reopen a stale picker.
- **Upgrading from the plugin-based version:** unload the old helper through
  Zellij's plugin manager or start a fresh session. The installer does not stop
  running plugins or modify existing panes. Recover any previously suppressed
  panes through Zellij's pane manager. Close/reopen an existing picker to use
  the new close-on-exit behavior.
- **Shortcut unchanged:** the installer preserves bindings when you decline an
  update; rerun it to approve that binding.

## Uninstallation

Remove `~/.local/bin/hxyz` and the `~/.local/bin/hz` symlink, remove the managed
bindings from the editor config you installed into, and remove
`~/.config/hxyz/yazi.toml` if no longer needed. Keep unrelated configuration.
If upgrading from the plugin-based version, the unused
`~/.config/hxyz/floating-panes.wasm` can also be removed.

## License

HXYZ is provided as-is. Use at your own risk.
