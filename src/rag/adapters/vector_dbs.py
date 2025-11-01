from ..core import ports


class EmptyDB(ports.VectorDatabase):
    async def add(self, vectors: list[ports.Vector], documents: list[ports.Document]) -> bool:
        return True

    # async def remove(self, vectors: list[Vector]) -> bool: ...
    async def search_similar(self, vector: ports.Vector) -> list[ports.Vector]:
        return []

    async def look_up(self, vectors: list[ports.Vector]) -> list[ports.Document]:
        return []
