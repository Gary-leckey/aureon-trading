"""Pytest conftest: add aureon/ and all its subdirectories to sys.path so bare
module-name imports (e.g. ``from aureon_nexus import ...``) resolve correctly
after the repository reorganisation.

Also runs ``async def`` tests via ``asyncio.run``: 16 test modules define native
coroutine tests, no async pytest plugin is declared in the repo's requirements, and
without one pytest fails every such test with "async def functions are not natively
supported" — so those 16 modules were red on every run without their assertions ever
executing. A stdlib hook keeps the repo's no-extra-dependency posture (the same reason
the JWT verifier is stdlib) while making the tests actually run.
"""

import asyncio
import inspect
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
AUREON = os.path.join(ROOT, "aureon")

for dirpath, dirnames, _filenames in os.walk(AUREON):
    # Skip __pycache__ and hidden directories
    dirnames[:] = [d for d in dirnames if not d.startswith(("__pycache__", "."))]
    if dirpath not in sys.path:
        sys.path.insert(0, dirpath)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def pytest_pyfunc_call(pyfuncitem):
    """Execute native-coroutine tests with asyncio.run (fresh loop per test).

    Returning True tells pytest the call was handled; returning None lets the normal
    sync path run. If a dedicated async plugin (pytest-asyncio/anyio) is ever installed,
    it hooks earlier in the chain and this fallback simply never fires.
    """
    test_fn = pyfuncitem.obj
    if inspect.iscoroutinefunction(test_fn):
        kwargs = {name: pyfuncitem.funcargs[name]
                  for name in pyfuncitem._fixtureinfo.argnames}
        asyncio.run(test_fn(**kwargs))
        return True
    return None
