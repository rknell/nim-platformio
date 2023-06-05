from os import system, path
from shutil import copyfile
from pathlib import Path

Import("env")

src = Path(env.subst("$PROJECT_SRC_DIR"))

if not path.exists(src/'panicoverride.nim'):
  copyfile(Path().parent/'panicoverride.nim', src/'panicoverride.nim')

if not path.exists('nim.cfg'):
  copyfile(Path().parent/'nim.cfg', 'nim.cfg')

libdeps = env.subst("$PROJECT_LIBDEPS_DIR/$PIOENV")

cpu = "avr"
if "espressif" in env.subst("$PIOPLATFORM"):
  cpu = "esp"
elif "ststm32" in env.subst("$PIOPLATFORM"):
  cpu = "arm"

flags = (
  f"--path:{libdeps} "
  f"--cpu:{cpu} "
)

result = system(f"nim cpp {flags} {src/'main'}")
if result != 0:
  exit(result)
