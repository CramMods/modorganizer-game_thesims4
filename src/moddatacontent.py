from mobase import FileTreeEntry, IFileTree, ModDataContent

from .modfiles import ModFiles


class TheSims4ModDataContent(ModDataContent):
    def getAllContents(self) -> list[ModDataContent.Content]:
        return [
            ModDataContent.Content(
                ModFiles.FileTypes.MOD_PACKAGE, "Package", ":/MO/gui/content/bsa"
            ),
            ModDataContent.Content(
                ModFiles.FileTypes.MOD_SCRIPT, "Script", ":/MO/gui/content/script"
            ),
            ModDataContent.Content(
                ModFiles.FileTypes.TRAY_LOT, "Lot", ":/MO/gui/content/skyproc"
            ),
            ModDataContent.Content(
                ModFiles.FileTypes.TRAY_ROOM, "Room", ":/MO/gui/content/skyproc"
            ),
            ModDataContent.Content(
                ModFiles.FileTypes.TRAY_SIM, "Sim", ":/MO/gui/content/skyproc"
            ),
        ]

    def getContentsFor(self, filetree: IFileTree) -> list[int]:
        foundTypes: set[ModFiles.FileTypes] = set()

        def _walk(parentPath: str, entry: FileTreeEntry) -> IFileTree.WalkReturn:
            nonlocal foundTypes
            foundTypes.add(ModFiles.identify(entry))
            return IFileTree.WalkReturn.CONTINUE

        filetree.walk(_walk)

        knownTypes = [x.id for x in self.getAllContents()]
        return [x for x in foundTypes if x in knownTypes]
