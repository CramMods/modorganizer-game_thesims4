from typing import cast

from mobase import FileTreeEntry, IFileTree, ModDataChecker

from .modfiles import ModFiles


class TheSims4ModDataChecker(ModDataChecker):
    def __init__(self):
        super().__init__()

    def dataLooksValid(self, filetree: IFileTree) -> ModDataChecker.CheckReturn:
        result = cast(ModDataChecker.CheckReturn, self._cleanTree(filetree, True))
        return result

    def fix(self, filetree: IFileTree) -> IFileTree | None:
        return cast(IFileTree, self._cleanTree(filetree))

    def _cleanTree(
        self, tree: IFileTree, checkOnly: bool = False
    ) -> IFileTree | ModDataChecker.CheckReturn:
        checkReturn: ModDataChecker.CheckReturn = ModDataChecker.CheckReturn.INVALID
        newTree: IFileTree = tree.createOrphanTree()
        modTree: IFileTree | None = None
        trayTree: IFileTree | None = None

        def _updateCheckReturn(newValue: ModDataChecker.CheckReturn) -> None:
            nonlocal checkReturn
            if checkReturn == ModDataChecker.CheckReturn.FIXABLE:
                pass
            else:
                checkReturn = newValue

        def _walk(parentPath: str, entry: FileTreeEntry) -> IFileTree.WalkReturn:
            nonlocal checkReturn
            nonlocal newTree
            nonlocal modTree
            nonlocal trayTree

            isFile = entry.fileType() == FileTreeEntry.FileTypes.FILE
            fileType = ModFiles.identify(entry)
            isMod = fileType in [
                ModFiles.FileTypes.MOD_OTHER,
                ModFiles.FileTypes.MOD_PACKAGE,
                ModFiles.FileTypes.MOD_SCRIPT,
            ]
            isTray = fileType in [
                ModFiles.FileTypes.TRAY_LOT,
                ModFiles.FileTypes.TRAY_OTHER,
                ModFiles.FileTypes.TRAY_ROOM,
                ModFiles.FileTypes.TRAY_SIM,
            ]

            if isFile:
                if isMod:
                    if checkOnly:
                        if parentPath.casefold().strip("\\").strip("/") == "mods":
                            _updateCheckReturn(ModDataChecker.CheckReturn.VALID)
                        else:
                            _updateCheckReturn(ModDataChecker.CheckReturn.FIXABLE)
                    else:
                        if not modTree:
                            modTree = newTree.addDirectory("Mods")
                        modTree.copy(entry)

                elif isTray:
                    if checkOnly:
                        if parentPath.casefold().strip("\\").strip("/") == "tray":
                            _updateCheckReturn(ModDataChecker.CheckReturn.VALID)
                        else:
                            _updateCheckReturn(ModDataChecker.CheckReturn.FIXABLE)
                    else:
                        if not trayTree:
                            trayTree = newTree.addDirectory("Tray")
                        trayTree.copy(entry)

            return IFileTree.WalkReturn.CONTINUE

        tree.walk(_walk)

        if checkOnly:
            return checkReturn
        else:
            return newTree
