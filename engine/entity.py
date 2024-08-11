import typing

class Entity():
    def __init__(self):
        self.pos: tuple[int, int] = (0,0)

    '''
    Returns true if this entity contains the specified keys
    '''
    def contains_properties(self, props: tuple[str]) -> bool:
        for p in props:
            if not hasattr(self, p):
                return False
        return True

class EntityGroup():
    def __init__(self):
        self.entities: list[Entity] = []

    def add(self, entity: Entity):
        self.entities.append(entity)

    def remove(self, entity: Entity):
        self.entities.remove(entity)

    '''
    Yields an iterable of entities which contain the required properties.
    If this becomes too slow, we can just cache these.
    '''
    def query(self, *props: str) -> typing.Generator[Entity]:
        for e in self.entities:
            if e.contains_properties(props):
                yield e

    '''
    Returns the first entity that contains the require properties.
    If this becomes too slow, we can just cache these.
    '''
    def query_singleton(self, *props: str) -> Entity | None:
        for e in self.entities:
            if e.contains_properties(props):
                return e
        return None
    
    '''
    We can cache queries if it becomes a problem
    '''
    def _hash_props(self, props: list[str]):
        return ','.join(props)

