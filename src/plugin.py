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

from .moddatachecker import TheSims4ModDataChecker
from .moddatacontent import TheSims4ModDataContent


class TheSims4GamePlugin(IPluginGame, IPluginFileMapper):
    _gamePath: str = ""
    _organizer: IOrganizer
    _isRunning: bool = False

    def __init__(self):
        IPluginGame.__init__(self)
        IPluginFileMapper.__init__(self)

    # IPlugin Implementation

    def name(self) -> str:
        return "The Sims 4 Support"

    def localizedName(self) -> str:
        return self.name()

    def author(self) -> str:
        return "Cram42"

    def version(self) -> VersionInfo:
        return VersionInfo("0.3.0")

    def description(self) -> str:
        return "Game support for The Sims 4."

    def settings(self) -> list[PluginSetting]:
        return [
            PluginSetting(
                "per_profile_data",
                "Store run data per profile, rather than per instance",
                True,
            )
        ]

    def init(self, organizer: IOrganizer) -> bool:
        self._organizer = organizer
        self._organizer.gameFeatures().registerFeature(
            self,
            TheSims4ModDataChecker(),
            0,
            True,
        )
        self._organizer.gameFeatures().registerFeature(
            self,
            TheSims4ModDataContent(),
            0,
            True,
        )
        self._organizer.onAboutToRun(self._onAboutToRun)
        self._organizer.onFinishedRun(self._onFinishedRun)
        return True

    # IPluginGame Implementation

    def binaryName(self) -> str:
        return "Game/Bin/TS4_x64.exe"

    def dataDirectory(self) -> QDir:
        userDocumentsDir = QDir(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
        )
        return QDir(userDocumentsDir.absoluteFilePath("Electronic Arts/The Sims 4"))

    def detectGame(self) -> None:
        pass

    def documentsDirectory(self) -> QDir:
        return QDir()

    def executableForcedLoads(self) -> list[ExecutableForcedLoadSetting]:
        return []

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

    def gameDirectory(self) -> QDir:
        return QDir(self._gamePath)

    def gameIcon(self) -> QIcon:
        return getIconForExecutable(self.binaryAbsPath())

    def gameName(self) -> str:
        return "The Sims 4"

    def gameNexusName(self) -> str:
        return self.gameShortName()

    def gameShortName(self) -> str:
        return "thesims4"

    def gameVersion(self) -> str:
        return getFileVersion(self.binaryAbsPath())

    def getLauncherName(self) -> str:
        return ""

    def getSupportURL(self) -> str:
        return ""

    def initializeProfile(self, directory: QDir, settings: ProfileSetting) -> None:
        pass

    def isInstalled(self) -> bool:
        return bool(self._gamePath)

    def listSaves(self, folder: QDir) -> list[ISaveGame]:
        return []

    def looksValid(self, directory: QDir) -> bool:
        return directory.exists(self.binaryName())

    def nexusGameID(self) -> int:
        return 641

    def savesDirectory(self) -> QDir:
        return QDir()

    def secondaryDataDirectories(self) -> dict[str, QDir]:
        # Allow runData to appear in file list, but not create loops when mapping
        return {} if self._isRunning else {"runData": self.runDataDirectory()}

    def setGamePath(self, path: str) -> None:
        self._gamePath = path

    def setGameVariant(self, variant: str) -> None:
        pass

    def validShortNames(self) -> list[str]:
        return []

    # IPluginFileMapper Implementation

    def mappings(self) -> list[Mapping]:
        return [
            Mapping(
                self.runDataDirectory().absoluteFilePath(None),
                self.dataDirectory().absoluteFilePath(None),
                True,
                True,
            )
        ]

    # Extra

    def binaryAbsPath(self) -> str:
        return self.gameDirectory().absoluteFilePath(self.binaryName())

    def modsDirectory(self) -> QDir:
        return QDir(self.dataDirectory().absoluteFilePath("Mods"))

    def trayDirectory(self) -> QDir:
        return QDir(self.dataDirectory().absoluteFilePath("Tray"))

    def runDataDirectory(self) -> QDir:
        perProfile = self._organizer.pluginSetting(self.name(), "per_profile_data")
        parentDir = QDir(
            self._organizer.profilePath() if perProfile else self._organizer.basePath()
        )
        return QDir(parentDir.absoluteFilePath("runData"))

    def _onAboutToRun(self, exePath: str, workingDir: QDir, args: str) -> bool:
        self._isRunning = True
        return True

    def _onFinishedRun(self, exePath: str, returnCode: int) -> None:
        self._isRunning = False
