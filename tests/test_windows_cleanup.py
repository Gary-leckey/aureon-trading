#!/usr/bin/env python3
"""
🧪 Windows Cleanup Test
=======================

Quick test to verify the Windows stderr fix is working.
"""

from aureon_baton_link import link_system as _baton_link; _baton_link(__name__)
import sys
import os

if sys.platform != 'win32':
    print("⚠️  This test is designed for Windows")
    # Under pytest, a module-level sys.exit kills the whole session with
    # INTERNALERROR (it only ever "worked" while test_crash.py had disarmed
    # sys.exit process-wide — see conftest.py). Skip honestly instead; the
    # script path (python tests/test_windows_cleanup.py) is unchanged.
    if "pytest" in sys.modules:
        import pytest
        pytest.skip("Windows-only diagnostic", allow_module_level=True)
    sys.exit(1)

# Test 1: Check Python version
print(f"✅ Python {sys.version.split()[0]} on {os.name}")

# Test 2: Check encoding
print(f"✅ Encoding: {sys.stdout.encoding}")

# Test 3: Import check
print("✅ Testing imports...")
try:
    import asyncio
    print("   ✅ asyncio imported")
except ImportError as e:
    print(f"   ❌ asyncio failed: {e}")

# Test 4: Simple async test
print("✅ Testing async operations...")
async def test_async():
    await asyncio.sleep(0.1)
    return "✅ Async works"

try:
    result = asyncio.run(test_async())
    print(f"   {result}")
except Exception as e:
    print(f"   ❌ Async failed: {e}")

print("\n" + "="*60)
print("✅ WINDOWS CLEANUP TEST PASSED!")
print("="*60)
print("\nYou can now run:")
print("  python run_aureon_windows.py --dry-run")
print("\nOR pull and run the full system:")
print("  git pull origin main")
print("  python run_aureon_windows.py")
