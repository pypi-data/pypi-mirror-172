from __future__ import annotations


class GenotypeFactoryError(RuntimeError):
    @classmethod
    def character_not_allowed(cls, char: str) -> GenotypeFactoryError:
        return cls(f'Character not allowed: {char}')
