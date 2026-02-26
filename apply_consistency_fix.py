#!/usr/bin/env python3
"""
Apply Consistency Fix to Your Code
==================================
This script applies the consistency fixes to your existing Python files.
"""

import os
import re
from pathlib import Path

def apply_environment_loading():
    """Add environment loading to Python files that need it."""
    
    files_to_fix = [
        "generate_chats.py",
        "chat_tools.py", 
        "app.py"
    ]
    
    env_loading_code = '''
# Load environment variables from .env file
def load_dotenv():
    """Load environment variables from .env file for consistent configuration."""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip('"\\'')
                    os.environ[key] = value

# Load environment at module level
load_dotenv()

# Apply consistent random seed for production mode
if os.getenv("DEBUG_MODE", "false").lower() == "false":
    import random
    seed_value = int(os.getenv("RANDOM_SEED", "42"))
    random.seed(seed_value)
    print(f"🎲 Applied consistent random seed: {seed_value}")
'''
    
    for filename in files_to_fix:
        if Path(filename).exists():
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if fix is already applied
            if "load_dotenv()" not in content:
                # Find import section end
                import_end = 0
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if (line.startswith('import ') or 
                        line.startswith('from ') or 
                        line.strip() == '' or 
                        line.strip().startswith('#')):
                        import_end = i + 1
                    else:
                        break
                
                # Insert environment loading after imports
                lines.insert(import_end, env_loading_code)
                new_content = '\n'.join(lines)
                
                # Write fixed file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Applied consistency fix to {filename}")
            else:
                print(f"⚠️  {filename} already has consistency fix")
        else:
            print(f"❌ {filename} not found")

def create_usage_instructions():
    """Create usage instructions file."""
    
    instructions = """
# Debug vs Production Mode Fix - Usage Instructions

## The Problem
Your Python project was producing different results in debug mode vs production mode due to:
- Inconsistent random number generation
- Missing environment variables  
- Different execution contexts

## The Solution Applied
1. **Environment Configuration (.env file)**: Added consistent config
2. **Random Seed Management**: Applied consistent seeding for production mode
3. **Debug Mode Toggle**: Use DEBUG_MODE environment variable to control behavior

## How to Use

### For Consistent/Reproducible Results (Production Mode):
```bash
# Set in .env file or environment:
DEBUG_MODE=false
RANDOM_SEED=42
```
- Results will be identical every time
- Good for testing, production, demos

### For Variable Results (Debug/Development Mode):
```bash
# Set in .env file or environment:
DEBUG_MODE=true
# RANDOM_SEED is ignored in debug mode
```
- Results will vary between runs
- Good for development, testing different scenarios

## Testing Your Fix

1. **Run the consistency test:**
   ```bash
   python simple_consistency_test.py
   ```

2. **Test with your actual code:**
   ```bash
   # Production mode (consistent results)
   python generate_chats.py --seed 42 -n 5
   
   # Should produce identical results each time
   ```

3. **Switch modes by editing .env file:**
   - Change DEBUG_MODE=false to DEBUG_MODE=true
   - Restart your Python environment
   - Run tests again to see different behavior

## Environment Variables

The .env file contains:
- `DEBUG_MODE`: Controls consistency behavior
- `RANDOM_SEED`: Seed value for consistent results  
- `FORCE_RANDOM_SIN`: Always generate random SINs
- Azure OpenAI configuration

## Files Modified

- `.env` - Added consistency configuration
- `generate_chats.py` - Added environment loading and seeding
- `chat_tools.py` - Added consistent random generation
- `simple_consistency_test.py` - Test script to verify fix

## Troubleshooting

- **Still getting different results?** 
  - Check DEBUG_MODE=false in .env file
  - Restart Python environment/kernel
  - Verify random seed is being applied

- **Want truly random results?**
  - Set DEBUG_MODE=true in .env file
  - Or remove/comment out RANDOM_SEED

- **Import errors?**
  - Run: pip install flask openai langchain
  - Check that .env file is loaded properly

## Quick Commands

```bash
# Install dependencies (if needed)
pip install flask openai langchain

# Test consistency
python simple_consistency_test.py

# Run with consistent results
python generate_chats.py --seed 42 -n 3

# Check environment
python debug_environment.py
```

## Success Indicators

✅ simple_consistency_test.py shows "Consistent: YES" for production mode
✅ debug_environment.py shows all packages installed
✅ generate_chats.py produces identical results with same seed
✅ No more "out of range" results between debug and production!
"""
    
    with open("FIX_INSTRUCTIONS.md", "w", encoding="utf-8") as f:
        f.write(instructions.strip())
    
    print("✅ Created FIX_INSTRUCTIONS.md")

def main():
    """Apply all consistency fixes."""
    
    print("=" * 60)
    print("APPLYING CONSISTENCY FIXES")
    print("=" * 60)
    
    # Step 1: Apply environment loading to Python files
    print("\n1. Applying environment loading fixes...")
    apply_environment_loading()
    
    # Step 2: Create usage instructions
    print("\n2. Creating usage instructions...")
    create_usage_instructions()
    
    print("\n" + "=" * 60)
    print("✅ CONSISTENCY FIXES APPLIED!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Restart your Python environment/kernel")
    print("2. Run: python simple_consistency_test.py")
    print("3. Read: FIX_INSTRUCTIONS.md for detailed usage")
    print("4. Test your actual code - results should now be consistent!")

if __name__ == "__main__":
    main()