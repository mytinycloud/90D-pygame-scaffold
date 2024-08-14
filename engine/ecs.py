import typing
import dataclasses

COMPONENT_COUNT = 0
COMPONENT_INDICES = {}

'''
Required to enable querying of a given component.
The supplied string should be the attribute name that will be used for the component.

The component class will also be converted to a dataclass.
Mutable fields will require factories to ensure the defaults are valid.

@enumerate_component("new_component")
class NewComponent()
    new_field: Vector2 = factory(Vector2)

e = Entity()
e.new_component = NewComponent()
'''
def enumerate_component(name: str):
    global COMPONENT_COUNT
    COMPONENT_INDICES[name] = COMPONENT_COUNT
    COMPONENT_COUNT += 1
    def named_component_inner(component: typing.Callable):
        return dataclasses.dataclass(init=True, slots=True, kw_only=True)(component)
    return named_component_inner

'''
Creates a bitwise mask for all components in the entity
'''
def component_mask(components: tuple[str]):
    mask = 0
    for name in components:
        try:
            i = COMPONENT_INDICES[name]
            mask |= 1 << i
        except:
            continue
    return mask

'''
Provides valid default arguments for components with mutable fields (required for python reasons)
See @enumerate_component for examples.
'''
def factory(constructor: typing.Callable[[],typing.Any]) -> typing.Any:
    return dataclasses.field(default_factory=constructor)

'''
An entity is a collection of components
'''
class Entity():
    def __init__(self, name: str):
        self.name = name # Name for debugging
        self.mask = 0

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
            if key not in ["name", "mask"]:
                setattr(e, key, dataclasses.replace(value))
        return e
    
    
SystemFunction = typing.Callable[['EntityGroup'], None]

class EntityGroup():
    def __init__(self):
        self.entities: list[Entity] = []
        self.systems: list[SystemFunction] = []
        self._singleton_cache: dict[int, Entity] = {}

    '''
    Add a new entity to the group. The components must already be assigned, as they are used for component masks.
    '''
    def add(self, entity: Entity):
        entity.mask = component_mask(vars(entity).keys())
        self.entities.append(entity)

    '''
    Remove an entity from the group.
    '''
    def remove(self, entity: Entity):
        self.entities.remove(entity)

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
        mask = component_mask(components)
        for e in self.entities:
            if e.mask & mask == mask:
                yield e

    '''
    Returns the first entity that contains the require properties.
    This value gets cached, as singletons are not expected to be changed over the group lifetime.
    '''
    def query_singleton(self, *components: str) -> Entity:
        mask = component_mask(components)
        if not mask in self._singleton_cache:
            try:
                self._singleton_cache[mask] = next(self.query(*components))
            except StopIteration:
                raise Exception(f"Singleton not found with [{', '.join(components)}]")
        return self._singleton_cache[mask]