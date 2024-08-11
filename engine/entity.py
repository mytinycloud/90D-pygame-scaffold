import typing

class Entity():
    def __init__(self):
        pass

    '''
    Returns true if this entity contains the specified keys
    '''
    def _contains_properties(self, props: tuple[str]) -> bool:
        for p in props:
            if not hasattr(self, p):
                return False
        return True
    
SystemFunction = typing.Callable[['EntityGroup'], None]

class EntityGroup():
    def __init__(self):
        self.entities: list[Entity] = []
        self.systems: list[SystemFunction] = []

    '''
    Add a new entity to the group
    '''
    def add(self, entity: Entity):
        self.entities.append(entity)

    '''
    Remove an entity from the group.
    '''
    def remove(self, entity: Entity):
        self.entities.remove(entity)

    '''
    Creates a new entity and returns it.
    '''
    def create(self) -> Entity:
        e = Entity()
        self.add(e)
        return e
    
    '''
    Adds a new system
    '''
    def mount_system(self, system: SystemFunction):
        self.systems.append(system)

    '''
    Run all the mounted systems (in the order they were mounted)
    '''
    def run_systems(self):
        for system in self.systems:
            system(self)

    '''
    Yields an iterable of entities which contain the required properties.
    If this becomes too slow, we can just cache these.
    '''
    def query(self, *props: str) -> typing.Generator[Entity, None, None]:
        for e in self.entities:
            if e._contains_properties(props):
                yield e

    '''
    Returns the first entity that contains the require properties.
    If this becomes too slow, we can just cache these.
    '''
    def query_singleton(self, *props: str) -> Entity | None:
        for e in self.entities:
            if e._contains_properties(props):
                return e
        return None
    
    '''
    We can cache queries if it becomes a problem
    '''
    def _hash_props(self, props: list[str]):
        return ','.join(props)

