# HXYZ

HXYZ integrates [Helix](https://helix-editor.com), [Yazi](https://yazi.rs), and
[Zellij](https://zellij.dev) into a keyboard-driven development workflow.
It provides a file picker, per-tab terminal panes, LazyGit, and Copilot CLI
floating panes from within Helix.

## Supported Multiplexers

The repository is organized by terminal multiplexer. Zellij is currently the
supported implementation:

| Multiplexer | Directory | Command | Documentation |
| --- | --- | --- | --- |
| Zellij | [`zellij/`](zellij/) | `hxyz` | [`zellij/README.md`](zellij/README.md) |

Shared multiplexer-selection tooling is kept in [`common/`](common/). The
`zwt` command detects the active multiplexer and dispatches to the matching
implementation when one is available.

## Requirements

For the Zellij implementation, install:

- Zellij
- Yazi
- Helix (`hx` or `helix`)
- Python 3
- `jq`
- LazyGit (for `hxyz git`)
- GitHub Copilot CLI (for `hxyz vibe`)

## Installation

Run the installer from the implementation directory:

```bash
cd zellij
python3 install.py
```

The installer:

- installs `hxyz` and the `hz` shortcut in `~/.local/bin/`
- installs the shared `zwt` dispatcher
- installs the HXYZ Yazi configuration in `~/.config/hxyz/`
- adds the HXYZ keybindings to `~/.config/helix/config.toml`
- checks for existing files before modifying them

Use `--dry-run` to preview changes, `--verbose` for detailed output, or
`--no-dep-check` to skip dependency checks:

```bash
python3 install.py --dry-run
```

## Keybindings

The installer adds these bindings under `[keys.normal.space.m]`:

| Binding | Action |
| --- | --- |
| `space m f` | Toggle the Yazi file picker |
| `space m g` | Open LazyGit in a floating pane |
| `space m o` | Open Copilot CLI in a floating pane |

## Quick Start

Start or attach to a Zellij session and open Helix:

```bash
hxyz
```

Useful commands:

```bash
hxyz --help
hxyz newtab ~/path/to/repository
hxyz terminal
hxyz git
hxyz vibe
```

Each Zellij tab can represent a different repository. The picker, terminal,
LazyGit, and Copilot panes are scoped to the current tab.

## Documentation

See [`zellij/README.md`](zellij/README.md) for the complete Zellij guide,
including configuration, multi-repository workflows, troubleshooting, and
uninstallation.

## Repository Layout

```text
.
├── common/
│   └── bin/zwt          # Shared multiplexer dispatcher
├── zellij/
│   ├── bin/hxyz         # Zellij implementation
│   ├── config/          # Yazi configuration
│   ├── install.py       # Installer
│   └── README.md        # Detailed Zellij documentation
└── README.md
```

## License

HXYZ is provided as-is. Use at your own risk.
