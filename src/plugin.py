from PyQt6.QtCore import QDir, QStandardPaths
from PyQt6.QtGui import QIcon

from mobase import (
    ExecutableForcedLoadSetting,
    ExecutableInfo,
    IOrganizer,
    IPluginFileMapper,
    IPluginGame,
    ISaveGame,
    Mapping,
    PluginSetting,
    ProfileSetting,
    VersionInfo,
    getFileVersion,
    getIconForExecutable,
)


class TheSims4GamePlugin(IPluginGame, IPluginFileMapper):
    _gamePath: str = ""
    _organizer: IOrganizer

    def __init__(self):
        IPluginFileMapper.__init__(self)
        IPluginGame.__init__(self)

    # IPlugin Implementation

    def name(self) -> str:
        return "The Sims 4 Support"

    def localizedName(self) -> str:
        # TODO: Translation stuff
        return self.name()

    def author(self) -> str:
        return "Cram42"

    def version(self) -> VersionInfo:
        return VersionInfo("0.1.0")

    def description(self) -> str:
        return "Game support for The Sims 4."

    def settings(self) -> list[PluginSetting]:
        return []

    def init(self, organizer: IOrganizer) -> bool:
        self._organizer = organizer
        self._organizer.onAboutToRun(self._onAboutToRun)
        return True

    # IPluginFileMapper Implementation

    def mappings(self) -> list[Mapping]:
        return [
            Mapping(
                QDir(self._organizer.basePath()).absoluteFilePath("runData"),
                self.dataRootDirectory().absoluteFilePath(None),
                True,
                True,
            )
        ]

    # IPluginGame Implementation

    def gameName(self) -> str:
        return "The Sims 4"

    def gameShortName(self) -> str:
        return "thesims4"

    def validShortNames(self) -> list[str]:
        return ["TS4"]

    def nexusGameID(self) -> int:
        return -1

    def gameDirectory(self) -> QDir:
        return QDir(self._gamePath)

    def setGamePath(self, path: str) -> None:
        self._gamePath = path

    def dataDirectory(self) -> QDir:
        return self.modDirectory()

    def documentsDirectory(self) -> QDir:
        return QDir()

    def savesDirectory(self) -> QDir:
        return QDir()

    def binaryName(self) -> str:
        return "TS4_x64.exe"

    def gameIcon(self) -> QIcon:
        return getIconForExecutable(self.binaryAbsPath())

    def gameVersion(self) -> str:
        return getFileVersion(self.binaryAbsPath())

    def steamAPPId(self) -> str:
        return ""

    def isInstalled(self) -> bool:
        return bool(self._gamePath)

    def getLauncherName(self) -> str:
        return ""

    def executables(self) -> list[ExecutableInfo]:
        return [
            ExecutableInfo(self.gameName(), self.binaryAbsPath()),
            ExecutableInfo(
                "{0} (Offline, Skip Intro)".format(self.gameName()),
                self.binaryAbsPath(),
            )
            .withArgument("-alwaysoffline")
            .withArgument("-nointro"),
        ]

    def executableForcedLoads(self) -> list[ExecutableForcedLoadSetting]:
        return []

    def getSupportURL(self) -> str:
        return ""

    def detectGame(self) -> None:
        pass

    def looksValid(self, directory: QDir) -> bool:
        return directory.exists(self.binaryRelPath())

    def initializeProfile(self, directory: QDir, settings: ProfileSetting) -> None:
        pass

    def listSaves(self, folder: QDir) -> list[ISaveGame]:
        return []

    def setGameVariant(self, variant: str) -> None:
        pass

    # Extra

    def binaryRelPath(self) -> str:
        return "Game/Bin/{0}".format(self.binaryName())

    def binaryAbsPath(self) -> str:
        return self.gameDirectory().absoluteFilePath(self.binaryRelPath())

    def dataRootDirectory(self) -> QDir:
        docsDir = QDir(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
        )
        return QDir(docsDir.absoluteFilePath("Electronic Arts/The Sims 4"))

    def modDirectory(self) -> QDir:
        return QDir(self.dataRootDirectory().absoluteFilePath("Mods"))

    def _onAboutToRun(self, exePath: str, workingDir: QDir, args: str) -> bool:
        return True
