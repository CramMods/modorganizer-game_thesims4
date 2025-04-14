from mobase import IPlugin

from .plugin import TheSims4GamePlugin


def createPlugin() -> IPlugin:
    return TheSims4GamePlugin()
