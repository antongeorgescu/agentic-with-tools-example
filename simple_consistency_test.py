#!/usr/bin/env python3
"""
Simple Consistency Test
=======================
This script tests random number consistency between debug and production modes.
"""

import os
import random
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file."""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes
                    value = value.strip('"\'')
                    os.environ[key] = value
        print("✅ Loaded .env file")
    else:
        print("❌ .env file not found")

def test_random_consistency():
    """Test random number consistency."""
    print("=" * 60)
    print("RANDOM CONSISTENCY TEST")
    print("=" * 60)
    
    # Load environment variables
    load_env_file()
    
    # Test with consistent seed (Production Mode)
    print("\n🏭 PRODUCTION MODE (DEBUG_MODE=false, consistent seed):")
    os.environ["DEBUG_MODE"] = "false"
    seed_value = int(os.getenv("RANDOM_SEED", "42"))
    
    results_prod_1 = []
    results_prod_2 = []
    
    # First run
    random.seed(seed_value)
    for i in range(5):
        results_prod_1.append(random.randint(100, 999))
    
    # Second run with same seed
    random.seed(seed_value)
    for i in range(5):
        results_prod_2.append(random.randint(100, 999))
    
    print(f"  Production Run 1: {results_prod_1}")
    print(f"  Production Run 2: {results_prod_2}")
    print(f"  Consistent: {'✅ YES' if results_prod_1 == results_prod_2 else '❌ NO'}")
    
    # Test with debug mode (Variable results)
    print("\n🐛 DEBUG MODE (DEBUG_MODE=true, no consistent seed):")
    os.environ["DEBUG_MODE"] = "true"
    
    results_debug_1 = []
    results_debug_2 = []
    
    # First run (no seed reset)
    for i in range(5):
        results_debug_1.append(random.randint(100, 999))
    
    # Second run (no seed reset)
    for i in range(5):
        results_debug_2.append(random.randint(100, 999))
    
    print(f"  Debug Run 1: {results_debug_1}")
    print(f"  Debug Run 2: {results_debug_2}")
    print(f"  Different: {'✅ YES' if results_debug_1 != results_debug_2 else '❌ NO'}")
    
    print("\n📊 SUMMARY:")
    print("  • Production mode: Uses consistent seed for reproducible results")
    print("  • Debug mode: Uses random seed for varied results")
    print("  • Set DEBUG_MODE=false in .env for consistent behavior")

def test_sin_generation():
    """Test SIN generation consistency."""
    print("\n" + "=" * 60)
    print("SIN GENERATION CONSISTENCY TEST")
    print("=" * 60)
    
    # Simple SIN generation function (standalone)
    def generate_test_sin(use_consistent_seed=True):
        if use_consistent_seed and os.getenv("DEBUG_MODE", "false").lower() == "false":
            seed_value = int(os.getenv("RANDOM_SEED", "42"))
            random.seed(seed_value)
        
        first_digit = random.randint(1, 9)
        remaining_digits = [random.randint(0, 9) for _ in range(8)]
        sin_digits = [first_digit] + remaining_digits
        return f"{sin_digits[0]}{sin_digits[1]}{sin_digits[2]}-{sin_digits[3]}{sin_digits[4]}{sin_digits[5]}-{sin_digits[6]}{sin_digits[7]}{sin_digits[8]}"
    
    # Test Production Mode
    print("\n🏭 Production SIN Generation:")
    os.environ["DEBUG_MODE"] = "false"
    
    sins_prod = []
    for i in range(3):
        sin = generate_test_sin(use_consistent_seed=True)
        sins_prod.append(sin)
    
    print(f"  Generated SINs: {sins_prod}")
    
    # Test Debug Mode  
    print("\n🐛 Debug SIN Generation:")
    os.environ["DEBUG_MODE"] = "true"
    
    sins_debug = []
    for i in range(3):
        sin = generate_test_sin(use_consistent_seed=True)
        sins_debug.append(sin)
    
    print(f"  Generated SINs: {sins_debug}")
    
    # Analysis
    if sins_prod[0] == sins_prod[1] == sins_prod[2]:
        print("  ✅ Production mode: Consistent (same SIN repeated)")
    else:
        print("  ❌ Production mode: Inconsistent")
    
    if len(set(sins_debug)) > 1:
        print("  ✅ Debug mode: Variable (different SINs)")
    else:
        print("  ⚠️  Debug mode: All same (might need true randomization)")

if __name__ == "__main__":
    test_random_consistency()
    test_sin_generation()
    
    print("\n" + "=" * 60)
    print("✅ CONSISTENCY TEST COMPLETE")
    print("=" * 60)
    print("\n💡 To fix inconsistent results:")
    print("  1. Make sure .env file has DEBUG_MODE=false")
    print("  2. Make sure .env file has RANDOM_SEED=42 (or any consistent value)")
    print("  3. Restart your Python environment/kernel")
    print("  4. Results should now be consistent between debug and production!")