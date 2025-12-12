
try:
    from stargate_grid import StargateGrid
    print("StargateGrid imported successfully")
    sg = StargateGrid()
    print(f"Grid Coherence: {sg.calculate_grid_coherence()}")
except Exception as e:
    print(f"Import failed: {e}")

try:
    from rainbow_bridge import RainbowBridge
    print("RainbowBridge imported successfully")
except Exception as e:
    print(f"RainbowBridge failed: {e}")

try:
    from aureon_enhancements import EnhancementLayer
    print("EnhancementLayer imported successfully")
    el = EnhancementLayer()
    res = el.get_unified_modifier(0.5, 0.5, 100000, 1000)
    print(f"Unified Modifier: {res.trading_modifier}")
    print(f"Grid Coherence from Layer: {res.grid_coherence}")
except Exception as e:
    print(f"EnhancementLayer failed: {e}")
