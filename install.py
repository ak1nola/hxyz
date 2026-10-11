#!/usr/bin/env python3
"""
HXYZ Install Script
Manages installation of hxyz (Helix + Zellij + Yazi integration) with dependency checking
and safe configuration injection.
"""

import os
import re
import sys
import shutil
import argparse
import subprocess
from pathlib import Path


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    DIM = '\033[2m'


def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")


def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_error(msg):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")


def verbose(msg, verbose_flag):
    if verbose_flag:
        print(f"{Colors.DIM}  {msg}{Colors.RESET}")


class InstallContext:
    def __init__(self, dry_run=False, verbose_flag=False, no_dep_check=False):
        self.dry_run = dry_run
        self.verbose = verbose_flag
        self.no_dep_check = no_dep_check
        self.script_dir = Path(__file__).parent.resolve()
        self.home = Path.home()
        
        # Paths
        self.hxyz_src = self.script_dir / "hxyz"
        self.hxyz_dst = self.home / ".local" / "bin" / "hxyz"
        self.hz_symlink = self.home / ".local" / "bin" / "hz"
        
        self.yazi_src = self.script_dir / "yazi.toml"
        self.yazi_dst_dir = self.home / ".config" / "hxyz"
        self.yazi_dst = self.yazi_dst_dir / "yazi.toml"

        self.helix_config = self.home / ".config" / "helix" / "config.toml"
        self.keybinding_src = self.script_dir / "keybinding_config.txt"

    def check_dependencies(self):
        """Verify required dependencies are installed"""
        if self.no_dep_check:
            verbose("Skipping dependency check", self.verbose)
            return True
        
        dependencies = ["zellij", "yazi", "helix", "python3"]
        missing = []
        
        for dep in dependencies:
            # For helix, check both 'helix' and 'hx'
            if dep == "helix":
                hx_check = subprocess.run(
                    ["which", "hx"],
                    capture_output=True,
                    text=True
                )
                helix_check = subprocess.run(
                    ["which", "helix"],
                    capture_output=True,
                    text=True
                )
                if hx_check.returncode != 0 and helix_check.returncode != 0:
                    missing.append(dep)
            else:
                result = subprocess.run(
                    ["which", dep],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    missing.append(dep)
        
        if missing:
            print_error(f"Missing dependencies: {', '.join(missing)}")
            print_info("Install them and try again. Use --no-dep-check to skip this check.")
            return False
        
        verbose("All dependencies found", self.verbose)
        return True

    def check_hz_symlink_exists(self):
        """Check if hz symlink already exists in ~/.local/bin/"""
        if self.hz_symlink.is_symlink():
            try:
                if self.hz_symlink.resolve() == self.hxyz_dst.resolve():
                    verbose(f"hz already points to {self.hxyz_dst}", self.verbose)
                    return False
            except OSError as e:
                print_error(f"Failed to inspect existing hz symlink: {e}")
                return True

        if self.hz_symlink.exists() or self.hz_symlink.is_symlink():
            print_error(f"hz already exists at {self.hz_symlink}")
            print_info("Remove it or use a different installation path")
            return True
        verbose(f"hz not found at {self.hz_symlink} (good)", self.verbose)
        return False

    @staticmethod
    def _assignment(line):
        """Return a TOML assignment's key and value, excluding trailing comments."""
        match = re.match(r"^\s*([A-Za-z0-9_-]+)\s*=\s*(.*)$", line)
        if not match:
            return None

        value = match.group(2)
        quote = None
        escaped = False
        for index, char in enumerate(value):
            if escaped:
                escaped = False
            elif char == "\\" and quote == '"':
                escaped = True
            elif quote:
                if char == quote:
                    quote = None
            elif char in ("'", '"'):
                quote = char
            elif char == "#":
                value = value[:index].rstrip()
                break

        return match.group(1), value.strip()

    @classmethod
    def _table_contents(cls, content, table_name):
        """Return a table's line range and direct key assignments."""
        lines = content.splitlines(keepends=True)
        header = re.compile(r"^\s*\[([^\]]+)\]\s*(?:#.*)?$")
        start = None
        end = len(lines)
        for index, line in enumerate(lines):
            match = header.match(line)
            if not match:
                continue
            if start is not None:
                end = index
                break
            if match.group(1) == table_name:
                start = index

        assignments = {}
        if start is not None:
            for index in range(start + 1, end):
                assignment = cls._assignment(lines[index])
                if assignment:
                    key, value = assignment
                    assignments[key] = (value, index)
        return lines, start, end, assignments

    def confirm(self, prompt):
        """Ask for confirmation; return None if input is unavailable."""
        try:
            answer = input(f"{prompt} [y/N] ")
        except EOFError:
            print_error("No response received; cannot continue the requested update")
            return None
        return answer.strip().lower() in ("y", "yes")

    def install_hxyz(self):
        """Install or update hxyz, asking before replacing a changed executable."""
        if not self.hxyz_src.exists():
            print_error(f"hxyz script not found at {self.hxyz_src}")
            return False
        
        self.hxyz_dst.parent.mkdir(parents=True, exist_ok=True)

        if self.hxyz_dst.exists():
            try:
                if self.hxyz_src.read_bytes() == self.hxyz_dst.read_bytes():
                    print_success("hxyz is already up to date")
                    return True
            except OSError as e:
                print_error(f"Failed to compare hxyz files: {e}")
                return False

            if self.dry_run:
                print(f"  Would ask whether to update {self.hxyz_dst} from {self.hxyz_src}")
                return True

            update = self.confirm(f"Installed hxyz differs from {self.hxyz_src}. Update {self.hxyz_dst}?")
            if update is None:
                return False
            if not update:
                print_warning("Keeping the existing hxyz executable")
                return True
        
        if self.dry_run:
            print(f"  Would copy {self.hxyz_src} → {self.hxyz_dst}")
            return True
        
        try:
            shutil.copy2(self.hxyz_src, self.hxyz_dst)
            self.hxyz_dst.chmod(0o755)
            verbose(f"Copied hxyz to {self.hxyz_dst}", self.verbose)
            print_success("Installed hxyz to ~/.local/bin/hxyz")
            return True
        except Exception as e:
            print_error(f"Failed to install hxyz: {e}")
            return False

    def install_yazi_config(self):
        """Copy yazi.toml to ~/.config/hxyz/"""
        if not self.yazi_src.exists():
            print_error(f"yazi.toml not found at {self.yazi_src}")
            return False

        if self.yazi_dst.exists() or self.yazi_dst.is_symlink():
            print_warning(f"Keeping existing Yazi config at {self.yazi_dst}")
            return True
        
        self.yazi_dst_dir.mkdir(parents=True, exist_ok=True)
        
        if self.dry_run:
            print(f"  Would copy {self.yazi_src} → {self.yazi_dst}")
            return True
        
        try:
            shutil.copy2(self.yazi_src, self.yazi_dst)
            verbose(f"Copied yazi.toml to {self.yazi_dst}", self.verbose)
            print_success(f"Installed yazi config to ~/.config/hxyz/yazi.toml")
            return True
        except Exception as e:
            print_error(f"Failed to install yazi config: {e}")
            return False

    def create_hz_symlink(self):
        """Create hz symlink to hxyz executable"""
        self.hz_symlink.parent.mkdir(parents=True, exist_ok=True)

        if self.hz_symlink.is_symlink():
            try:
                if self.hz_symlink.resolve() == self.hxyz_dst.resolve():
                    print_success("'hz' symlink is already configured")
                    return True
            except OSError as e:
                print_error(f"Failed to inspect existing hz symlink: {e}")
                return False
        
        if self.dry_run:
            print(f"  Would create symlink {self.hz_symlink} → {self.hxyz_dst}")
            return True
        
        try:
            # Create symlink using hxyz_dst as absolute path
            self.hz_symlink.symlink_to(self.hxyz_dst)
            verbose(f"Created symlink hz -> hxyz at {self.hz_symlink}", self.verbose)
            print_success("Created 'hz' symlink to 'hxyz'")
            return True
        except Exception as e:
            print_error(f"Failed to create hz symlink: {e}")
            return False

    def update_keybindings(self):
        """Compare managed Helix bindings and prompt separately for each difference."""
        if not self.keybinding_src.exists():
            print_error(f"keybinding_config.txt not found at {self.keybinding_src}")
            return False
        
        if not self.helix_config.exists():
            print_error(f"Helix config not found at {self.helix_config}")
            return False
        
        try:
            keybinding_content = self.keybinding_src.read_text()
            helix_content = self.helix_config.read_text()

            section_match = re.search(r"(?m)^\s*\[([^\]]+)\]\s*(?:#.*)?$", keybinding_content)
            if not section_match:
                print_error("No keybinding table found in keybinding_config.txt")
                return False
            table_name = section_match.group(1)
            source_lines, source_start, _, _ = self._table_contents(keybinding_content, table_name)
            if source_start is None:
                print_error(f"Keybinding table [{table_name}] not found in keybinding_config.txt")
                return False
            source_end = len(source_lines)
            for index in range(source_start + 1, len(source_lines)):
                if re.match(r"^\s*\[", source_lines[index]):
                    source_end = index
                    break

            source_bindings = {}
            for line in source_lines[source_start + 1:source_end]:
                assignment = self._assignment(line)
                if assignment:
                    source_bindings[assignment[0]] = (assignment[1], line)
            if not source_bindings:
                print_error(f"No keybindings found in [{table_name}]")
                return False

            helix_lines, table_start, table_end, current_bindings = self._table_contents(
                helix_content, table_name
            )
            accepted = []
            for key, (source_value, source_line) in source_bindings.items():
                current = current_bindings.get(key)
                if current and current[0] == source_value:
                    verbose(f"Helix binding {key} is up to date", self.verbose)
                    continue

                if current:
                    print_warning(f"Helix binding {key} differs from keybinding_config.txt")
                    print(f"  Current: {current[0]}")
                else:
                    print_warning(f"Helix binding {key} is missing from Helix config")
                    print("  Current: <missing>")
                print(f"  Desired: {source_value}")

                if self.dry_run:
                    print(f"  Would ask whether to update Helix binding {key}")
                    continue

                update = self.confirm(f"Update Helix binding {key}?")
                if update is None:
                    return False
                if update:
                    accepted.append((key, source_line, current[1] if current else None))

            if self.dry_run or not accepted:
                if not self.dry_run:
                    print_success("Helix keybindings are up to date or unchanged")
                return True

            replacements = {}
            additions = []
            for key, source_line, line_index in accepted:
                if line_index is None:
                    additions.append(source_line)
                else:
                    replacements[line_index] = source_line

            for index, line in replacements.items():
                helix_lines[index] = line

            if additions:
                if table_start is None:
                    new_content = helix_content
                    if new_content and not new_content.endswith("\n"):
                        new_content += "\n"
                    if new_content and not new_content.endswith("\n\n"):
                        new_content += "\n"
                    new_content += f"[{table_name}]\n" + "".join(
                        line if line.endswith("\n") else line + "\n" for line in additions
                    )
                else:
                    if table_end > 0 and not helix_lines[table_end - 1].endswith(("\n", "\r")):
                        helix_lines[table_end - 1] += "\n"
                    helix_lines[table_end:table_end] = [
                        line if line.endswith(("\n", "\r")) else line + "\n"
                        for line in additions
                    ]
                    new_content = "".join(helix_lines)
            else:
                new_content = "".join(helix_lines)

            self.helix_config.write_text(new_content)
            print_success(f"Updated Helix keybindings in {self.helix_config}")
            return True
        except OSError as e:
            print_error(f"Failed to update Helix keybindings: {e}")
            return False

    def run(self):
        """Execute the installation"""
        print(f"\n{Colors.BLUE}╔════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BLUE}║  HXYZ Installation Script              ║{Colors.RESET}")
        print(f"{Colors.BLUE}╚════════════════════════════════════════╝{Colors.RESET}\n")
        
        if self.dry_run:
            print_info("DRY RUN mode - no changes will be made\n")
        
        # Pre-installation checks
        print_info("Checking dependencies...")
        if not self.check_dependencies():
            return False
        print_success("Dependencies OK\n")
        
        print_info("Checking for conflicts...")
        if self.check_hz_symlink_exists():
            return False

        print_success("No conflicts detected\n")
        
        # Installation
        print_info("Installing components...")
        if not self.install_hxyz():
            return False
        
        if not self.create_hz_symlink():
            return False
        
        if not self.install_yazi_config():
            return False
        
        if not self.update_keybindings():
            return False
        
        # Success
        print(f"\n{Colors.GREEN}✓ Installation successful!{Colors.RESET}\n")
        self.show_post_install_info()
        return True

    def show_post_install_info(self):
        """Display post-installation information"""
        print(f"{Colors.BLUE}Quick Reference:{Colors.RESET}")
        print(f"  Keybinding:  {Colors.YELLOW}space + m + f{Colors.RESET}")
        print(f"  Action:      Toggle file picker pane in Helix\n")
        
        print(f"{Colors.BLUE}Setup Summary:{Colors.RESET}")
        print(f"  ✓ hxyz script → ~/.local/bin/hxyz")
        print(f"  ✓ hz symlink → ~/.local/bin/hz")
        print(f"  ✓ yazi config → ~/.config/hxyz/yazi.toml")
        print(f"  ✓ Helix keybinding injected\n")
        
        print(f"{Colors.BLUE}Next Steps:{Colors.RESET}")
        print(f"  1. Start with: {Colors.YELLOW}hxyz{Colors.RESET} or {Colors.YELLOW}hz{Colors.RESET}")
        print(f"  2. Or use keybinding: {Colors.YELLOW}space + m + f{Colors.RESET} in Helix\n")


def main():
    parser = argparse.ArgumentParser(
        description="Install HXYZ (Helix + Zellij + Yazi integration)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 install.py              # Standard installation
  python3 install.py --dry-run    # Preview what would be installed
  python3 install.py --verbose    # Show detailed progress
  python3 install.py --no-dep-check  # Skip dependency verification
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without making changes"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress"
    )
    parser.add_argument(
        "--no-dep-check",
        action="store_true",
        help="Skip dependency verification"
    )
    
    args = parser.parse_args()
    
    ctx = InstallContext(
        dry_run=args.dry_run,
        verbose_flag=args.verbose,
        no_dep_check=args.no_dep_check
    )
    
    success = ctx.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
