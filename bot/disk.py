from pathlib import Path

class File():

    def __init__(self, path: Path, *, exist_ok: bool = True) -> None:
        """
        Initializes a representation of a file on disk.

        Args:
            path: A reference to a file on disk.
            exist_ok: Whether the provided file should be created on disk if it does not exist.
        """

        # create an absolute reference to the file
        self._path: Path = path.absolute().resolve()
        """A path referencing the file on disk."""
        
        # create the parent directory on disk (if it doesn't already exist)
        self._path.parent.mkdir(parents=True, exist_ok=exist_ok)
        # create the file on disk (if it doesn't already exist)
        self._path.touch(exist_ok=exist_ok)

    @property
    def name(self) -> str:
        """The name of the file."""
        return self._path.name
    
    @property
    def path(self) -> Path:
        """The absolute path of the file."""
        return self._path
    
    
class Folder():

    def __init__(self, path: Path, *, exist_ok: bool = True) -> None:
        """
        Initializes a representation of a folder on disk.

        Args:
            path: A reference to a folder on disk.
            exist_ok: Whether the provided folder should be created on disk if it does not exist.
        """

        # create an absolute reference to the folder
        self._path: Path = path.absolute().resolve()
        """A path referencing the folder on disk."""

        # create the directory on disk (if it doesn't already exist)
        self._path.mkdir(parents=True, exist_ok=exist_ok)

    @property
    def name(self) -> str:
        """The name of the folder."""
        return self._path.name
    
    @property
    def path(self) -> Path:
        """The absolute path of the folder."""
        return self._path