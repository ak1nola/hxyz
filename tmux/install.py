#!/usr/bin/env python3
"""
THXY Install Script
Manages installation and uninstallation of thxy
(tmux + Helix + yazi integration) with dependency checking
and safe configuration updates.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes"""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    DIM = "\033[2m"


def print_blah():
    return "your parents seem pretty cool"

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
        self.thxy_src = self.script_dir / "bin" / "thxy"
        self.thxy_dst = self.home / ".local" / "bin" / "thxy"
        self.th_symlink = self.home / ".local" / "bin" / "th"

        self.zwt_src = self.script_dir.parent / "common" / "bin" / "zwt"
        self.zwt_dst = self.home / ".local" / "bin" / "zwt"

        self.yazi_src = self.script_dir / "config" / "yazi.toml"
        self.yazi_dst_dir = self.home / ".config" / "thxy"
        self.yazi_dst = self.yazi_dst_dir / "yazi.toml"

        self.helix_config = self.home / ".config" / "helix" / "config.toml"
        self.keybinding_src = self.script_dir.parent / "common" / "config" / "keybinding_config.txt"

    def get_keybinding_spec(self):
        """Read keybinding sections and their key names from keybinding source file.

        Returns a list of (section_name, key_names) tuples.
        """
        if not self.keybinding_src.exists():
            return [("[keys.normal.space.m]", ["f", "g"])]

        sections = []
        current_section = None
        current_keys = []

        for line in self.keybinding_src.read_text().splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if stripped.startswith("[") and stripped.endswith("]"):
                if current_section is not None:
                    sections.append((current_section, current_keys))
                current_section = stripped
                current_keys = []
                continue

            if "=" in stripped:
                current_keys.append(stripped.split("=", 1)[0].strip())

        if current_section is not None:
            sections.append((current_section, current_keys))

        return sections or [("[keys.normal.space.m]", ["f", "g"])]

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
                    ["which", "hx"], capture_output=True, text=True
                )
                helix_check = subprocess.run(
                    ["which", "helix"], capture_output=True, text=True
                )
                if hx_check.returncode != 0 and helix_check.returncode != 0:
                    missing.append(dep)
            else:
                result = subprocess.run(["which", dep], capture_output=True, text=True)
                if result.returncode != 0:
                    missing.append(dep)

        if missing:
            print_error(f"Missing dependencies: {', '.join(missing)}")
            print_info(
                "Install them and try again. Use --no-dep-check to skip this check."
            )
            return False

        verbose("All dependencies found", self.verbose)
        return True

    def check_thxy_exists(self):
        """Check if thxy already exists in ~/.local/bin/"""
        if self.thxy_dst.exists():
            print_error(f"thxy already exists at {self.thxy_dst}")
            print_info("Remove it or use a different installation path")
            return True
        verbose(f"thxy not found at {self.thxy_dst} (good)", self.verbose)
        return False

    def check_th_symlink_exists(self):
        """Check if th symlink already exists in ~/.local/bin/"""
        if self.th_symlink.exists() or self.th_symlink.is_symlink():
            print_error(f"th already exists at {self.th_symlink}")
            print_info("Remove it or use a different installation path")
            return True
        verbose(f"th not found at {self.th_symlink} (good)", self.verbose)
        return False

    def check_keybinding_exists(self):
        """Check if all thxy keybindings already exist in helix config."""
        if not self.helix_config.exists():
            verbose(f"Helix config not found at {self.helix_config}", self.verbose)
            return False

        try:
            sections = self.get_keybinding_spec()
            lines = self.helix_config.read_text().splitlines()

            for section_name, key_names in sections:
                section_start = None
                section_end = len(lines)

                for i, line in enumerate(lines):
                    if line.strip() == section_name:
                        section_start = i
                        break

                if section_start is None:
                    return False

                for i in range(section_start + 1, len(lines)):
                    stripped = lines[i].strip()
                    if stripped.startswith("[") and stripped.endswith("]"):
                        section_end = i
                        break

                section_lines = lines[section_start + 1 : section_end]
                present_keys = set()

                for line in section_lines:
                    stripped = line.strip()
                    if "=" not in stripped:
                        continue
                    present_keys.add(stripped.split("=", 1)[0].strip())

                if not all(key in present_keys for key in key_names):
                    return False

            return True
        except Exception as e:
            verbose(f"Error reading helix config: {e}", self.verbose)

        return False

    def remove_file_or_symlink(self, path, label):
        """Remove a file or symlink if it exists."""
        if not path.exists() and not path.is_symlink():
            print_warning(f"{label} not found at {path} (skipping)")
            return True

        if self.dry_run:
            print(f"  Would remove {path}")
            return True

        try:
            path.unlink()
            print_success(f"Removed {label}: {path}")
            return True
        except Exception as e:
            print_error(f"Failed to remove {label} at {path}: {e}")
            return False

    def remove_directory(self, path, label):
        """Remove a directory recursively if it exists."""
        if not path.exists():
            print_warning(f"{label} not found at {path} (skipping)")
            return True

        if self.dry_run:
            print(f"  Would remove directory {path}")
            return True

        try:
            shutil.rmtree(path)
            print_success(f"Removed {label}: {path}")
            return True
        except Exception as e:
            print_error(f"Failed to remove {label} at {path}: {e}")
            return False

    def remove_keybinding(self):
        """Remove THXY keybindings from helix config."""
        if not self.helix_config.exists():
            print_warning(f"Helix config not found at {self.helix_config} (skipping)")
            return True

        try:
            sections = self.get_keybinding_spec()
            lines = self.helix_config.read_text().splitlines()
            total_removed = 0

            for section_name, key_names in sections:
                section_start = None
                section_end = len(lines)
                for i, line in enumerate(lines):
                    if line.strip() == section_name:
                        section_start = i
                        break

                if section_start is None:
                    continue

                for i in range(section_start + 1, len(lines)):
                    stripped = lines[i].strip()
                    if stripped.startswith("[") and stripped.endswith("]"):
                        section_end = i
                        break

                body = lines[section_start + 1 : section_end]
                new_body = []
                removed_count = 0

                for line in body:
                    stripped = line.strip()
                    if "=" in stripped:
                        key_name = stripped.split("=", 1)[0].strip()
                        if key_name in key_names:
                            removed_count += 1
                            continue
                    new_body.append(line)

                total_removed += removed_count

                section_empty = all(not line.strip() for line in new_body)
                if section_empty:
                    lines = lines[:section_start] + lines[section_end:]
                else:
                    lines = lines[: section_start + 1] + new_body + lines[section_end:]

            if total_removed == 0:
                print_warning("No thxy keybindings found in helix config (skipping)")
                return True

            while True:
                collapsed = "\n".join(lines).replace("\n\n\n", "\n\n")
                if collapsed == "\n".join(lines):
                    break
                lines = collapsed.split("\n")

            if self.dry_run:
                print(f"  Would remove thxy keybindings from {self.helix_config}")
                return True

            self.helix_config.write_text("\n".join(lines).rstrip() + "\n")
            print_success("Removed thxy keybindings from helix config")
            return True
        except Exception as e:
            print_error(f"Failed to remove thxy keybindings: {e}")
            return False

    def install_thxy(self):
        """Copy thxy script to ~/.local/bin/"""
        if not self.thxy_src.exists():
            print_error(f"thxy script not found at {self.thxy_src}")
            return False

        self.thxy_dst.parent.mkdir(parents=True, exist_ok=True)

        if self.dry_run:
            print(f"  Would copy {self.thxy_src} → {self.thxy_dst}")
            return True

        try:
            shutil.copy2(self.thxy_src, self.thxy_dst)
            self.thxy_dst.chmod(0o755)
            verbose(f"Copied thxy to {self.thxy_dst}", self.verbose)
            print_success("Installed thxy to ~/.local/bin/thxy")
            return True
        except Exception as e:
            print_error(f"Failed to install thxy: {e}")
            return False

    def install_zwt(self):
        """Copy zwt script to ~/.local/bin/"""
        if not self.zwt_src.exists():
            print_error(f"zwt script not found at {self.zwt_src}")
            return False

        self.zwt_dst.parent.mkdir(parents=True, exist_ok=True)

        if self.dry_run:
            print(f"  Would copy {self.zwt_src} → {self.zwt_dst}")
            return True

        try:
            shutil.copy2(self.zwt_src, self.zwt_dst)
            self.zwt_dst.chmod(0o755)
            verbose(f"Copied zwt to {self.zwt_dst}", self.verbose)
            print_success("Installed zwt to ~/.local/bin/zwt")
            return True
        except Exception as e:
            print_error(f"Failed to install zwt: {e}")
            return False

    def install_yazi_config(self):
        """Copy yazi.toml to ~/.config/thxy/"""
        if not self.yazi_src.exists():
            print_error(f"yazi.toml not found at {self.yazi_src}")
            return False

        self.yazi_dst_dir.mkdir(parents=True, exist_ok=True)

        if self.dry_run:
            print(f"  Would copy {self.yazi_src} → {self.yazi_dst}")
            return True

        try:
            shutil.copy2(self.yazi_src, self.yazi_dst)
            verbose(f"Copied yazi.toml to {self.yazi_dst}", self.verbose)
            print_success(f"Installed yazi config to ~/.config/thxy/yazi.toml")
            return True
        except Exception as e:
            print_error(f"Failed to install yazi config: {e}")
            return False

    def create_th_symlink(self):
        """Create th symlink to thxy executable"""
        self.th_symlink.parent.mkdir(parents=True, exist_ok=True)

        if self.dry_run:
            print(f"  Would create symlink {self.th_symlink} → {self.thxy_dst}")
            return True

        try:
            # Create symlink using thxy_dst as absolute path
            self.th_symlink.symlink_to(self.thxy_dst)
            verbose(f"Created symlink th -> thxy at {self.th_symlink}", self.verbose)
            print_success("Created 'th' symlink to 'thxy'")
            return True
        except Exception as e:
            print_error(f"Failed to create th symlink: {e}")
            return False

    def inject_keybinding(self):
        """Inject thxy keybindings into helix config."""
        if not self.keybinding_src.exists():
            print_error(f"keybinding_config.txt not found at {self.keybinding_src}")
            return False

        if not self.helix_config.exists():
            print_error(f"Helix config not found at {self.helix_config}")
            return False

        try:
            sections = self.get_keybinding_spec()
            keybinding_lines = self.keybinding_src.read_text().splitlines()
            helix_content = self.helix_config.read_text()

            # Parse keybinding_config.txt into section -> lines mapping
            src_sections = {}  # section_name -> [line, ...]
            current_section = None
            for line in keybinding_lines:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped
                    src_sections.setdefault(current_section, [])
                    continue
                if current_section and "=" in stripped:
                    src_sections[current_section].append(line)

            all_missing = {}  # section_name -> [missing_lines]

            for section_name, key_names in sections:
                keys_for_section = src_sections.get(section_name, [])
                if not keys_for_section:
                    continue

                if section_name in helix_content:
                    # Section exists, find its bounds
                    section_start = helix_content.find(section_name)
                    next_section_start = helix_content.find("\n[", section_start + 1)
                    if next_section_start == -1:
                        section_text = helix_content[section_start:]
                    else:
                        section_text = helix_content[section_start:next_section_start]

                    missing = []
                    for key_line in keys_for_section:
                        key_name = key_line.strip().split("=", 1)[0].strip()
                        if (
                            f"{key_name} =" not in section_text
                            and f"{key_name}=" not in section_text
                        ):
                            missing.append(key_line)

                    if missing:
                        all_missing[section_name] = missing
                else:
                    # Section doesn't exist at all
                    all_missing[section_name] = keys_for_section

            if not all_missing:
                print_warning("thxy keybindings already exist in helix config")
                return True

            if self.dry_run:
                for section_name, lines in all_missing.items():
                    print(
                        f"  Would add to {section_name}: {', '.join(l.strip().split('=')[0].strip() for l in lines)}"
                    )
                return True

            # Apply changes
            for section_name, missing_lines in all_missing.items():
                if section_name in helix_content:
                    section_start = helix_content.find(section_name)
                    next_section_start = helix_content.find("\n[", section_start + 1)
                    if next_section_start == -1:
                        helix_content = (
                            helix_content.rstrip()
                            + "\n"
                            + "\n".join(missing_lines)
                            + "\n"
                        )
                    else:
                        helix_content = (
                            helix_content[:next_section_start].rstrip()
                            + "\n"
                            + "\n".join(missing_lines)
                            + "\n"
                            + helix_content[next_section_start:]
                        )
                else:
                    helix_content = (
                        helix_content.rstrip()
                        + "\n\n"
                        + section_name
                        + "\n"
                        + "\n".join(missing_lines)
                        + "\n"
                    )

            self.helix_config.write_text(helix_content)
            verbose(f"Injected keybindings into {self.helix_config}", self.verbose)
            print_success("Injected thxy keybindings into helix config")
            return True
        except Exception as e:
            print_error(f"Failed to inject keybinding: {e}")
            return False

    def run(self):
        """Execute the installation"""
        print(
            f"\n{Colors.BLUE}╔════════════════════════════════════════╗{Colors.RESET}"
        )
        print(f"{Colors.BLUE}║  THXY Installation Script              ║{Colors.RESET}")
        print(
            f"{Colors.BLUE}╚════════════════════════════════════════╝{Colors.RESET}\n"
        )

        if self.dry_run:
            print_info("DRY RUN mode - no changes will be made\n")

        # Pre-installation checks
        print_info("Checking dependencies...")
        if not self.check_dependencies():
            return False
        print_success("Dependencies OK\n")

        print_info("Checking for conflicts...")
        # We don't block on existing thxy if it's already installed, but let's keep the existing logic
        # unless it's problematic. The check_thxy_exists currently prints error and returns True.

        # If both keybindings exist, we can warn but we should skip injection
        keybindings_exist = self.check_keybinding_exists()
        if keybindings_exist:
            print_warning("'space m' keybindings already configured in helix")

        print_success("No conflicts detected\n")

        # Installation
        print_info("Installing components...")
        # These will overwrite if already exists or handle accordingly
        if not self.install_thxy():
            return False

        if not self.install_zwt():
            return False

        if not self.create_th_symlink():
            # This might fail if it already exists, let's see create_th_symlink
            pass  # ignore failure for symlink if it exists?

        if not self.install_yazi_config():
            return False

        if not keybindings_exist:
            if not self.inject_keybinding():
                return False
        else:
            verbose("Skipping keybinding injection (already exists)", self.verbose)

        # Success
        print(f"\n{Colors.GREEN}✓ Installation successful!{Colors.RESET}\n")
        self.show_post_install_info()
        return True

    def run_uninstall(self):
        """Execute uninstallation."""
        print(
            f"\n{Colors.BLUE}╔════════════════════════════════════════╗{Colors.RESET}"
        )
        print(f"{Colors.BLUE}║  THXY Uninstall Script                 ║{Colors.RESET}")
        print(
            f"{Colors.BLUE}╚════════════════════════════════════════╝{Colors.RESET}\n"
        )

        if self.dry_run:
            print_info("DRY RUN mode - no changes will be made\n")

        print_info("Removing installed components...")
        success = True

        if not self.remove_file_or_symlink(self.thxy_dst, "thxy executable"):
            success = False

        if not self.remove_file_or_symlink(self.th_symlink, "th symlink"):
            success = False

        if not self.remove_directory(self.yazi_dst_dir, "thxy config directory"):
            success = False

        if not self.remove_keybinding():
            success = False

        if success:
            print(f"\n{Colors.GREEN}✓ Uninstall successful!{Colors.RESET}\n")
            self.show_post_uninstall_info()
        else:
            print_error("Uninstall completed with errors")

        return success

    def show_post_install_info(self):
        """Display post-installation information"""
        print(f"{Colors.BLUE}Quick Reference:{Colors.RESET}")
        print(f"  Keybinding:  {Colors.YELLOW}space + m + f{Colors.RESET}")
        print(f"  Action:      Toggle file picker pane in Helix")
        print(f"  Keybinding:  {Colors.YELLOW}space + m + g{Colors.RESET}")
        print(f"  Action:      Open Lazygit in floating pane\n")

        print(f"{Colors.BLUE}Setup Summary:{Colors.RESET}")
        print(f"  ✓ thxy script → ~/.local/bin/thxy")
        print(f"  ✓ th symlink → ~/.local/bin/th")
        print(f"  ✓ yazi config → ~/.config/thxy/yazi.toml")
        print(f"  ✓ Helix keybindings injected\n")

        print(f"{Colors.BLUE}Next Steps:{Colors.RESET}")
        print(
            f"  1. Start with: {Colors.YELLOW}thxy{Colors.RESET} or {Colors.YELLOW}th{Colors.RESET}"
        )
        print(
            f"  2. Or use keybinding: {Colors.YELLOW}space + m + f/g{Colors.RESET} in Helix\n"
        )

    def show_post_uninstall_info(self):
        """Display post-uninstall information"""
        print(f"{Colors.BLUE}Removed:{Colors.RESET}")
        print(f"  ✓ ~/.local/bin/thxy")
        print(f"  ✓ ~/.local/bin/th")
        print(f"  ✓ ~/.config/thxy")
        print(f"  ✓ thxy keybindings from ~/.config/helix/config.toml\n")


def main():
    parser = argparse.ArgumentParser(
        description="Install or uninstall THXY (tmux + Helix + yazi integration)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 install.py              # Standard installation
  python3 install.py uninstall    # Remove installed files and keybindings
  python3 install.py --dry-run    # Preview what would be installed
  python3 install.py --verbose    # Show detailed progress
  python3 install.py --no-dep-check  # Skip dependency verification
        """,
    )

    parser.add_argument(
        "action",
        nargs="?",
        choices=["install", "uninstall"],
        default="install",
        help="Choose whether to install or uninstall THXY",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without making changes",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed progress"
    )
    parser.add_argument(
        "--no-dep-check", action="store_true", help="Skip dependency verification"
    )

    args = parser.parse_args()

    ctx = InstallContext(
        dry_run=args.dry_run, verbose_flag=args.verbose, no_dep_check=args.no_dep_check
    )

    if args.action == "uninstall":
        success = ctx.run_uninstall()
    else:
        success = ctx.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
