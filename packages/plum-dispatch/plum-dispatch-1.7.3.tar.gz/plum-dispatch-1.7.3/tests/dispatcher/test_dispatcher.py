import operator
import collections
from typing import Union, List


import pytest

from plum import Dispatcher, Function, NotFoundLookupError, parametric


def _build_function():
    dispatch = Dispatcher()

    @dispatch
    def f(x: int):
        pass

    @dispatch
    def f(x: float):
        pass

    return f


def _build_class(instance):
    dispatch = Dispatcher()

    class A:
        @dispatch
        def f(x: int):
            pass

        @dispatch
        def f(x: float):
            pass

    if instance:
        return A().f
    else:
        return A.f


@pytest.mark.parametrize(
    "build",
    [
        _build_function,
        lambda: _build_class(True),
        lambda: _build_class(False),
    ],
)
def test_methods_precedences(build):
    f = build()
    assert len(f._methods) == 0
    assert len(f._precedences) == 0
    # Try `f.methods` first.
    assert len(f.methods) == 2
    assert len(f.precedences) == 2
    assert f.methods is f._methods
    assert f.precedences is f._precedences

    f = build()
    assert len(f._methods) == 0
    assert len(f._precedences) == 0
    # Try `f.methods` first.
    assert len(f.precedences) == 2
    assert len(f.methods) == 2
    assert f.methods is f._methods
    assert f.precedences is f._precedences


def test_keywords():
    dispatch = Dispatcher()

    @dispatch
    def f(x: int, *, option=None):
        return x

    assert f(2) == 2
    assert f(2, option=None) == 2
    with pytest.raises(NotFoundLookupError):
        f(2, None)


def test_defaults():
    dispatch = Dispatcher()

    y_default = 3

    @dispatch
    def f(x: int, y: int = y_default, *, option=None):
        return y

    @dispatch
    def f(x: float, y: int = y_default, *, option=None):
        return y**2

    assert f(2) == y_default
    assert f(2, option=None) == y_default
    assert f(2, 4) == 4
    assert f(2, y=4) == 4
    assert f(2, y=4, option=None) == 4

    assert f(2.0) == y_default**2
    assert f(2.0, y=4) == 4**2

    with pytest.raises(NotFoundLookupError):
        f(2, 4.0)

    with pytest.raises(NotFoundLookupError):
        f(2, 4.0, option=2)

    # Wrong default type
    with pytest.raises(TypeError):

        @dispatch
        def f(x: int, y: float = y_default):
            return y

    # Ignore wrong type annotations on keyword arguments.
    def f(x: int, y: float = y_default, *, option: int = None):
        return y

    # Multiple arguments
    @dispatch
    def g(x: int, y: int = y_default, z: float = 3.0):
        return (y, z)

    assert g(2) == (y_default, 3.0)


def test_redefinition():
    dispatch = Dispatcher()

    @dispatch
    def f(x: int):
        return "first"

    assert f(1) == "first"

    @dispatch
    def f(x: int):
        return "second"

    assert f(1) == "second"


def test_abstract():
    dispatch = Dispatcher()

    @dispatch.abstract
    def f(x):
        """docstring"""

    assert len(f.methods) == 0
    assert len(f.precedences) == 0
    assert f.__doc__ == "docstring"

    @dispatch
    def f(x: int):
        pass

    assert len(f.methods) == 1
    assert len(f.precedences) == 1
    assert f.__doc__ == "docstring"


def test_abstract_in_class():
    dispatch = Dispatcher()

    class A:
        @dispatch.abstract
        def f(self, x):
            """docstring"""

    assert len(A.f.methods) == 0
    assert len(A.f.precedences) == 0
    assert A.f.__doc__ == "docstring"

    class A:
        @dispatch.abstract
        def f(self, x):
            """docstring"""

        @dispatch
        def f(self, x: int):
            pass

    assert len(A.f.methods) == 1
    assert len(A.f.precedences) == 1
    assert A.f.__doc__ == "docstring"


def test_metadata_and_printing():
    dispatch = Dispatcher()

    class A:
        _dispatch = Dispatcher()

        @_dispatch
        def g(self):
            """docstring of g"""

    @dispatch
    def f():
        """docstring of f"""

    assert f.__name__ == "f"
    assert f.__qualname__ == "test_metadata_and_printing.<locals>.f"
    assert f.__module__ == "tests.dispatcher.test_dispatcher"
    assert f.__doc__ == "docstring of f"
    assert repr(f) == f"<function {f._f} with 1 method(s)>"

    assert f.invoke().__name__ == "f"
    assert f.invoke().__qualname__ == "test_metadata_and_printing.<locals>.f"
    assert f.invoke().__module__ == "tests.dispatcher.test_dispatcher"
    assert f.invoke().__doc__ == "docstring of f"
    n = len(hex(id(f))) + 1  # Do not check memory address and extra ">".
    # Replace `cyfunction` with `function` to play nice with Cython.
    assert repr(f.invoke())[:-n].replace("cyfunction", "function") == repr(f._f)[:-n]

    a = A()
    g = a.g

    assert g.__name__ == "g"
    assert g.__qualname__ == "test_metadata_and_printing.<locals>.A.g"
    assert g.__module__ == "tests.dispatcher.test_dispatcher"
    assert g.__doc__ == "docstring of g"
    assert repr(g) == f'<function {A._dispatch._classes[A]["g"]._f} with 1 method(s)>'

    assert g.invoke().__name__ == "g"
    assert g.invoke().__qualname__ == "test_metadata_and_printing.<locals>.A.g"
    assert g.invoke().__module__ == "tests.dispatcher.test_dispatcher"
    assert g.invoke().__doc__ == "docstring of g"
    assert (
        # Replace `cyfunction` with `function` to play nice with Cython.
        repr(g.invoke())[:-n].replace("cyfunction", "function")
        == repr(A._dispatch._classes[A]["g"]._f)[:-n]
    )


def test_counting():
    dispatch = Dispatcher()

    @dispatch.abstract
    def f(x):
        pass

    assert repr(f) == f"<function {f._f} with 0 method(s)>"

    @dispatch
    def f(x: int):
        pass

    @dispatch
    def f(x: int):
        pass

    # At this point, two methods are pending but not yet resolved. The second is a
    # redefinition of the first, but this will only be clear after the methods are
    # resolved.
    assert repr(f) == f"<function {f._f} with 2 method(s)>"

    # Resolve the methods.
    f(1)

    # Counting should now be right.
    assert repr(f) == f"<function {f._f} with 1 method(s)>"

    @dispatch
    def f(x: str):
        pass

    assert repr(f) == f"<function {f._f} with 2 method(s)>"


def test_multi():
    dispatch = Dispatcher()

    @dispatch
    def f(x):
        return "fallback"

    @dispatch.multi((int,), (str,))
    def f(x: Union[int, str]):
        return "int or str"

    assert f(1) == "int or str"
    assert f("1") == "int or str"
    assert f(1.0) == "fallback"


def test_multi_in_class():
    dispatch = Dispatcher()

    class A:
        @dispatch
        def f(self, x):
            return "fallback"

        @dispatch.multi(
            (
                object,
                int,
            ),
            (
                object,
                str,
            ),
        )
        def f(self, x: Union[int, str]):
            return "int or str"

    a = A()
    assert a.f(1) == "int or str"
    assert a.f("1") == "int or str"
    assert a.f(1.0) == "fallback"


def test_extension():
    dispatch = Dispatcher()

    @dispatch
    def f():
        return "fallback"

    @f.dispatch
    def f(x: int):
        return "int"

    @f.dispatch_multi((str,), (float,))
    def f(x: Union[str, float]):
        return "str or float"

    assert f() == "fallback"
    assert f(1) == "int"
    assert f("1") == "str or float"
    assert f(1.0) == "str or float"


def test_invoke():
    dispatch = Dispatcher()

    @dispatch()
    def f():
        return "fallback"

    @dispatch
    def f(x: int):
        return "int"

    @dispatch
    def f(x: str):
        return "str"

    @dispatch
    def f(x: Union[int, str, float]):
        return "int, str, or float"

    assert f() == "fallback"
    assert f(1) == "int"
    assert f("1") == "str"
    assert f(1.0) == "int, str, or float"
    assert f.invoke()() == "fallback"
    assert f.invoke(int)("1") == "int"
    assert f.invoke(str)(1) == "str"
    assert f.invoke(float)(1) == "int, str, or float"
    assert f.invoke(Union[int, str])(1) == "int, str, or float"
    assert f.invoke(Union[int, str, float])(1) == "int, str, or float"


def test_invoke_in_class():
    dispatch = Dispatcher()

    class A:
        def do(self, x):
            return "fallback"

    class B(A):
        @dispatch
        def do(self, x: int):
            return "int"

    class C(B):
        @dispatch
        def do(self, x: str):
            return "str"

    c = C()

    # Test bound calls.
    assert c.do.invoke(str)("1") == "str"
    assert c.do.invoke(int)(1) == "int"
    assert c.do.invoke(float)(1.0) == "fallback"

    # Test unbound calls.
    assert C.do.invoke(C, str)(c, "1") == "str"
    assert C.do.invoke(C, int)(c, 1) == "int"
    assert C.do.invoke(C, float)(c, 1.0) == "fallback"


def test_errors():
    dispatch = Dispatcher()

    class A:
        @dispatch
        def __init__(self):
            pass

        @dispatch
        def __call__(self):
            pass

    for method in [A, A()]:
        try:
            # No argument are supported, so passing `1` should result in a look-up error.
            method(1)
        except NotFoundLookupError as e:
            # The message should not contain "object". If it does, that would indicate
            # that a non-descriptive error message was thrown.
            assert "object" not in str(e).lower()


def test_runtime_type_of_tracking():
    dispatch = Dispatcher()

    @dispatch
    def f(x: int):
        pass

    assert not f._runtime_type_of
    f(1)
    assert not f._runtime_type_of

    @parametric
    class A:
        pass

    @dispatch
    def f(x: A[1]):
        pass

    assert not f._runtime_type_of
    f(1)
    assert not f._runtime_type_of

    @dispatch
    def f(x: List[int]):
        pass

    assert not f._runtime_type_of
    f(1)
    assert f._runtime_type_of


def test_unassignable_annotations():
    class A:
        @classmethod
        def create(cls):
            pass

    # `A.create` will have an attribute `__annotations__`, but it cannot be assigned.

    f = Function(lambda: None)
    f.dispatch(A.create)
    f()


@pytest.mark.parametrize(
    "f, x, res",
    [
        (operator.attrgetter("x"), collections.namedtuple("NamedTuple", "x")(x=1), 1),
        (operator.itemgetter("x"), {"x": 1}, 1),
    ],
)
def test_nonfunctions(f, x, res):
    plum_f = Function(lambda: None)
    plum_f.dispatch(f)
    assert plum_f(x) == res
