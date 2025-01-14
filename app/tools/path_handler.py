import re
from pathlib import Path
from tinytag import TinyTag
from pydantic_settings import BaseSettings

ROOTDIR: Path = (Path.cwd().resolve()).parent

def get_path(*args: str | Path, rel: bool = False, create_dir: bool = False) -> Path:
    """
    Abstracts a path-like object or string path and returns it as a Path object.
    
    Optionally creates the directory if it doesn't exist.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Return relative path, defaults to False.
        create_dir (bool, optional): Create the directory if it doesn't exist, defaults to False.
    """
    
    home = ROOTDIR

    if create_dir:
        for arg in args: home = home / arg
        home.parent.mkdir(parents=True, exist_ok=True)
    else:
        for arg in args: home = home / arg
    
    return home.relative_to(ROOTDIR) if rel else home


def str_path(*args: str | Path, rel: bool = True) -> str:
    """
    Abstracts a path-like object or string path and returns it as a string.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Return relative path, defaults to True.
    """

    home = ROOTDIR

    for arg in args: home = home / arg
    if rel: home = home.relative_to(ROOTDIR)

    return home.as_posix()


def get_filename(*args: str | Path) -> tuple[str, str, str]:
    """
    Extract the filename, stem, and suffix from a given path or multiple Path objects.

    Args:
        *args (str | Path): One or more paths as strings or Path objects.

    Returns:
        tuple[str, str, str]:
            filename (str): The name of the file without directory.
            stem (str): The name of the file without its extension.
            suffix (str): The file extension (including the dot).
    """

    home = ROOTDIR

    for arg in args: home = home / arg
    name, stem, suffix = home.name, home.stem, home.suffix

    if not suffix.isascii():
        stem, suffix = stem + suffix, ''
    elif stem.startswith('.') and suffix == '':
        stem, suffix = '', stem

    return (name, stem, suffix.lower())


def is_supported_file(path: str) -> bool:
    """
    Check if a file supported by tinytag based on its suffix.
    """

    return get_path(path).suffix in TinyTag.SUPPORTED_FILE_EXTENSIONS


def is_excluded_file(name: str) -> bool:
    """
    Check if a file should be excluded based on its filename.
    """

    patterns = [
        r'.*Small.*',
        r'.*Cache.*',
        r'.*[{].*',
        r'.*cache.*',
        r'^\.',
        r'.*~$',
    ]

    for pattern in patterns:
        if re.search(pattern, name, re.IGNORECASE):
            return True
        
    return False


def create_dir(Config: BaseSettings) -> None:
    """
    Create directories based on paths defined in the Config.
    """

    required_dirs = ["DATADIR", "LIBRARYDIR", "ARTWORKDIR"]
    
    for attr in required_dirs:
        dir_path = getattr(Config, attr, None)
        if not isinstance(dir_path, Path): raise ValueError()
        dir_path.mkdir(parents=True, exist_ok=True)
