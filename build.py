#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cross-platform PyInstaller build helper for RedBookCards."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"
APP_NAME = "RedBookCards"


def clean() -> None:
    for path in (DIST, BUILD):
        if path.exists():
            shutil.rmtree(path)


def icon_path() -> Path | None:
    icons = ROOT / "resources" / "icons"
    if sys.platform == "win32":
        candidate = icons / "app.ico"
    elif sys.platform == "darwin":
        # PyInstaller can convert PNG to icns when Pillow is installed.
        candidate = icons / "icon_512x512.png"
    else:
        candidate = icons / "icon_512x512.png"
    return candidate if candidate.exists() else None


def build(mode: str | None = None) -> Path:
    if mode is None:
        # A Windows one-file exe is convenient. On macOS, onedir is the
        # recommended layout for a normal .app bundle.
        mode = "onedir" if sys.platform == "darwin" else "onefile"

    separator = ";" if sys.platform == "win32" else ":"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--windowed",
        f"--{mode}",
        "--name",
        APP_NAME,
        "--add-data",
        f"{ROOT / 'resources'}{separator}resources",
        "--hidden-import",
        "PySide6.QtWebEngineCore",
        "--hidden-import",
        "PySide6.QtWebEngineWidgets",
        "--hidden-import",
        "pymdownx.superfences",
        "--hidden-import",
        "pymdownx.highlight",
        "--hidden-import",
        "pymdownx.arithmatex",
        "--hidden-import",
        "latex2mathml",
    ]

    icon = icon_path()
    if icon:
        cmd += ["--icon", str(icon)]

    if sys.platform == "win32":
        version_file = ROOT / "version_info.txt"
        if version_file.exists():
            cmd += ["--version-file", str(version_file)]

    cmd.append(str(ROOT / "main.py"))

    print(f"Building RedBookCards on {platform.platform()} ({platform.machine()})")
    print(" ".join(str(part) for part in cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)

    if sys.platform == "win32":
        output = DIST / (f"{APP_NAME}.exe" if mode == "onefile" else APP_NAME / f"{APP_NAME}.exe")
    elif sys.platform == "darwin":
        output = DIST / f"{APP_NAME}.app"
    else:
        output = DIST / (APP_NAME if mode == "onefile" else APP_NAME / APP_NAME)

    if not output.exists():
        raise FileNotFoundError(f"PyInstaller completed but output was not found: {output}")

    print(f"Build complete: {output}")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RedBookCards with PyInstaller")
    parser.add_argument("--mode", choices=("onefile", "onedir"), default=None)
    parser.add_argument("--no-clean", action="store_true", help="Keep the previous build/dist directories")
    args = parser.parse_args()

    if not args.no_clean:
        clean()

    try:
        build(args.mode)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
