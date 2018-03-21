from cx_Freeze import setup, Executable

base = None
executables = [Executable( "honey-finder.py",base = base)]

packages = ["idna"]
options = {
    'HoneyFinder.exe':{
        'packages':packages,
    },
}

setup(
    name = "HoneyFinder.exe",
    options = options,
    version = "Early Access Edition",
    description = "Find Error logs faster than Pooh can eat all his honey.",
    executables = executables
)