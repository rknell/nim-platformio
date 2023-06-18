from os import path, system
from pathlib import Path
from shutil import copyfile


Import("env")


def copy_files():
    """Copies a minimum set of files needed to compile
    if they do not already exist in the project.
    """
    prj_src_dir = Path(env.subst("$PROJECT_SRC_DIR"))

    # Default files and their destination
    default_file_info = (
        ("panicoverride.nim", prj_src_dir),
        ("main.nim", prj_src_dir),
        ("nim.cfg", prj_src_dir.parent),
        )

    # Copy a default file if a file is missing
    for fn, dest in default_file_info:
        if not path.exists(dest/fn):
            copyfile(Path().parent/fn, dest/fn)


def compile():
    """
    To be responsive to changes to PlatformIO project
    config files, some arguments are generated dynamically
    and passed to the nim compiler on the command line.
    """
    # A table to convert PlatformIO 'platform' setting
    # to the CPU type to give to the Nim compiler.
    default_cpu_family = "avr"
    cpu_info = (
        ("espressif", "esp"),
        ("ststm32", "arm"),
        )

    prj_src_dir = Path(env.subst("$PROJECT_SRC_DIR"))

    # Build project-specific args to the nim compiler
    libdeps = env.subst("$PROJECT_LIBDEPS_DIR/$PIOENV")
    for plat, cpu_family in cpu_info:
        if plat in env.subst("$PIOPLATFORM"):
            cpu = cpu_family
            break
    else:
        cpu = default_cpu_family
    nim_args = f"--path:{libdeps} --cpu:{cpu} "

    # Compile main.nim
    system(f"nim cpp {nim_args} {prj_src_dir/'main'}")


# try:4
copy_files()
compile()
