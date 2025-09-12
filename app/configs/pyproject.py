import tomllib
from enum import StrEnum


class Managers(StrEnum):
    poetry = "tool.poetry"
    uv = "project"


class _ParserPyproject:
    def __init__(self, manager: Managers, pyproject_toml: str = "pyproject.toml"):
        with open(pyproject_toml, "rb") as f:
            self._pyproject_toml = tomllib.load(f)
        self._tool = self._pyproject_toml.get("tool", {})

        _prev_manager = None
        for key in manager.value.split("."):
            self._manager = self._pyproject_toml.get(key, {})
            if self._manager:
                _prev_manager = self._manager
            else:
                self._manager = _prev_manager.get(key, {})

        self.name = self._manager.get("name", {})
        self.version = self._manager.get("version")


class ParserPyproject:
    __slots__ = ()
    _parser = _ParserPyproject(Managers.uv)
    name = _parser.name
    version = _parser.version
