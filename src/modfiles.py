from enum import IntEnum
from pathlib import Path

from mobase import FileTreeEntry


class ModFiles:
    class FileTypes(IntEnum):
        UNIDENTIFIED = 0
        MOD_OTHER = 1
        MOD_PACKAGE = 2
        MOD_SCRIPT = 3
        TRAY_OTHER = 4
        TRAY_LOT = 5
        TRAY_ROOM = 6
        TRAY_SIM = 7

    Extensions: dict[FileTypes, list[str]] = {
        FileTypes.MOD_PACKAGE: ["package"],
        FileTypes.MOD_SCRIPT: ["ts4script"],
        FileTypes.TRAY_OTHER: ["trayitem"],
        FileTypes.TRAY_LOT: ["blueprint", "bpi"],
        FileTypes.TRAY_ROOM: ["rmi", "room"],
        FileTypes.TRAY_SIM: ["hhi", "householdbinary", "sgi"],
    }

    @classmethod
    def identify(cls, target: str | FileTreeEntry) -> FileTypes:
        if isinstance(target, FileTreeEntry):
            if target.fileType() != FileTreeEntry.FileTypes.FILE:
                return cls.FileTypes.UNIDENTIFIED
            else:
                return cls.identify(target.name())
        else:
            ext: str = Path(target).suffix.strip(".")
            for key, values in cls.Extensions.items():
                if ext in values:
                    return key
            return cls.FileTypes.UNIDENTIFIED
