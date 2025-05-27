"""
Get the type annotation of an object as per PEP 484.

Its canonical open-source location is:
https://github.com/Temerold/annotation-generator
"""

from typing import Any, Callable, Dict, Iterable, List, Set, Tuple, Union


def get_type_annotation(obj: Any, alphabetize: bool = True) -> Any:
    """Get the type annotation of an object as per PEP 484.

    Args:
        obj: The object to get the type annotation for.
        alphabetize: If True, sorts the types in the annotation alphabetically.
            Defaults to True.

    Returns:
        The type annotation of the object.
    """

    def _sorted(
        iterable: Iterable,
        /,
        *,
        key: Callable | None = None,
        reverse: bool = False,
    ) -> list:
        return (
            sorted(iterable, key=key, reverse=reverse)
            if alphabetize
            else list(iterable)
        )

    primitives = [bool, float, int, str, type(None)]  # TODO: Add more types

    if type(obj) in primitives:
        return type(obj)

    if isinstance(obj, dict):
        key_types = _sorted([get_type_annotation(k) for k in obj.keys()], key=str)
        val_types = _sorted([get_type_annotation(v) for v in obj.values()], key=str)
        key_annotation = Union[tuple(key_types)] if len(key_types) > 1 else key_types[0]
        val_annotation = Union[tuple(val_types)] if len(val_types) > 1 else val_types[0]
        return Dict[key_annotation, val_annotation]

    if not isinstance(obj, (list, set, tuple)):  # TODO: Use `Iterable` instead?
        return type(obj)

    types = _sorted([get_type_annotation(e) for e in obj], key=str)

    # TODO: Handle cases where `obj` is an empty iterable. I don't look forward to this.
    if isinstance(obj, (list, set)):
        annotation = Union[tuple(types)] if len(types) > 1 else types[0]
        return List[annotation] if isinstance(obj, list) else Set[annotation]

    if isinstance(obj, tuple):
        if len(set(types)) != 1 or len(obj) == 1:
            return Tuple[types]
        else:
            return Tuple[types[0], ...]
