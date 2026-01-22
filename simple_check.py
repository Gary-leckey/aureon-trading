
import sys
print(f"Python: {sys.executable}")
try:
    import numpy
    print(f"Numpy: {numpy.__version__}")
except ImportError as e:
    print(f"Numpy Import Failed: {e}")
