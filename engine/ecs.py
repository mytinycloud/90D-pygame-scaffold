import typing

class Component():
    def __init__(self):
        pass
    
    '''
    Default way of cloning a component - a shallow copy
    '''
    def clone(self) -> 'Component':
        c = Component()
        for key, value in vars(self).items():
            setattr(c, key, value)
        return c

'''
An entity is a collection of components
'''
class Entity():
    def __init__(self, name: str):
        self.name = name # Name for debugging

    def __repr__(self) -> str:
        return f"<Entity: {self.name}>"

    '''
    Returns true if this entity contains the specified keys
    '''
    def contains(self, components: tuple[str]) -> bool:
        for c in components:
            if not hasattr(self, c):
                return False
        return True
    
    '''
    Clones an entity by cloning its components
    '''
    def clone(self) -> 'Entity':
        e = Entity(self.name)
        for key, value in vars(self).items():
            if key != "name":
                setattr(e, key, value.clone())
        return e
    
    
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
    def create(self, name: str) -> Entity:
        e = Entity(name)
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
    def query(self, *components: str) -> typing.Generator[Entity, None, None]:
        for e in self.entities:
            if e.contains(components):
                yield e

    '''
    Returns the first entity that contains the require properties.
    If this becomes too slow, we can just cache these.
    '''
    def query_singleton(self, *components: str) -> Entity | None:
        for e in self.entities:
            if e.contains(components):
                return e
        return None
    
    '''
    We can cache queries if it becomes a problem
    '''
    def _hash_props(self, props: list[str]):
        return ','.join(props)

