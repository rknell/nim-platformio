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
    Generates nim compiler arguments dynamically
    based on PlatformIO settings and compiles main.nim
    """
    libdeps = env.subst("$PROJECT_LIBDEPS_DIR/$PIOENV")
    cpu = _get_cpu()
    nim_args = f"--path:{libdeps} --cpu:{cpu} "
    prj_src_dir = Path(env.subst("$PROJECT_SRC_DIR"))
    system(f"nim cpp {nim_args} {prj_src_dir/'main'}")


def _get_cpu() -> str:
    """
    Returns the CPU type to give to the Nim compiler
    based on the PlatformIO platform setting.
    Reference:
    https://docs.platformio.org/en/latest/platforms/index.html
    """
    DEFAULT_CPU = "arm"
    platform_cpu = {
        "atmelavr": "avr",
        "atmelmegaavr": "avr",
        "espressif32": "esp",
        "espressif8266": "esp",
        "riscv_gap": "riscv32",
        "sifive": "riscv32",
        "timsp430": "msp430",
    }
    pio_plat = env.subst("$PIOPLATFORM")
    return platform_cpu.get(pio_plat, DEFAULT_CPU)


# try:4
copy_files()
compile()
