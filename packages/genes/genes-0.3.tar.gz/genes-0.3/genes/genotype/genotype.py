
from collections.abc import Sized
from typing import List


class Genotype(Sized):

    _data: List[bool]

    def __init__(self, genotype: List[bool]):
        self._data = genotype

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, item) -> bool:
        return self._data[item]

    def data(self) -> List[bool]:
        return self._data

    def __str__(self) -> str:
        result: str = ''
        for i in self._data:
            result += '0' if i is False else '1'
        return result
