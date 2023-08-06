from typing import List


class VersionBump:
    def __init__(self, version: str):
        self.version = version

    @property
    def parts(self) -> List[int]:
        return [int(i) for i in self.version.split(".")]

    @property
    def patch(self) -> str:
        parts = self.parts
        parts[2] += 1
        return self.semvar(parts)

    @property
    def minor(self) -> str:
        parts = self.parts
        parts[1] += 1
        parts[2] = 0
        return self.semvar(parts)

    @property
    def major(self) -> str:
        parts = self.parts
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
        return self.semvar(parts)

    @staticmethod
    def semvar(parts: List[int]) -> str:
        return ".".join([str(i) for i in parts])
