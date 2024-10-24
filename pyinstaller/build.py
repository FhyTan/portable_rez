import os
import subprocess
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import List


def create_spec_file(script_names: List[str] = None):
    """Create a PyInstaller spec file for all rez scripts."""

    spec_file = Path(__file__).parent / f"rez.spec"

    # Collect the rez scripts to build
    if script_names and "rez" in script_names:
        script_names.append("rez-rezolve")

    script_files = []
    for script_file in Path(__file__).parent.iterdir():
        if (
            script_file.is_file()
            and 'rez' in script_file.name
            and script_file.suffix == ".py"
            and (script_names is None or script_file.stem in script_names)
        ):
            script_files.append(script_file)

    print("Building script: {}".format(", ".join([s.stem for s in script_files])))

    # Write the spec file
    with spec_file.open("w") as f:
        # Write the header
        f.write(
            """# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('rez')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('rezplugins')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
            """
        )

        # Write the analysis, pyz, and exe for each script
        template_string = """
{name}_analysis = Analysis(
    ['{script_name}'],
    pathex=['{pathex}'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
{name}_pyz = PYZ({name}_analysis.pure)
{name}_exe = EXE(
    {name}_pyz,
    {name}_analysis.scripts,
    [],
    exclude_binaries=True,
    name='{exe_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
    """
        for script_file in script_files:
            script_name = script_file.name
            pathex = Path(__file__).parent.parent / "src"

            if script_file.stem == "rez-rezolve":
                # Special treat the rez-rezolve script use `rez` as the exe name
                f.write(
                    template_string.format(
                        name="rez",
                        exe_name="rez",
                        script_name=script_name,
                        pathex=pathex,
                    )
                )
                # Also compatible with osx
                f.write(
                    template_string.format(
                        name="rezolve",
                        exe_name="rezolve",
                        script_name=script_name,
                        pathex=pathex,
                    )
                )
            else:
                # Normally, just use the script stem as the exe name
                f.write(
                    template_string.format(
                        name=script_file.stem.replace("-", "_"),
                        exe_name=script_file.stem,
                        script_name=script_name,
                        pathex=pathex,
                    )
                )

        # Write the collect for each script
        f.write("\ncoll = COLLECT(\n")
        for script_file in script_files:
            if script_file.stem == "rez-rezolve":
                # Special treat the rez-rezolve script use `rez` as the exe name
                f.write(
                    "    rez_exe,\n"
                    "    rez_analysis.binaries,\n"
                    "    rez_analysis.datas,\n"
                )
                # Also compatible with osx
                f.write(
                    "    rezolve_exe,\n"
                    "    rezolve_analysis.binaries,\n"
                    "    rezolve_analysis.datas,\n"
                )
            else:
                name = script_file.stem.replace("-", "_")
                f.write(
                    f"    {name}_exe,\n"
                    f"    {name}_analysis.binaries,\n"
                    f"    {name}_analysis.datas,\n"
                )
        f.write(
            "    strip=False,\n"
            "    upx=True,\n"
            "    upx_exclude=[],\n"
            "    name='rez',\n"
            ")\n"
        )


def build_spec_file():
    """Build the spec file using PyInstaller."""

    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    spec_file = Path(__file__).parent / f"rez.spec"
    subprocess.run(
        f"pyinstaller -y --clean {spec_file}",
        shell=True,
        env={"PYTHONPATH": str(src_dir), **os.environ},
    )


def setup_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Build rez scripts using PyInstaller.",
        epilog=(
            "By default, all rez scripts in the pyinstaller directory will be built.\n"
            "You can specify the scripts to build using the --scripts argument.\n"
            "\n"
            "Example: python build.py --scripts rez rez-env\n"
        ),
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-s",
        "--script-names",
        nargs="+",
        help="The names of the scripts to build. If not specified, all scripts will be built.",
    )
    return parser


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    print(args)

    create_spec_file(args.script_names)
    build_spec_file()
