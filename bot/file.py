from pathlib import Path

class File():

    def __init__(self, reference: Path, exist_ok: bool = True) -> None:
        # create an absolute reference to the file
        self._reference: Path = reference.absolute().resolve()
        # create the file's parent directory (if necessary)
        self._reference.parent.mkdir(parents=True, exist_ok=exist_ok)
        # create the file (if necessary)
        self._reference.touch(exist_ok=exist_ok)

    @property
    def name(self) -> str:
        """The name of the file."""
        return self._reference.name
    
    @property
    def path(self) -> Path:
        """The absolute path of the file."""
        return self._reference
    
    @property
    def parent(self) -> Path:
        """The parent directory of the file."""
        return self._reference.parent